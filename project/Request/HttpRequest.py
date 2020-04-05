import requests

class HttpRequest:
	@staticmethod
	def GetHtmlData(url):
		r = requests.get(url)
		return r.text
