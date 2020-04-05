from bs4 import BeautifulSoup
from TruyenZ import *


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
			
def PareInput(args):
	inputpath = ''
	outputpath = ''
	try:
		opts, args = getopt.getopt(sys.argv[1:],"hi:o:",["ifile=","ofile="])
	except getopt.GetoptError:
		print( 'file.py -i <inputpath> -o <outputpath>')
		sys.exit(2)
	for opt, arg in opts:
		if opt == '-h':
			print ('file.py -i <inputpath> -o <outputpath>')
			sys.exit()
		elif opt in ("-i", "--ifile"):
			inputpath = arg
		elif opt in ("-o", "--ofile"):
			outputpath = arg


ScrawlWebManager.PushRelax("https://truyenz.info/manga/quyen-khi-luu-tinh/")
ScrawlWebManager.SetSavePath("D:\\")
ScrawlWebManager.FetchandSaveRelaxObject()
print ("Done")
#a = BeautifulSoup("<div class='adsf'></div>","lxml")
#print("class" in a.div.attrs)