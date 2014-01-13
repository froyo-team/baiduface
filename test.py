# -*- coding: utf-8 -*-
from baidu_face import BaiduFace
from mongoengine import * 

def connect_db():
		connect('database') 

def main():
		connect_db()
		baidu_face = BaiduFace()
		baidu_face.test()

if __name__ == '__main__':
	main()