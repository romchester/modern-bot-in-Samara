class MapPoint():
	caption: str
	desc: str
	imgURL: str
	mapURL: str

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