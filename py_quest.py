# -*- coding: utf-8 -*-
import urllib
import traceback 

class PyQuest(object):
		def __init__(self,url):
				self._url = url

		def request(self,rtype,parama):
				try:
					params = urllib.urlencode(parama)
					if rtype == 'GET':
							
							f = urllib.urlopen(self._url+"?%s" % params)
					elif rtype == 'POST':
							f = urllib.urlopen(self._url, params)
					result = f.read()
					if result is not None:
							return result
 				except Exception,e:
					print e
					print traceback.format_exc()
		def strip_tags(self,html):
				"""
				Python remove all html tag
				    str_text=strip_tags("<font color=red>hello</font>")
				    print str_text
				    hello
				"""
				from HTMLParser import HTMLParser
				html = html.strip()
				html = html.strip("\n")
				result = []
				parser = HTMLParser()
				parser.handle_data = result.append
				parser.feed(html)
				parser.close()
				return ''.join(result)
