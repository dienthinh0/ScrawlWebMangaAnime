import os
import requests
from bs4 import BeautifulSoup
import io
import re

def RemoveIgnoreChar(strChar):
	ignoreStr = '\\\/*"<>:?|'
	outstr = strChar
	for char in ignoreStr:
		outstr = outstr.replace(char, "")
	return outstr
class HttpRequest:
	@staticmethod
	def GetHtmlData(url):
		r = requests.get(url)
		return r.text
class RelaxObject:
	url = ""
	type = 0 #TODO
	name = ""
	info = ""
	listChapter = []
	def __init__(self, url):
		self.url = url
	
	def FetchData (self):
		print ("Fetch:" + self.url)
		dataHtml = HttpRequest.GetHtmlData(self.url)
		soup = BeautifulSoup(dataHtml, 'lxml')
		if soup is not None:
			self.name = self.GetName(soup)
			self.listChapter = self.GetListChapter(soup)
	def FetchAndSaveData(self,path):
		self.FetchData()
		nameFolder = self.GenerateFolder(path)
		self.SaveInfo(nameFolder)

	def GenerateFolder(self, path):
		nameFolder = os.path.join(path, RemoveIgnoreChar(self.name))
		
		if os.path.exists(nameFolder) == False:
			os.mkdir(nameFolder)
		return nameFolder
		
	def FetchAllChap(self):
		for chap in self.listChapter:
			chap.FetchData()
	
	def FetchAndSaveAllChap(self,path):
		nameFolder = self.GenerateFolder(path)
		for chap in self.listChapter:
			chap.FetchData()
			chap.SaveData(nameFolder)

	def SaveInfo(self, nameFolder):
		f = open(os.path.join(nameFolder , RemoveIgnoreChar(self.name) + ".txt"), 'w+')
		f.write(str(self.type))
		f.write(self.info)
		f.close()
	
	def GetName(self, soup):
		pass
		
	def GetListChapter(self, soup):
		pass

class ChapterObject:
	url = ""
	name = ""
	type = 0
	data = None
	
	def __init__(self, url):
		self.url = url
		#Cheat
		self.type = 2
		
	def FetchData(self):
		print ("Fetch Data Chap :" + self.url)
		dataHtml = HttpRequest.GetHtmlData(self.url)
		soup = BeautifulSoup(dataHtml, 'lxml')
		if soup is not None:
			self.name = self.GetName(soup)
			self.data = self.GetData(soup)
	def GetName(self, soup):
		pass
	
	def GetData(self, soup):
		dataContent = None
		if self.type == 0:
			dataContent = self.GetAnime(soup)
		elif self.type == 1:
			dataContent = self.GetManga(soup)
		elif self.type == 2:
			dataContent = self.GetNovel(soup)
		elif self.type == 3:
			dataContent = self.GetAudio(soup)
		return dataContent
		
	def GetAnime(self, soup):
		pass
		
	def GetManga(self, soup):
		pass
		
	def GetNovel(self, soup):
		pass
		
	def GetAudio(self,soup):
		pass
		
	def SaveData(self, path):
		if self.data is None:
			self.data = self.FetchData()
		if self.type == 0:
			self.SaveDataAnime(path)
		elif self.type == 1:
			self.SaveDataManaga(path)
		elif self.type == 2:
			self.SaveDataNovel(path)
		elif self.type == 3:
			self.SaveDataAudio(path)
		
	def SaveDataAudio(self,path):
		pass
	
	def SaveDataNovel(self,path):
		f = io.open(os.path.join(path , RemoveIgnoreChar(self.name) + ".txt"),"w+", encoding="utf-8")
		f.write(self.data)
		f.close()
	
	def SaveDataManaga(self, path):
		pass
		
	def SaveDataAnime(self, path):
		pass
	
class TruyenZObject(RelaxObject):
	def GetListChapter(self, soup):
		listTagChapter = soup.find("ul", attrs={ "class" : "main version-chap"})
		listChapter = []
		for tag in listTagChapter:
			if tag.name == "li":
				listChapter.append(ChapterTruyenZ(tag.a["href"]))
		return listChapter
		
	def GetName(self, soup):
		title = soup.find("div", attrs=({"class":"post-title"}))
		tagName = title.h1.text.strip().replace("\t","").replace("\n"," - ")
		return tagName	
	
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
class ScrawlWebManager:
	
	listRelaxObject = []
	savePath = "./"
	def SetSavePath(path):
		ScrawlWebManager.savePath = path
	def PushRelax(url):
		ScrawlWebManager.listRelaxObject.append(ScrawlWebManager.CreateRelaxObject(url))

	def ClearRelax():
		ScrawlWebManager.listRelaxObject = []
		
	def CreateRelaxObject(url):
		domain = url.split("//")[1].split("/")[0]
		relaxObject = None
		if domain == "truyenz.info":
			relaxObject = TruyenZObject(url)
		return relaxObject
	
	def FetchandSaveRelaxObject():
		for relax in ScrawlWebManager.listRelaxObject:
			relax.FetchAndSaveData(ScrawlWebManager.savePath)
			relax.FetchAndSaveAllChap(ScrawlWebManager.savePath)
			

ScrawlWebManager.PushRelax("https://truyenz.info/manga/light-novel-solo-leveling")
ScrawlWebManager.SetSavePath("C:\\Users\\dient\\Desktop\\scrawlManga")
ScrawlWebManager.FetchandSaveRelaxObject()
print ("Done")
#a = BeautifulSoup("<div class='adsf'></div>","lxml")
#print("class" in a.div.attrs)