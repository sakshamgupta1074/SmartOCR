import re
from xlutils.copy import copy    
from xlrd import open_workbook
import xlsxwriter
import json
import os
import sys
import requests
import time
from matplotlib.patches import Polygon
from PIL import Image
from io import BytesIO
import io

def ocr_excel(cordinates,image_path):
	
	

	# Create a workbook and add a worksheet.
	workbook = xlsxwriter.Workbook('test.xls')
	worksheet = workbook.add_worksheet()
	workbook.close()
	import numpy as np
	row=1
	column=1
	arr = np.array(cordinates)
	for dic in arr:
		cropocr(dic,row,column,image_path)
		row=row+1

def cropocr(dic,row,column,image_path):
	from PIL import Image
	x1=int(dic[0])
	y1=int(dic[1])
	x2=int(dic[2])
	y2=int(dic[3])
	prec=dic[4]
	shape=dic[5]
	img = Image.open(image_path)
	img2 = img.crop((x1,y1,x2,y2))
	img2.save("temp.jpg")

	

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

	image_path = "temp.jpg"
	im = Image.open(image_path)  
	newsize = (200, 200) 
	image_path = im.resize(newsize)
	
	img_byte_arr = io.BytesIO()
	image_path.save(img_byte_arr,format='JPEG')
	image_data = img_byte_arr.getvalue()
	headers = {'Ocp-Apim-Subscription-Key': subscription_key,'Content-Type': 'application/octet-stream'}
	response = requests.post(
	    text_recognition_url, headers=headers, data=image_data)
	response.raise_for_status()
	operation_url = response.headers["Operation-Location"]

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
	temp=[]
	open('file.doc', "w").close()
	if ("analyzeResult" in analysis):

	    polygons = ((line['text'])
	                for line in analysis["analyzeResult"]["readResults"][0]["lines"])
	    for line in polygons:
	        result = line.split("\n")
	        res= ""
	        for i in result:
	            res+=i
	            temp.append(res) 

	    res = ' '.join(str(e) for e in temp)

	    s = res
	    m = re.search('\(([^)]+)', s)
	    if m:
	    	m=m.group(1)
	    	res=re.sub("[\(\[].*?[\)\]]", "", s)
	    k=res
	    l= re.findall('\d*%',k)
	    if l:
	    	res=re.sub(r'\d*%'," ",k)
	    else:
	    	l='100%'


# importing xlwt module 


	book_ro = open_workbook("test.xls")
	book = copy(book_ro)  # creates a writeable copy
	sheet1 = book.get_sheet(0)  # get a first sheet
	sheet1.write(0,0,'ID')
	sheet1.write(0,1,'Child')
	sheet1.write(0,2,'Percentage')
	sheet1.write(0,3,'Shapes')
	sheet1.write(0,4,'City/Country')
	sheet1.write(0,5,'Own Percentage')

	sheet1.write(row,0,row)
	sheet1.write(row,1,res)
	sheet1.write(row,2,prec)
	sheet1.write(row,3,shape)
	sheet1.write(row,4,m)
	sheet1.write(row,5,l)

	book.save("test.xls")
