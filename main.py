import glob
import json
import os
import glob
import sys
import requests
import time
import matplotlib.pyplot as plt
from matplotlib.patches import Polygon
from PIL import Image
from io import BytesIO
def ocr(image_path):
	os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY'] = 'b080de7cbdda4fd6817e83e3fdf6706f'
	os.environ['COMPUTER_VISION_ENDPOINT'] = 'https://imagetotextey.cognitiveservices.azure.com/'

	missing_env = False
	# Add your Computer Vision subscription key and endpoint to your environment variables.
	if 'COMPUTER_VISION_ENDPOINT' in os.environ:
		endpoint = os.environ['COMPUTER_VISION_ENDPOINT']
	else:
		print("From Azure Cognitive Service, retrieve your endpoint and subscription key.")
		print("\nSet the COMPUTER_VISION_ENDPOINT environment variable, such as \"https://westus2.api.cognitive.microsoft.com\".\n")
		missing_env = True

	if 'COMPUTER_VISION_SUBSCRIPTION_KEY' in os.environ:
		subscription_key = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']
	else:
		print("From Azure Cognitive Service, retrieve your endpoint and subscription key.")
		print("\nSet the COMPUTER_VISION_SUBSCRIPTION_KEY environment variable, such as \"1234567890abcdef1234567890abcdef\".\n")
		missing_env = True

	if missing_env:
		print("**Restart your shell or IDE for changes to take effect.**")
		sys.exit()

	text_recognition_url = endpoint + "/vision/v3.1/read/analyze"

	image_data = open(image_path, "rb").read()

	headers = {'Ocp-Apim-Subscription-Key': subscription_key,'Content-Type': 'application/octet-stream'}
	response = requests.post(
		text_recognition_url, headers=headers, data=image_data)
	response.raise_for_status()
	# Holds the URI used to retrieve the recognized text.
	operation_url = response.headers["Operation-Location"]

	# The recognized text isn't immediately available, so poll to wait for completion.
	analysis = {}
	poll = True
	while (poll):
		response_final = requests.get(
			response.headers["Operation-Location"], headers=headers)
		analysis = response_final.json()

		time.sleep(1)
		if ("analyzeResult" in analysis):
			poll = False
		if ("status" in analysis and analysis['status'] == 'failed'):
			poll = False

		with open('file.doc', 'a') as f:
			print("**********************", file=f)
	if ("analyzeResult" in analysis):
		polygons = ((line['text'])for line in analysis["analyzeResult"]["readResults"][0]["lines"])
		for line in polygons:
			result = line.split("\n")
			res= ""
			for i in result:
				res+=i 
			with open('file.doc', 'a') as f:
				print(res, file=f)
	return




def alltojpg(mainfilename):
	import ntpath
	ntpath.basename("a/b/c")
	head, tail = ntpath.split(mainfilename)
	print(tail)
	print(head)
	if mainfilename.endswith('.pdf'):
		from wand.image import Image
		f = mainfilename
		with(Image(filename=f, resolution=300)) as source: 
			for i, image in enumerate(source.sequence):
				newfilename = head + str(i + 1) + '.jpeg'
				Image(image).save(filename=newfilename)
				ocr(newfilename)
	elif mainfilename.endswith('.ppt'):
		from wand.image import Image
		f = mainfilename
		with(Image(filename=f, resolution=300)) as source: 
			for i, image in enumerate(source.sequence):
				newfilename = head + str(i + 1) + '.jpeg'
				Image(image).save(filename=newfilename)
				ocr(newfilename)
	elif mainfilename.endswith('.doc'):
		from wand.image import Image
		f = mainfilename	
		with(Image(filename=f, resolution=300)) as source: 
			for i, image in enumerate(source.sequence):
				newfilename = head + str(i + 1) + '.jpeg'
				Image(image).save(filename=newfilename)
				ocr(newfilename)
	elif mainfilename.endswith('.docx'):
		from wand.image import Image
		f = mainfilename
		with(Image(filename=f, resolution=300)) as source: 
			for i, image in enumerate(source.sequence):
				newfilename = head + str(i + 1) + '.jpeg'
				Image(image).save(filename=newfilename)
				ocr(newfilename)
	elif mainfilename.endswith('.png'):
		from PIL import Image
		im = Image.open(mainfilename)
		rgb_im = im.convert('RGB')
		rgb_im.save(head+'/'+'tail.jpg')
		ocr(head+'/'+'tail.jpg')
	elif mainfilename.endswith('.jpg'):
		ocr(mainfilename)
	elif mainfilename.endswith('.jpeg'):
		ocr(mainfilename)

def alltoexcel(mainfilename):
	import ntpath
	ntpath.basename("a/b/c")
	head, tail = ntpath.split(mainfilename)
	print(tail)
	print(head)
	if mainfilename.endswith('.pdf'):
		from wand.image import Image
		f = mainfilename
		with(Image(filename=f, resolution=300)) as source: 
			for i, image in enumerate(source.sequence):
				newfilename = head + str(i + 1) + '.jpg'
				Image(image).save(filename=newfilename)
		return newfilename
	elif mainfilename.endswith('.ppt'):
		from wand.image import Image
		f = mainfilename
		with(Image(filename=f, resolution=300)) as source: 
			for i, image in enumerate(source.sequence):
				newfilename = head + str(i + 1) + '.jpg'
				Image(image).save(filename=newfilename)
		return newfilename
	elif mainfilename.endswith('.doc'):
		from wand.image import Image
		f = mainfilename
		with(Image(filename=f, resolution=300)) as source: 
			for i, image in enumerate(source.sequence):
				newfilename = head + str(i + 1) + '.jpg'
				Image(image).save(filename=newfilename)
		return newfilename
	elif mainfilename.endswith('.docx'):
		from wand.image import Image
		f = mainfilename
		with(Image(filename=f, resolution=300)) as source: 
			for i, image in enumerate(source.sequence):
				newfilename = head + str(i + 1) + '.jpg'
				Image(image).save(filename=newfilename)
		return newfilename
	elif mainfilename.endswith('.png'):
		from PIL import Image
		im = Image.open(mainfilename)
		rgb_im = im.convert('RGB')
		rgb_im.save(head+'/'+'tail.jpg')
		return head+'/'+'tail.jpg'
	elif mainfilename.endswith('.jpg'):
		return mainfilename
	elif mainfilename.endswith('.jpeg'):
		return mainfilename

def convertndocr(doc_path):
	open('file.doc', "w").close()
	alltojpg(doc_path)

def deletedir():
	files = glob.glob('/tempwand/*')
	for f in files:
	    os.remove(f)