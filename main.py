from threading import Lock
from telebot import types, TeleBot
from telebot.util import quick_markup
from MapPoint import *
from os import path

# https://t.me/SmrModernGuideBot
# save file_id for speedup (warmup period)

bot: TeleBot = TeleBot('5909930778:AAF4IKk3PqYiTq9hTqQZnr7-ZUAXBttkkAk')
file = 'data.txt'
userpos_lock: dict[int, Lock] = {}
userpos: dict[int, int] = {}
chat_user_accord: dict[int, int] = {}
MapPoints: list[MapPoint] = []
Warmed = False
iter = types.ReplyKeyboardMarkup()
iter.row('Идём дальше!')
iter.row("Помощь")

if __name__ == '__main__':
	MapPoints = []
	with open(file, "r", encoding="utf8") as f:
		buf = []
		for s in f:
			buf.append(s.strip("\n"))
			if (len(buf) == 4):
				MapPoints.append(
					MapPoint(
						CAPTION = buf[0],
						DESC = buf[1],
						IMGURL = f"{path.curdir}/{buf[2]}",
						MAPURL = buf[3]
					)
				)
				buf = []

@bot.message_handler(
	func = lambda message:
		not(message.from_user.id in userpos.keys()) or
		message.text.lower() == 'начать заново'
)
def init_user(message: types.Message):
	start(message)

@bot.message_handler(
	commands=['start']
)
def start(message: types.Message) -> None:
	global chat_user_accord, userpos, userpos_lock
	print(f"User {message.from_user.id} is known: {message.from_user.id in chat_user_accord.keys()}")
	markup = types.ReplyKeyboardMarkup()
	markup.row('Посмотреть маршрут на карте')
	markup.row('Узнать про объекты')
	bot.send_message(
		message.chat.id,
		f"Привет, {message.from_user.first_name}! Для того чтобы продолжить, выберите действие",
		reply_markup=markup
		)
	chat_user_accord[message.from_user.id] = message.chat.id
	userpos_lock[message.from_user.id] = Lock()
	userpos_lock[message.from_user.id].acquire()
	userpos[message.from_user.id] = 0
	userpos_lock[message.from_user.id].release()

@bot.message_handler(
	content_types=['text'],
	func=lambda message:
		message.text.lower() == 'узнать про объекты'
)
def travel_begin(message: types.Message):
	global userpos, userpos_lock
	
	userpos_lock[message.from_user.id].acquire()
	markup = quick_markup(
	{
		"Открыть на карте":
		{
			"url": MapPoints[userpos[message.from_user.id]].mapURL ,
			"callback_data": message.chat.id
		}
	}, row_width=1)
	if userpos[message.from_user.id] >= len(MapPoints):
		return travel_end(message)
	markup = quick_markup(
	{
		"Открыть на карте":
		{
			"url": MapPoints[userpos[message.from_user.id]].mapURL ,
			"callback_data": message.chat.id
		}
	}, row_width=1)
	while True:
		try:
			if (MapPoints[userpos[message.from_user.id]].last_id):
				msg_img = bot.send_photo(
					message.chat.id,
					MapPoints[userpos[message.from_user.id]].last_id,
					MapPoints[userpos[message.from_user.id]].caption,
					reply_markup=markup
				)
				MapPoints[userpos[message.from_user.id]].last_id = msg_img.photo[-1].file_id
			else:
				with open(MapPoints[userpos[message.from_user.id]].imgURL, "rb") as p:
					msg_img = bot.send_photo(
						message.chat.id,
						types.InputFile(p),
						MapPoints[userpos[message.from_user.id]].caption,
						reply_markup=markup
					)
					MapPoints[userpos[message.from_user.id]].last_id = msg_img.photo[-1].file_id
			break
		except Exception as e:
			# print(e)
			if userpos[message.from_user.id] >= len(userpos):
				userpos[message.from_user.id] = len(MapPoints) - 1 
			else:
				userpos[message.from_user.id]
			print(f"Retry \"{MapPoints[userpos[message.from_user.id]].caption}\"")
	bot.send_message(
		message.chat.id,
		MapPoints[userpos[message.from_user.id]].desc,
		reply_markup=iter
	)
	userpos[message.from_user.id] += 1
	userpos_lock[message.from_user.id].release()

@bot.message_handler(
	func=lambda message: message.text.lower() == 'сброс маршрута'
)
def travel_reset(message: types.Message):
	global userpos, userpos_lock
	
	userpos_lock[message.from_user.id].acquire()
	userpos[message.from_user.id] = 0
	bot.send_message(
		message.chat.id,
		"Маршрут сброшен",
		reply_markup=iter
	)
	userpos_lock[message.from_user.id].release()

@bot.message_handler(
	content_types=['text'],
	func=lambda message:
		message.text.lower() == 'идём дальше!' and
		message.from_user.id in userpos.keys() and
		userpos[message.from_user.id] < len(MapPoints)
)
def travel_next(message: types.Message):
	global userpos, userpos_lock
	userpos_lock[message.from_user.id].acquire()
	if userpos[message.from_user.id] >= len(MapPoints):
		return travel_end(message)
	markup = quick_markup(
	{
		"Открыть на карте":
		{
			"url": MapPoints[userpos[message.from_user.id]].mapURL ,
			"callback_data": message.chat.id
		}
	}, row_width=1)
	while True:
		try:
			if (MapPoints[userpos[message.from_user.id]].last_id):
				msg_img = bot.send_photo(
					message.chat.id,
					MapPoints[userpos[message.from_user.id]].last_id,
					MapPoints[userpos[message.from_user.id]].caption,
					reply_markup=markup
				)
				MapPoints[userpos[message.from_user.id]].last_id = msg_img.photo[-1].file_id
			else:
				with open(MapPoints[userpos[message.from_user.id]].imgURL, "rb") as p:
					p.seek(0);
					msg_img = bot.send_photo(
						message.chat.id,
						types.InputFile(p),
						MapPoints[userpos[message.from_user.id]].caption,
						reply_markup=markup
					)
					MapPoints[userpos[message.from_user.id]].last_id = msg_img.photo[-1].file_id
			break
		except Exception as e:
			if userpos[message.from_user.id] >= len(MapPoints):
				userpos[message.from_user.id] = len(MapPoints) - 1 
			else:
				userpos[message.from_user.id]
			print(f"Retry \"{MapPoints[userpos[message.from_user.id]].caption}\"")
	bot.send_message(
		message.chat.id,
		MapPoints[userpos[message.from_user.id]].desc,
		reply_markup=iter
	)
	userpos[message.from_user.id] += 1
	userpos_lock[message.from_user.id].release()

	global Warmed
	if not Warmed:
		travel_next.warmed = True
		for p in MapPoints:
			travel_next.warmed = travel_next.warmed and p.last_id != None
		if travel_next.warmed:
			print("Warmed")
			Warmed = True

@bot.message_handler(
	content_types=['text'],
	func=lambda message:
		message.text.lower() == 'идём дальше!' and
		message.from_user.id in userpos.keys() and
		userpos[message.from_user.id] >= len(MapPoints)
)
def travel_end(message: types.Message):
	global userpos, userpos_lock
	userpos_lock[message.from_user.id].acquire()
	
	iter = types.ReplyKeyboardMarkup()
	iter.row('Начать заново')
	iter.row("Помощь")

	bot.send_message(
		message.chat.id,
		"""
		Итак, к сожалению, наша экскурсия подошла
к концу. Было очень увлекательно, неправда
ли? Мы будем рады видеть Вас снова!
		""",
		reply_markup=iter
	)
	userpos[message.from_user.id] = 0
	userpos_lock[message.from_user.id].release()

@bot.message_handler(
	content_types=['text'],
	func=lambda message: message.text.lower() == 'посмотреть маршрут на карте'
)
def map_view(message: types.Message):
	markup_btn = quick_markup(
	{
		"Открыть маршрут на карте":
		{
			"url": 'https://yandex.ru/maps/-/CCUzZFVK3D',
			"callback_data": message.chat.id
		}
	}, row_width=1)
	markup = markup_btn
	bot.send_message(
		message.chat.id,
		"Для открытия навигации нажмите на кнопку ниже:",
		reply_markup=markup, 
	)

@bot.message_handler(
	func=lambda message: message.text.lower() == 'скрыть клавиатуру'
)
def hide_kb(message: types.Message):
	bot.send_message(message.from_user.id, 'Клавиатура убрана.', reply_markup = types.ReplyKeyboardRemove())

@bot.message_handler(
	func=lambda message: message.text.lower() == 'вернутся'
)
def ret(message: types.Message):
	global userpos, userpos_lock
	userpos_lock[message.from_user.id].acquire()
	userpos[message.from_user.id] -= 1
	userpos_lock[message.from_user.id].release()
	travel_next(message)

@bot.message_handler(
	func=lambda message:
		message.text.lower() == 'помощь' or
		message.text.lower() == '/help'
)
def help(message: types.Message) -> None:
	markup = types.ReplyKeyboardMarkup()
	markup.row('Сброс маршрута')
	markup.row('Скрыть клавиатуру')
	markup.row('Вернутся')
	bot.send_message(
		message.from_user.id,
		'Выбирите действие',
		reply_markup = markup
	)

@bot.message_handler(
	content_types=['text']
)
def err404(message: types.Message):
	bot.send_message(
		message.chat.id, 
		"😢К сожалению, это не является командой. Убедитесь в правильности команды"
	)

if __name__ == '__main__':
	print("Bot started\nWarming up")
	try:
		bot.infinity_polling(logger_level=3)
	except KeyboardInterrupt:
		for u in chat_user_accord.keys():
			bot.send_message(u, "В данный момент бот был отключён для обслуживания, но скоро возбновит работу")