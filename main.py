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
from xlutils.copy import copy    
from xlrd import open_workbook
import xlsxwriter
import detect3
import cv2
import numpy as np

def preproces_image(
	image,
	*,
	kernel_size=15,
	crop_side=50,
	blocksize=35,
	constant=15,
	max_value=255,
):
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	bit = cv2.bitwise_not(gray)
	image_adapted = cv2.adaptiveThreshold(
		src=bit,
		maxValue=max_value,
		adaptiveMethod=cv2.ADAPTIVE_THRESH_MEAN_C,
		thresholdType=cv2.THRESH_BINARY,
		blockSize=blocksize,
		C=constant,
	)
	kernel = np.ones((kernel_size, kernel_size), np.uint8)
	erosion = cv2.erode(image_adapted, kernel, iterations=2)
	return erosion[crop_side:-crop_side, crop_side:-crop_side]

def find_edges(image_preprocessed, *, bw_threshold=150, limits=(0.09, 0.08)):
	mask = image_preprocessed < bw_threshold
	edges = []
	for axis in (1, 0):
		count = mask.sum(axis=axis)
		limit = limits[axis] * image_preprocessed.shape[axis]
		index_ = np.where(count >= limit)
		_min, _max = index_[0][0], index_[0][-1]
		edges.append((_min, _max))
	return edges


def adapt_edges(edges, *, height, width):
	(x_min, x_max), (y_min, y_max) = edges
	x_min2 = x_min
	x_max2 = x_max + min(250, (height - x_max) * 10 // 11)
	# could do with less magic numbers
	y_min2 = max(0, y_min)
	y_max2 = y_max + min(250, (width - y_max) * 10 // 11)
	return (x_min2, x_max2), (y_min2, y_max2)



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



#function to convert all file formats to jpg image file.
def alltojpg(mainfilename):
	import ntpath
	ntpath.basename("a/b/c")
	head, tail = ntpath.split(mainfilename)
	print(tail)
	print(head)
	#file is in pdf format
	if mainfilename.endswith('.pdf'):
		from wand.image import Image
		f = mainfilename
		with(Image(filename=f, resolution=300)) as source: 
			for i, image in enumerate(source.sequence):
				newfilename = head + str(i + 1) + '.jpeg'
				Image(image).save(filename=newfilename)
				ocr(newfilename)
	#file is in ppt format
	elif mainfilename.endswith('.ppt'):
		from wand.image import Image
		f = mainfilename
		with(Image(filename=f, resolution=300)) as source: 
			for i, image in enumerate(source.sequence):
				newfilename = head + str(i + 1) + '.jpeg'
				Image(image).save(filename=newfilename)
				ocr(newfilename)
	#file is in doc format
	elif mainfilename.endswith('.doc'):
		from wand.image import Image
		f = mainfilename	
		with(Image(filename=f, resolution=300)) as source: 
			for i, image in enumerate(source.sequence):
				newfilename = head + str(i + 1) + '.jpeg'
				Image(image).save(filename=newfilename)
				ocr(newfilename)
	#file is in docx format
	elif mainfilename.endswith('.docx'):
		from wand.image import Image
		f = mainfilename
		with(Image(filename=f, resolution=300)) as source: 
			for i, image in enumerate(source.sequence):
				newfilename = head + str(i + 1) + '.jpeg'
				Image(image).save(filename=newfilename)
				ocr(newfilename)
	#file is in png format
	elif mainfilename.endswith('.png'):
		from PIL import Image
		im = Image.open(mainfilename)
		rgb_im = im.convert('RGB')
		rgb_im.save(head+'/'+'tail.jpg')
		ocr(head+'/'+'tail.jpg')
	#file is in jpg format so will pass the same forward
	elif mainfilename.endswith('.jpg'):
		ocr(mainfilename)
	#file is in jpeg format so will pass the same forward
	elif mainfilename.endswith('.jpeg'):
		ocr(mainfilename)

#function to convert every top to down organizational chart in any file format to excel
def alltoexcel(mainfilename):
	workbook = xlsxwriter.Workbook('graph.xls')
	# sheet = workbook.add_worksheet("Org_Chart-1")
	# workbook.close()
	import ntpath
	ntpath.basename("a/b/c")
	head, tail = ntpath.split(mainfilename)
	print(tail)
	print(head)
	if mainfilename.endswith('.pdf'):
		from wand.image import Image
		f = mainfilename
		with(Image(filename=f, resolution=300)) as source:
			count=0
			for i, image in enumerate(source.sequence):
				count=count+1
				newfilename = head + str(i + 1) + '.jpg'
				Image(image).save(filename=newfilename)
				filename_in = newfilename
				filename_out = newfilename
				image = cv2.imread(str(filename_in))
				height, width = image.shape[0:2]
				image_preprocessed = preproces_image(image)
				edges = find_edges(image_preprocessed)
				(x_min, x_max), (y_min, y_max) = adapt_edges(
					edges, height=height, width=width
				)
				image_cropped = image[x_min:x_max, y_min:y_max]
				cv2.imwrite(str(filename_out), image_cropped)
				detect3.detectshapescs2(newfilename,"Org_Chart-"+str(count),workbook)
			workbook.close()
		return newfilename
	elif mainfilename.endswith('.ppt'):
		from wand.image import Image
		f = mainfilename
		with(Image(filename=f, resolution=300)) as source:
			count=0 
			for i, image in enumerate(source.sequence):
				count=count+1
				newfilename = head + str(i + 1) + '.jpg'
				Image(image).save(filename=newfilename)
				filename_in = newfilename
				filename_out = newfilename
				image = cv2.imread(str(filename_in))
				height, width = image.shape[0:2]
				image_preprocessed = preproces_image(image)
				edges = find_edges(image_preprocessed)
				(x_min, x_max), (y_min, y_max) = adapt_edges(
					edges, height=height, width=width
				)
				image_cropped = image[x_min:x_max, y_min:y_max]
				cv2.imwrite(str(filename_out), image_cropped)
				detect3.detectshapescs2(newfilename,"Org_Chart-"+str(count),workbook)
			workbook.close()
		return newfilename
	elif mainfilename.endswith('.doc'):
		from wand.image import Image
		f = mainfilename
		with(Image(filename=f, resolution=300)) as source:
			count=0 
			for i, image in enumerate(source.sequence):
				count=count+1
				newfilename = head + str(i + 1) + '.jpg'
				Image(image).save(filename=newfilename)
				filename_in = newfilename
				filename_out = newfilename
				image = cv2.imread(str(filename_in))
				height, width = image.shape[0:2]
				image_preprocessed = preproces_image(image)
				edges = find_edges(image_preprocessed)
				(x_min, x_max), (y_min, y_max) = adapt_edges(
					edges, height=height, width=width
				)
				image_cropped = image[x_min:x_max, y_min:y_max]
				cv2.imwrite(str(filename_out), image_cropped)
				detect3.detectshapescs2(newfilename,"Org_Chart-"+str(count),workbook)
			workbook.close()
		return newfilename
	elif mainfilename.endswith('.docx'):
		from wand.image import Image
		f = mainfilename
		with(Image(filename=f, resolution=300)) as source: 
			count=0
			for i, image in enumerate(source.sequence):
				count=count+1
				newfilename = head + str(i + 1) + '.jpg'
				Image(image).save(filename=newfilename)
				filename_in = newfilename
				filename_out = newfilename
				image = cv2.imread(str(filename_in))
				height, width = image.shape[0:2]
				image_preprocessed = preproces_image(image)
				edges = find_edges(image_preprocessed)
				(x_min, x_max), (y_min, y_max) = adapt_edges(
					edges, height=height, width=width
				)
				image_cropped = image[x_min:x_max, y_min:y_max]
				cv2.imwrite(str(filename_out), image_cropped)
				detect3.detectshapescs2(newfilename,"Org_Chart-"+str(count),workbook)
			workbook.close()
		return newfilename
	elif mainfilename.endswith('.png'):
		from PIL import Image
		im = Image.open(mainfilename)
		rgb_im = im.convert('RGB')
		rgb_im.save(head+'/'+'tail.jpg')
		newfile=head+'/'+'tail.jpg'
		detect3.detectshapescs2(newfile,"Org_Chart-"+str(1),workbook)
		workbook.close()
		return head+'/'+'tail.jpg',
	elif mainfilename.endswith('.jpg'):
		detect3.detectshapescs2(mainfilename,"Org_Chart-"+str(1),workbook)
		workbook.close()
		return mainfilename
	elif mainfilename.endswith('.jpeg'):
		detect3.detectshapescs2(mainfilename,"Org_Chart-"+str(1),workbook)
		workbook.close()
		return mainfilename

#function to convert every top to down organizational chart in any file format to excel
def alltoexcel_lr(mainfilename):
	workbook = xlsxwriter.Workbook('graph.xls')
	# sheet = workbook.add_worksheet("Org_Chart-1")
	# workbook.close()
	import ntpath
	ntpath.basename("a/b/c")
	head, tail = ntpath.split(mainfilename)
	print(tail)
	print(head)
	if mainfilename.endswith('.pdf'):
		from wand.image import Image
		f = mainfilename
		with(Image(filename=f, resolution=300)) as source:
			count=0
			for i, image in enumerate(source.sequence):
				count=count+1
				newfilename = head + str(i + 1) + '.jpg'
				Image(image).save(filename=newfilename)
				detect3.detectshapescs2_lr(newfilename,"Org_Chart-"+str(count),workbook)
			workbook.close()
		return newfilename
	elif mainfilename.endswith('.ppt'):
		from wand.image import Image
		f = mainfilename
		with(Image(filename=f, resolution=300)) as source:
			count=0 
			for i, image in enumerate(source.sequence):
				count=count+1
				newfilename = head + str(i + 1) + '.jpg'
				Image(image).save(filename=newfilename)
				detect3.detectshapescs2_lr(newfilename,"Org_Chart-"+str(count),workbook)
			workbook.close()
		return newfilename
	elif mainfilename.endswith('.doc'):
		from wand.image import Image
		f = mainfilename
		with(Image(filename=f, resolution=300)) as source:
			count=0 
			for i, image in enumerate(source.sequence):
				count=count+1
				newfilename = head + str(i + 1) + '.jpg'
				Image(image).save(filename=newfilename)
				detect3.detectshapescs2_lr(newfilename,"Org_Chart-"+str(count),workbook)
			workbook.close()
		return newfilename
	elif mainfilename.endswith('.docx'):
		from wand.image import Image
		f = mainfilename
		with(Image(filename=f, resolution=300)) as source: 
			count=0
			for i, image in enumerate(source.sequence):
				count=count+1
				newfilename = head + str(i + 1) + '.jpg'
				Image(image).save(filename=newfilename)
				detect3.detectshapescs2_lr(newfilename,"Org_Chart-"+str(count),workbook)
			workbook.close()
		return newfilename
	elif mainfilename.endswith('.png'):
		from PIL import Image
		im = Image.open(mainfilename)
		rgb_im = im.convert('RGB')
		rgb_im.save(head+'/'+'tail.jpg')
		newfile=head+'/'+'tail.jpg'
		detect3.detectshapescs2_lr(newfile,"Org_Chart-"+str(1),workbook)
		workbook.close()
		return head+'/'+'tail.jpg',
	elif mainfilename.endswith('.jpg'):
		detect3.detectshapescs2_lr(mainfilename,"Org_Chart-"+str(1),workbook)
		workbook.close()
		return mainfilename
	elif mainfilename.endswith('.jpeg'):
		detect3.detectshapescs2_lr(mainfilename,"Org_Chart-"+str(1),workbook)
		workbook.close()
		return mainfilename

#function to convert any file into editable document
def convertndocr(doc_path):
	open('file.doc', "w").close()
	alltojpg(doc_path)

#function to delete the temporary files stored in the database
def deletedir():
	files = glob.glob('/tempwand/*')
	for f in files:
		os.remove(f)
