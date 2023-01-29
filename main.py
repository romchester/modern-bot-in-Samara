from telebot import types, TeleBot
from telebot.util import quick_markup

# URL of photos is not local for speedup (using user cache)

bot: TeleBot
photos = dict()
if __name__ == '__main__':
  bot = TeleBot('5909930778:AAF4IKk3PqYiTq9hTqQZnr7-ZUAXBttkkAk')

def inline_query_handler(inline_query: types.InlineQuery) -> None:
  pass

@bot.message_handler(commands=['start'])
def start(message: types.Message) -> None:
  markup = types.ReplyKeyboardMarkup()
  markup.row('Посмотреть маршрут на карте')
  markup.row('Узнать про объекты')
  bot.send_message(
    message.chat.id,
    f"Привет, {message.from_user.first_name}! Для того чтобы продолжить, выберите действие",
    reply_markup=markup
    )

@bot.message_handler(commands=['info'])
def info(message: types.Message) -> None:
  markup = types.ReplyKeyboardMarkup()
  markup.row('Получить информацию по первому объекту')
  markup.row('Получить информацию по второму объекту')
  markup.row('Скрыть клавиатуру')
  markup.row('Вернутся')
  bot.send_message(
    message.from_user.id,
    'Нажмите на кнопку ниже, чтоб получить информацию.',
    reply_markup = markup
  )

@bot.message_handler(content_types=['text'])
def info_by(message: types.Message) -> None:
  if   message.text.lower() == 'получить информацию по первому объекту':
    bot.send_photo(
      message.from_user.id,
      'https://commons.wikimedia.org/wiki/File:Samara_Chapayevskaya_163.jpg#/media/Файл:Samara_Chapayevskaya_163.jpg',
      caption = 'Особняк Э.Г. Эрна')
    bot.send_message(
      message.chat.id,
      'Доктор Эрн, надворный советник, заказал проект дома Щербачёву в 1900 году. Дом был закончен в 1902 году, Эрн переехал в него с семьёй. Часть помещений сдавалась другим докторам под кабинеты и квартиры[1].Так с 1913 года здесь принимал врач Абрам Гринберг – сын доктора М. А. Гринберга, а другой сын Иосиф Гринберг – присяжный поверенный самарского окружного суда - снимал апартаменты[2].В 1920-е годы в бывшем доме Эрна находилось отделение самарской ВЧК (позже ОГПУ)[1]. В 1941—1943 году в здании размещалось эвакуированное из Москвы посольство Польши. В частности, в этом здании 4 декабря 1941 года наркомом иностранных дел СССР В. М. Молотовым и председателем правительства Польши в изгнании В. Сикорским была подписана Декларация «О достижении прочного и справедливого мира»[3][4]. Впоследствии особняк вошёл в состав комплекса Самарской областной клинической больницы № 2, в нем расположена поликлиника[4].'
    )
  elif message.text.lower() == 'получить информацию по второму объекту':
    bot.send_photo(
      message.from_user.id,
      'https://raw.githubusercontent.com/AFETZ/first_step.py/925caf7aaed417dc4d62160bd78eefc498f07875/2.jpg',
      caption = 'Музей модерна')
    bot.send_message(
      message.chat.id,
      "Музей Модерна на территории усадьбы Курлиных – это целостная архитектурно-историческая среда, культурная модель эпохи модерна конца XIX – начала XX веков, времени наивысшего расцвета купеческой Самары.\n"
      "Усадьбу Курлиных по праву называют «жемчужиной» самарского модерна. Музей Модерна открылся в конце 2012 года, он занимается изучением стиля модерн в регионе, сбором информации и предметов той эпохи"
    )
  elif message.text.lower() == 'скрыть клавиатуру':
      bot.send_message(message.from_user.id, 'Клавиатура убрана.', reply_markup = types.ReplyKeyboardRemove())
  elif message.text.lower() == 'вернутся':
      start(message)
  elif message.text.lower() == 'посмотреть маршрут на карте':
    markup = quick_markup(
      {
        "Открыть маршрут на карте": {
          "url": 'https://yandex.ru/maps/-/CCUzZFVK3D'
        }
      }
    )
    bot.send_message(
      message.chat.id,
      "Для открытия навигации нажмите на кнопку ниже:",
      reply_markup=markup
    )
  elif message.text.lower() == 'узнать про объекты':
    info(message)
  else:
    bot.send_message(
      "😢К сожалению, это не является командой. Убедитесь в правильности команды"
    )

if __name__ == '__main__':
  bot.inline_handler(inline_query_handler)
  bot.infinity_polling(logger_level=3)