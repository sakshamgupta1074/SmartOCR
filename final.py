from PIL import Image, ImageDraw
from skimage.morphology import skeletonize
from skimage import data
from skimage import morphology, filters
import sknw
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import networkx as nx
from skimage.measure import approximate_polygon
from xlutils.copy import copy    
from xlrd import open_workbook
import xlsxwriter
import cv2
from collections import defaultdict
import os
import sys
import requests
import time
from matplotlib.patches import Polygon
from PIL import Image
from io import BytesIO
import io
import re
import json
from shapely.geometry import Polygon
import matplotlib
from geopy.geocoders import Nominatim
from shapely.geometry import Polygon
node_levels=[]
fin=[]
te={}
cord_dic=[]
count=0
geolocator = Nominatim(timeout=3,user_agent="Shivasapp")
def color(path_original,cor):
	image = cv2.imread(path_original)
	for dic in cor:
		x0=float(dic[0])
		y0=float(dic[1])
		x1=float(dic[2])
		y1=float(dic[3])
		alpha = 1 # that's your transparency factor
		polygon = Polygon([(x0, y0), (x0, y1), (x1, y1), (x1, y0)])
		int_coords = lambda x: np.array(x).round().astype(np.int32)
		exterior = [int_coords(polygon.exterior.coords)]
		overlay = image.copy()
		cv2.fillPoly(overlay, exterior, color=(0, 0, 0))
		cv2.addWeighted(overlay, alpha, image, 1 - alpha, 0, image)
		cv2.imwrite('colored_black.jpg', image)
		return 'colored_black.jpg'

#Function to convert org chart to excel	
def toexcel(path_original,cor):

	path_black=color(path_original,cor)
	image = cv2.imread(path_original)
	workbook = xlsxwriter.Workbook('graph.xls')
	worksheet = workbook.add_worksheet()
	workbook.close()
	count,node_levels,ps,g,te= sknw_main(path_black,cor)
	book_ro = open_workbook("graph.xls")
	book = copy(book_ro)  # creates a writeable copy
	sheet = book.get_sheet(0)  # get a first sheet
	sheet.write(0,0,'ID')
	sheet.write(0,1,'Child')
	sheet.write(0,2,'Immediate Parent')
	sheet.write(0,5,'Shape Percentage')
	sheet.write(0,4,'Shapes')
	sheet.write(0,6,'City')
	sheet.write(0,7,'Country')
	sheet.write(0,3,'Own Percentage')
	idd='UID1'
	row=2
	te=np.array(te)
	te=te.tolist()
	result,prec,shape=textt(te[ps.index(node_levels[0][0])],ps.index(node_levels[0][0]),path_original)
	sem = result
	res=result
	kk=res
	per= re.findall('\d*%',kk)
	if per:
		res=re.sub(r'\d*%'," ",kk)
	else:
		per='100%'
	city = re.search('\(([^)]+)', sem)

	if city:
		city=city.group(1)
		res=re.sub("[\(\[].*?[\)\]]", "", sem)
		try:
			city,w=citycountname(city)
		except: 
			city=''
			w=''
		start = sem.find( '(' )
		if start != -1:
			res = sem[0:start-1]
	else:
		city =' '
		w = ' '
	prec=round(float(prec),2)
	prec=str(prec)+'%'
	sheet.write(1,1,res)
	sheet.write(1,0,idd)
	sheet.write(1,5,prec)
	sheet.write(1,4,shape)
	sheet.write(1,6,city)
	sheet.write(1,7,w)
	sheet.write(1,3,'')
	for i in range(count):
		coloring(i,node_levels,image,path_original,cor)
		node_levels,ps,g,te= sknw_loop(cor)
		for j in range(len(node_levels[i])):

			flag=0
			for k in range(len(node_levels[i+1])):
				source=ps.index(node_levels[i][j])
				destination=int(ps.index(node_levels[i+1][k]))
	
				if nx.has_path(g,source,destination):
					result,prec,shape=textt(te[source],source,path_original)
					sem = result
					res=result
					city = re.search('\(([^)]+)', sem)

					if city:
						city=city.group(1)
						res=re.sub("[\(\[].*?[\)\]]", "", sem)
						start = sem.find( '(' )
						if start != -1:
							res = sem[0:start-1]					
					else:
						city =' '
						w = ' '

					kk=res
					per= re.findall('\d*%',kk)
					if per:
						res=re.sub(r'\d*%'," ",kk)
					else:
						per='100%'
					sheet.write(row,2,res)

					result,prec,shape=textt(te[destination],destination,path_original)
					sem = result
					res=result
					kk=res
					per= re.findall('\d*%',kk)
					if per:
						res=re.sub(r'\d*%'," ",kk)
					else:
						per='100%'
					city = re.search('\(([^)]+)', sem)

					if city:
						city=city.group(1)
						res=re.sub("[\(\[].*?[\)\]]", "", sem)
						try:
							city,w=citycountname(city)
						except:
							continue
							city=''
							w=''
						start = sem.find( '(' )
						if start != -1:
							res = sem[0:start-1]
					else:
						city =' '
						w = ' '
					prec=round(float(prec),2)
					prec=str(prec)+'%'	
					idd='UID'+str(row)
					sheet.write(row,0,idd)
					sheet.write(row,1,res)
					sheet.write(row,5,prec)
					sheet.write(row,4,shape)
					sheet.write(row,6,city)
					sheet.write(row,7,w)
					sheet.write(row,3,per)
					row=row+1
					flag=1
			if flag==0:
				for l in range(len(node_levels[i+2])):
					source=ps.index(node_levels[i][j])
					try:
						destination=int(ps.index(node_levels[i+2][l]))
						if nx.has_path(g,source,destination):
							result,prec,shape=textt(te[source],source,path_original)
							sem = result
							res=result
							city = re.search('\(([^)]+)', sem)

							if city:
								city=city.group(1)
								res=re.sub("[\(\[].*?[\)\]]", "", sem)
								start = sem.find( '(' )
								if start != -1:
									res = sem[0:start-1]
							else:
								city =' '
								w = ' '
							kk=res
							per= re.findall('\d*%',kk)
							if per:
								res=re.sub(r'\d*%'," ",kk)
							else:
								per='100%'
							sheet.write(row,2,res)

							result,prec,shape=textt(te[destination],destination,path_original)
							sem = result
							res=result
							city = re.search('\(([^)]+)', sem)
							kk=res
							per= re.findall('\d*%',kk)
							if per:
								res=re.sub(r'\d*%'," ",kk)
							else:
								per='100%'
							if city:
								city=city.group(1)
								res=re.sub("[\(\[].*?[\)\]]", "", sem)
								try:
									city,w=citycountname(city)
								except :
									continue
									city=''
									w=''
								start = sem.find( '(' )
								if start != -1:
									res = sem[0:start-1]
							else:
								city =' '
								w = ' '

							prec=round(float(prec),2)
							prec=str(prec)+'%'
							idd='UID'+str(row)
							sheet.write(row,0,idd)
							sheet.write(row,1,res)
							sheet.write(row,5,prec)
							sheet.write(row,4,shape)
							sheet.write(row,6,city)
							sheet.write(row,7,w)
							sheet.write(row,3,per)

							row=row+1						# sheet.write(row,0,result)
					except :
						continue

	book.save("graph.xls")

#Function to find city and country
def citycountname(cityname):
	location = geolocator.geocode(cityname,language='en')
	loc_dict = location.raw
	sub=','
	if sub in loc_dict['display_name']:
		return (cityname,loc_dict['display_name'].rsplit(', ' , 1)[1])
	else:
		return (' ',loc_dict['display_name'].rsplit(',' , 1)[0])

#Function to color levels
def coloring(xii,node_levelsii,imageii,path_black,coordinates):
	height, width = imageii.shape[:2]
	x0=0
	try:
		x1=node_levelsii[xii][0][0]-20
	except:
		x1=0
	y0=0
	y1=width
	
	im = Image.open(path_black)
	draw = ImageDraw.Draw(im)
	draw.rectangle((y0,x0,y1,x1), fill=(255,255,255), outline=(255,255,255))
	im.save('imagedraw.jpg')
	path='imagedraw.jpg'
	fillbox(path,'imagedraw.jpg',coordinates)

#Function to draw main graph
def sknw_main(path_black,cor):
	image  = cv2.imread(path_black,0)
	ret,img = cv2.threshold(image, 0, 255,cv2.THRESH_OTSU)
	binary = img > filters.threshold_otsu(img)
	ske = skeletonize(~binary).astype(np.uint16)

	# build graph from skeleton
	graph = sknw.build_sknw(ske)


	# draw edges by pts
	for (s,e) in graph.edges():
	    ps = graph[s][e]['pts']
	    plt.plot(ps[:,1], ps[:,0], 'blue')
	cord=graph.edges
	# draw node by o
	nodes = graph.nodes()
	ps = np.array([nodes[i]['o'] for i in nodes])
	plt.plot(ps[:,1], ps[:,0], 'r.')

	#to find nodes between entities
	def FindPoint(x1, y1, x2, y2, x, y): 
	    if (x > y1 and x < y2 and y > x1 and y < x2): 
	    	
	    	return True
	    else :
	    	
	    	return False


	fin=[]
    #to store parent entity
	def parent_entity(dic,ps,cor):
		ps=np.array(ps)
		ps=ps.tolist()
		x1=int(dic[0])
		y1=int(dic[1])
		x2=int(dic[2])
		y2=int(dic[3])
		count=0
		i=[]
		for i in ps:
			x=(i[0])
			y=(i[1])
			if FindPoint(x1,y1,x2,y2,x,y):
				fin.append(i)
				cord_dic.append(dic)
				a=[x,y]
				te.update({(ps.index(a)): dic})
				break;
	  
	ps = np.array(ps)
	for dic in cor:
		parent_entity(dic,ps,cor)
	fin=np.array(fin)
	fina=fin.tolist()
	ps=np.array(ps)
	ps=ps.tolist()
	final_nodes=fina
	final_nodes.sort()
	lengthy = len(final_nodes)
	node_levels = [[] for i in range(lengthy)]
	node_levels[0].append(final_nodes[0])
	node_val = [[]for i in range(lengthy)]
	node_val[0].append(ps.index(final_nodes[0]))
	a=0
	for i in range(1,lengthy):
		if ((abs(final_nodes[i][0] - final_nodes[i-1][0]))<=10):
			node_levels[a].append(final_nodes[i])
			node_val[a].append(ps.index(final_nodes[i]))
		else:
			a=a+1
			node_levels[a].append(final_nodes[i])
			node_val[a].append(ps.index(final_nodes[i]))
	g = nx.Graph(graph.edges)
	gi = nx.to_directed(graph)
	j=[]
	index=[]
	for j in fina:
		index.append(ps.index(j))
	index.sort()
	count=0
	for i in node_levels:
		if len(i)==0:
			continue
		else:
			count=count+1
	return count,node_levels,ps,g,te

#to draw level graphs
def sknw_loop(cor):
	image  = cv2.imread('imagedraw.jpg',0)
	ret,img = cv2.threshold(image, 0, 255,cv2.THRESH_OTSU)
	binary = img > filters.threshold_otsu(img)
	ske = skeletonize(~binary).astype(np.uint16)

	# build graph from skeleton
	graph = sknw.build_sknw(ske)
	# draw image
	# draw edges by pts
	for (s,e) in graph.edges():
	    ps = graph[s][e]['pts']
	    plt.plot(ps[:,1], ps[:,0], 'blue')
	cord=graph.edges
	# draw node by o
	nodes = graph.nodes()
	ps = np.array([nodes[i]['o'] for i in nodes])
	def FindPoint(x1, y1, x2, y2, x, y): 
	    if (x >= y1 and x <= y2 and y >= x1 and y <= x2): 
	    	return True
	    else :
	    	
	    	return False


	fin=[]
	def parent_entity(dic,ps,cor):
		ps=np.array(ps)
		ps=ps.tolist()
		x1=float(dic[0])
		y1=float(dic[1])
		x2=float(dic[2])
		y2=float(dic[3])
		count=0
		i=[]
		for i in ps:
			x=(i[0])
			y=(i[1])

			if FindPoint(x1,y1,x2,y2,x,y):

				fin.append(i)
				cord_dic.append(dic)
				a=[x,y]
				te.update({(ps.index(a)): dic})
				break;
	  
	cor = np.array(cor)
	ps = np.array(ps)
	for dic in cor:
		parent_entity(dic,ps,cor)
	fin=np.array(fin)
	fina=fin.tolist()
	ps=np.array(ps)
	ps=ps.tolist()
	final_nodes=fina
	final_nodes.sort()
	lengthy = len(final_nodes)
	node_levels = [[] for i in range(lengthy)]
	node_levels[0].append(final_nodes[0])
	node_val = [[]for i in range(lengthy)]
	node_val[0].append(ps.index(final_nodes[0]))
	a=0
	for i in range(1,lengthy):
		if ((final_nodes[i][0] - final_nodes[i-1][0])<=10):
			node_levels[a].append(final_nodes[i])
			node_val[a].append(ps.index(final_nodes[i]))
		else:
			a=a+1
			node_levels[a].append(final_nodes[i])
			node_val[a].append(ps.index(final_nodes[i]))
	g = nx.Graph(graph.edges)
	gi = nx.to_directed(graph)
	j=[]
	index=[]
	for j in fina:
		index.append(ps.index(j))

	res = {index[i]: cord_dic[i] for i in range(len(index))} 
	index.sort()

	return node_levels,ps,g,te

#to fill shapes to draw graph
def fillbox(path,thresh_image,coordinates):
	
	image = cv2.imread(path, 0) 
	for i in range(len(coordinates)):
		start_point=(coordinates[i][0],coordinates[i][1])
		end_point=(coordinates[i][2],coordinates[i][3])
		color = (0, 0, 0) 
		thickness = -1
		image = cv2.rectangle(image, start_point, end_point, color, thickness) 
	cv2.imwrite(thresh_image,image)


#to ocr the text in image
def textt(dic,n,image_path):
	x1=float(dic[0])
	y1=float(dic[1])
	x2=float(dic[2])
	y2=float(dic[3])
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
	    return res,prec,shape

# cor=[[156, 274, 316, 325, 97.36135005950928, 'rectangle'], [355, 275, 516, 325, 97.23899364471436, 'rectangle'], [562, 99, 719, 149, 97.17506170272827, 'rectangle'], [382, 99, 542, 149, 96.84385061264038, 'rectangle'], [23, 99, 183, 148, 96.81214690208435, 'rectangle'], [442, 457, 602, 507, 96.20250463485718, 'rectangle'], [179, 186, 338, 237, 95.3770399093628, 'rectangle'], [4, 187, 166, 237, 94.89936828613281, 'rectangle'], [278, 362, 439, 414, 94.42919492721558, 'rectangle'], [74, 363, 234, 415, 94.10572648048401, 'rectangle'], [280, 9, 441, 61, 92.82688498497009, 'rectangle'], [112, 455, 194, 516, 68.0224359035492, 'circle'], [265, 99, 345, 157, 67.23973751068115, 'circle'], [43, 274, 123, 335, 54.711222648620605, 'pentagon'], [584, 188, 692, 252, 52.483564615249634, 'triangle'], [482, 364, 561, 428, 40.776342153549194, 'pentagon']]
# path_original='ey3.jpg'
# toexcel(path_original,cor)


