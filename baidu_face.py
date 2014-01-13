# -*- coding: utf-8 -*-
from py_quest import PyQuest
import time
import json
import string
import Image
import cStringIO
from mongoengine import *

db = MongoEngine()
class RedModel(db.Document):
		key = db.StringField()
		value = db.StringField()



class BaiduFace(object):
		def __init__(self):
				self.token = ''
				self.client_id='you api key'
				self.client_secret = 'you secret key'
				
				pass

		def oauth(self):
				red_time = RedModel.objects(key='baidu_face_accesstoken_time').first()
				red_token = RedModel.objects(key='baidu_face_accesstoken').first()

				if red_time is None or (time.time() > string.atof(red_time.value)):						
						url = "https://openapi.baidu.com/oauth/2.0/token"
						data = dict(grant_type='client_credentials',
												client_id=self.client_id,
												client_secret=self.client_secret 
												)		
						py_quest = PyQuest(url)		
						result = py_quest.request('GET',data)
						if result is not None:
								result = json.loads(result)
								access_token = result['access_token']
								
								
								if red_token or red_time is None:
										red_token = RedModel(key='baidu_face_accesstoken')
										red_time = RedModel(key='baidu_face_accesstoken_time')
										
								red_token.value = access_token
								
								red_time.value=str(time.time()+result['expires_in'])
								red_token.save()
								red_time.save()
								self.token = access_token
				else:
					self.token = red_token.value

		def face(self,pic_url):
				url = 'https://openapi.baidu.com/rest/2.0/media/v1/face/detect'
				data = dict(access_token=self.token,
												url=pic_url
												
												)	
				get_face = BaiduFaceTr(url,data)
				get_pic = BaiduFaceTr(pic_url,dict())
				get_face.start()
				get_pic.start()
				get_face.join()  
				get_pic.join()  
				file_str = get_pic.get_result()
				result = get_face.get_result()

				if result is not None:
						result = json.loads(result)

						face = result['face'][0]
						gender = face['attribute']['gender']
						smiling = face['attribute']['smiling']
						if (gender['confidence'] is not None) and (gender['value'] is not None):
								gender_str = gender['value']
						if (smiling['confidence'] is not None) and (gender['value'] is not None):
								smiling_str = 'you are happy'
						img_tr = ImageTr(file_str,result)
						img_tr.start()



						
						
		def test(self):
				test_url = 'http://www.hymn-idphoto.com/UploadFile/Photo/2012-9/2012092916265545378.jpg'
				
				self.oauth()
				
				self.face(test_url)



import threading
class BaiduFaceTr(threading.Thread): 
    def __init__(self, url,parama):  
        threading.Thread.__init__(self)  
        self.url = url
        self.parama = parama
        self.result = None
    def get_result(self):
    		return self.result
   
    def run(self):  
				py_quest = PyQuest(self.url)		
				self.result = py_quest.request('GET',self.parama)

class ImageTr(threading.Thread):
		def __init__(self,file_str,face_json):
				threading.Thread.__init__(self)  
				self.face_json = face_json
				self.file_str = file_str

		def run(self):
						result = self.face_json
						face = result['face'][0]
						tmpIm = cStringIO.StringIO(self.file_str)
						width = string.atof(result['img_width'])
						height = string.atof(result['img_height'])
						position = face['position']
						center_x = string.atof(position['center']['x'])*width
						center_y = string.atof(position['center']['y'])*height
						face_width = string.atof(position['width'])*width
						face_height = string.atof(position['height'])*height
						img = Image.open(tmpIm)
						region = (int(center_x-face_width/2-100),
											int(center_y-face_height/2-250),
											int(center_x+face_width/2+100),
											int(center_y+face_height/2+200))				
						cropImg = img.crop(region)
						cropImg.save('./static/'+result['img_id']+'.'+img.format)
				





				

