class MapPoint():
	caption: str = str()
	desc: str = str()
	imgURL: str = str()
	last_id: str = str()
	mapURL: str = str()

	def __init__(
		self, 
		CAPTION: str,
		DESC: str,
		IMGURL: str,
		MAPURL: str,
	):
		self.caption = CAPTION
		self.desc = DESC
		self.imgURL = IMGURL
		self.mapURL = MAPURL