import sys
sys.path.append('../')
from BaseWeb.WebPageBase import *

class TruyenZObject(RelaxObject):
	def GetListChapter(self, soup, type):
		listTagChapter = soup.find("ul", attrs={ "class" : "main version-chap"})
		listChapter = []
		for tag in listTagChapter:
			if tag.name == "li":
				listChapter.append(ChapterTruyenZ(tag.a["href"], type))
		return listChapter
		
	def GetName(self, soup):
		title = soup.find("div", attrs=({"class":"post-title"}))
		tagName = title.h1.text.strip().replace("\t","").replace("\n"," - ")
		return tagName
	
	def GetType(self, soup):
		nameChap = soup.find("div", attrs=({"class": "genres-content"})).text
		if "Anime" in nameChap:
			return MangaType.Anime
		if "Novel" in nameChap:
			return MangaType.Novel
		if "Audio" in nameChap:
			return MangaType.Audio
		return MangaType.Manga
	
	
class ChapterTruyenZ(ChapterObject):
	def GetName(self, soup):
		nameChap = soup.find("option", attrs=({"data-redirect": self.url})).text
		return nameChap
		
	def GetAnime(self, soup):
		pass
	def GetManga(self, soup):
		pass
	def GetNovel(self, soup):
		listText = []
		containtText = soup.find("div", attrs=({"class":"text-left"}))
		listText.append(containtText.h3.text)
		i = 1
		for c in containtText.children:
			if c is not None:
				listText.extend(self.GetTextNovel(c))
		return "\n".join(listText)
	def GetTextNovel(self, soupTag):
		if soupTag.name == "p":
			return [soupTag.text]
		if soupTag.name == "span":
			return [soupTag.text]
		if soupTag.name == "div":
			count = 0;
			for c in soupTag.children:
				count = count + 1
			if "class" not in soupTag.attrs or soupTag["class"][0] != 'tptn_counter':
				if count == 1:
					childs = [e for e in soupTag.children if e is not None]
					if isinstance(childs[0],str) == True:
						return [childs[0]]
					else:
						return self.GetTextNovel(childs[0])
				else:
					listText =[]
					for c in soupTag.children:
						listText.extend(self.GetTextNovel(c))
					return listText
		return []
			#TODO