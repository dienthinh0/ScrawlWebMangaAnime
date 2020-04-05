import sys
sys.path.append('../')
from bs4 import BeautifulSoup
from enum import Enum
from Request.HttpRequest import *
import os
import io

def RemoveIgnoreChar(strChar):
	ignoreStr = '\\\/*"<>:?|'
	outstr = strChar
	for char in ignoreStr:
		outstr = outstr.replace(char, "")
	return outstr
	
class MangaType(Enum):
	Anime = 0
	Manga = 1
	Novel = 2
	Audio = 3

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
		self.type = self.GetType(soup)
		if soup is not None:
			self.name = self.GetName(soup)
			self.listChapter = self.GetListChapter(soup, self.type)
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
	
	def GetType(self, soup):
		pass
	
	def GetName(self, soup):
		pass
		
	def GetListChapter(self, soup, type):
		pass

class ChapterObject:
	url = ""
	name = ""
	type = 0
	data = None
	
	def __init__(self, url, type):
		self.url = url
		self.type = type
		
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
		if self.type == MangaType.Anime:
			dataContent = self.GetAnime(soup)
		elif self.type == MangaType.Manga:
			dataContent = self.GetManga(soup)
		elif self.type == MangaType.Novel:
			dataContent = self.GetNovel(soup)
		elif self.type == MangaType.Audio:
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
		if self.type == MangaType.Anime:
			self.SaveDataAnime(path)
		elif self.type == MangaType.Manga:
			self.SaveDataManaga(path)
		elif self.type == MangaType.Novel:
			self.SaveDataNovel(path)
		elif self.type == MangaType.Audio:
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
	