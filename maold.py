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

geolocator = Nominatim(timeout=3,user_agent="Shivasapp")
# matplotlib.use('TkAgg')
cor=[[156, 274, 316, 325, 97.36135005950928, 'rectangle'], [355, 275, 516, 325, 97.23899364471436, 'rectangle'], [562, 99, 719, 149, 97.17506170272827, 'rectangle'], [382, 99, 542, 149, 96.84385061264038, 'rectangle'], [23, 99, 183, 148, 96.81214690208435, 'rectangle'], [442, 457, 602, 507, 96.20250463485718, 'rectangle'], [179, 186, 338, 237, 95.3770399093628, 'rectangle'], [4, 187, 166, 237, 94.89936828613281, 'rectangle'], [278, 362, 439, 414, 94.42919492721558, 'rectangle'], [74, 363, 234, 415, 94.10572648048401, 'rectangle'], [280, 9, 441, 61, 92.82688498497009, 'rectangle'], [112, 455, 194, 516, 68.0224359035492, 'circle'], [265, 99, 345, 157, 67.23973751068115, 'circle'], [43, 274, 123, 335, 54.711222648620605, 'pentagon'], [584, 188, 692, 252, 52.483564615249634, 'triangle'], [482, 364, 561, 428, 40.776342153549194, 'pentagon']]
cor2=[[1044, 687, 1199, 844, 98.51794838905334, 'rectangle'], [1023, 161, 1412, 398, 98.42606782913208, 'rectangle'], [1608, 688, 1765, 843, 98.40973615646362, 'rectangle'], [1606, 1135, 1764, 1293, 98.3725368976593, 'rectangle'], [1609, 1363, 1764, 1523, 98.32055568695068, 'rectangle'], [1608, 914, 1763, 1068, 98.26047420501709, 'rectangle'], [1419, 686, 1573, 844, 98.19836616516113, 'rectangle'], [1234, 686, 1386, 844, 98.08623790740967, 'rectangle'], [291, 686, 443, 848, 98.0351448059082, 'rectangle'], [668, 463, 823, 618, 97.92945384979248, 'rectangle'], [1794, 914, 1950, 1069, 97.85811305046082, 'rectangle'], [292, 917, 448, 1069, 97.8340744972229, 'rectangle'], [857, 688, 1006, 845, 97.83082008361816, 'rectangle'], [483, 463, 633, 618, 97.76562452316284, 'rectangle'], [1233, 463, 1389, 619, 97.72863984107971, 'rectangle'], [1044, 463, 1198, 616, 97.69213199615479, 'rectangle'], [1417, 1360, 1573, 1520, 97.63452410697937, 'rectangle'], [858, 463, 1006, 619, 97.62102961540222, 'rectangle'], [1417, 913, 1573, 1068, 97.54629135131836, 'rectangle'], [293, 464, 447, 620, 97.45721817016602, 'rectangle'], [1982, 914, 2139, 1070, 97.31693267822266, 'rectangle'], [100, 461, 256, 618, 97.10217714309692, 'rectangle'], [106, 913, 260, 1071, 97.03575372695923, 'rectangle'], [1425, 463, 1572, 618, 96.99065089225769, 'rectangle'], [1987, 462, 2134, 619, 96.98861837387085, 'rectangle'], [1608, 463, 1762, 621, 96.88670635223389, 'rectangle'], [1794, 462, 1944, 618, 96.80204391479492, 'rectangle'], [2170, 464, 2327, 620, 96.4996337890625, 'rectangle'], [1795, 1363, 1950, 1521, 96.36037349700928, 'circle'], [481, 910, 638, 1069, 96.02436423301697, 'circle'], [665, 911, 824, 1070, 95.39172649383545, 'circle'], [1041, 1362, 1198, 1520, 94.91395354270935, 'circle'], [1227, 1364, 1385, 1519, 94.8677659034729, 'circle'], [853, 910, 1009, 1071, 94.59567070007324, 'circle'], [1229, 912, 1386, 1067, 93.66307258605957, 'circle'], [1228, 1138, 1386, 1293, 92.7335262298584, 'circle'], [2169, 688, 2322, 845, 87.39859461784363, 'circle'], [468, 685, 649, 851, 79.39151525497437, 'pentagon'], [653, 683, 836, 852, 78.19159030914307, 'pentagon'], [1018, 1140, 1214, 1297, 75.00344514846802, 'pentagon'], [1864, 684, 2061, 852, 73.93273711204529, 'pentagon'], [1022, 913, 1211, 1071, 72.30607867240906, 'pentagon'], [1869, 1143, 2062, 1297, 72.1400797367096, 'pentagon'], [2079, 1139, 2267, 1297, 69.994056224823, 'pentagon']]
cor3=[[465, 32, 610, 83, 99.14318323135376, 'rectangle'], [373, 228, 467, 281, 98.2014536857605, 'rectangle'], [109, 479, 207, 532, 97.63641357421875, 'rectangle'], [371, 145, 468, 199, 97.63381481170654, 'rectangle'], [583, 146, 680, 198, 97.43796586990356, 'rectangle'], [477, 229, 576, 282, 97.30658531188965, 'rectangle'], [477, 146, 576, 199, 97.2882866859436, 'rectangle'], [214, 479, 314, 533, 97.27458357810974, 'rectangle'], [265, 228, 364, 281, 97.17519283294678, 'rectangle'], [687, 146, 786, 199, 97.14759588241577, 'rectangle'], [788, 311, 887, 365, 97.02692031860352, 'rectangle'], [211, 563, 312, 616, 96.82013392448425, 'rectangle'], [890, 563, 992, 616, 96.69045209884644, 'rectangle'], [579, 478, 680, 531, 96.68223857879639, 'rectangle'], [214, 146, 314, 199, 96.57435417175293, 'rectangle'], [370, 310, 470, 365, 96.52252197265625, 'rectangle'], [160, 227, 259, 282, 96.14912271499634, 'rectangle'], [685, 311, 783, 366, 96.01868391036987, 'rectangle'], [162, 396, 263, 450, 95.89778184890747, 'rectangle'], [161, 311, 262, 366, 95.3068494796753, 'rectangle'], [892, 311, 994, 366, 94.45666074752808, 'rectangle'], [937, 396, 1039, 448, 92.68903732299805, 'rectangle']]
cor4=[[184, 411, 424, 506, 99.38210248947144, 'rectangle'], [883, 411, 1122, 506, 99.33841228485107, 'rectangle'], [535, 411, 767, 507, 99.02624487876892, 'rectangle'], [1235, 410, 1467, 507, 99.01975989341736, 'rectangle'], [710, 249, 947, 341, 97.12972640991211, 'rectangle']]
cor1=[[101, 383, 209, 439, 97.06920981407166, 'rectangle'], [371, 893, 483, 950, 96.64686918258667, 'rectangle'], [74, 677, 182, 732, 96.56767845153809, 'rectangle'], [376, 970, 483, 1027, 96.28012180328369, 'rectangle'], [377, 455, 482, 512, 96.21717929840088, 'rectangle'], [529, 384, 634, 439, 95.40587067604065, 'rectangle'], [74, 603, 182, 659, 95.36973834037781, 'rectangle'], [252, 456, 357, 511, 95.1933741569519, 'rectangle'], [228, 384, 334, 438, 95.01414895057678, 'rectangle'], [377, 384, 483, 438, 94.92214918136597, 'rectangle'], [552, 681, 660, 734, 94.62305307388306, 'rectangle'], [74, 747, 182, 807, 94.16175484657288, 'rectangle'], [399, 605, 507, 658, 94.14619207382202, 'rectangle'], [227, 677, 332, 731, 93.93744468688965, 'rectangle'], [528, 529, 634, 584, 93.73767375946045, 'rectangle'], [532, 604, 634, 656, 93.6383843421936, 'rectangle'], [550, 897, 663, 952, 93.50910186767578, 'rectangle'], [225, 747, 334, 806, 93.13801527023315, 'rectangle'], [377, 749, 482, 807, 93.04974675178528, 'rectangle'], [227, 604, 332, 658, 92.86230802536011, 'rectangle'], [553, 749, 663, 805, 92.83314943313599, 'rectangle'], [377, 692, 485, 746, 92.5514817237854, 'rectangle'], [161, 308, 270, 365, 92.46026277542114, 'rectangle'], [377, 529, 485, 584, 92.4115538597107, 'rectangle'], [254, 528, 360, 584, 91.49185419082642, 'rectangle'], [529, 456, 634, 511, 91.43094420433044, 'rectangle'], [990, 161, 1101, 218, 91.29170179367065, 'rectangle'], [537, 234, 650, 295, 91.22763872146606, 'rectangle'], [1442, 235, 1551, 293, 90.69793224334717, 'rectangle'], [529, 973, 632, 1025, 90.26552438735962, 'rectangle'], [72, 529, 183, 583, 89.480459690094, 'rectangle'], [524, 1043, 633, 1099, 86.72857880592346, 'rectangle'], [991, 234, 1100, 288, 85.78926920890808, 'rectangle'], [75, 457, 184, 509, 75.02048015594482, 'rectangle'], [529, 824, 634, 876, 74.93516802787781, 'rectangle'], [384, 712, 477, 803, 44.96654570102692, 'rectangle']]
path_black='colored_black.jpg'
path_original='ey3.jpg'
nody=[]
fin=[]
te={}
cord_dic=[]
count=0

def citycountname(cityname):
	'''
	Usage:
	INPUT: Name of Place
	OUTPUT: Cityname and country if input is city name else country name if input is country name
'''
	location = geolocator.geocode(cityname,language='en')
	loc_dict = location.raw
	sub=','
	if sub in loc_dict['display_name']:
		return (cityname,loc_dict['display_name'].rsplit(', ' , 1)[1])
	else:
		return (' ',loc_dict['display_name'].rsplit(',' , 1)[0])


def coloring(xii,nodyii,imageii,path_black,coordinates):
	height, width = imageii.shape[:2]
	x0=0
	try:
		x1=nodyii[xii][0][0]-20
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


def sknwii(path_black,cor):
	image  = cv2.imread(path_black,0)
	ret,img = cv2.threshold(image, 0, 255,cv2.THRESH_OTSU)
	binary = img > filters.threshold_otsu(img)
	ske = skeletonize(~binary).astype(np.uint16)

	# build graph from skeleton
	graph = sknw.build_sknw(ske)
	# draw image
	plt.imshow(img, cmap='gray')
	# print(nx.info(graph))

	# draw edges by pts
	for (s,e) in graph.edges():
	    ps = graph[s][e]['pts']
	    plt.plot(ps[:,1], ps[:,0], 'blue')
	    # tolerance = 1
	# print(graph.edges)
	cord=graph.edges
	    # simple_polyline = approximate_polygon(ps, tolerance)
	    # plt.plot(simple_polyline[1:-1, 1], simple_polyline[1:-1, 0], '.m')
	    # print(simple_polyline[1:-1, 1],simple_polyline[1:-1, 0])
	# draw node by o
	nodes = graph.nodes()
	ps = np.array([nodes[i]['o'] for i in nodes])
	plt.plot(ps[:,1], ps[:,0], 'r.')

	# title and show
	plt.title('Built Graph with Nodes(Red) & Edges(Green)')
	# 
	plt.savefig('knw_output.png')
	plt.show()
	def FindPoint(x1, y1, x2, y2, x, y): 
	    if (x > y1 and x < y2 and y > x1 and y < x2): 
	    	# print("kkkkk")
	    	return True
	    else :
	    	# print("aaaa")
	    	return False


	fin=[]
	def prnt(dic,ps,cor):
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
			# print(x)
			# print(y)
			if FindPoint(x1,y1,x2,y2,x,y):
				fin.append(i)
				cord_dic.append(dic)
				a=[x,y]
				te.update({(ps.index(a)): dic})
				break;
	  
	ps = np.array(ps)
	for dic in cor:
		prnt(dic,ps,cor)
	# ocr_text={0: 'AGNICO EAGLE MINES LIMITED (NYSE', 10: 'West Pequcp Project LLC (Nevada)', 12: 'Amico Eagle Mexico, SA de CV', 14: 'Genex Exploration Gorp (Yukon)', 19: 'Agnico Eagle AB (Sweden)', 17: 'Agnice Eagle (Barbados) Lif (Barbados )', 33: 'Ojanv Resources Oy (Finland)', 34: 'Agnios-Eagle (USA) Limited (Nevada)', 39: 'Resources AB (Sweden)', 41: 'Servicios Pinos Altos, SA de CV (Mexicol', 74: 'Penne Insurance Inc. (Barbados)', 73: '1641315 Ontario Inc. (Ontario)', 78: 'Exploration LLC (Nevada)', 82: 'Minera Agave, S.A. de C.V. (Mexico)', 85: 'Agnico-Eagle Mines Sweden Cooperatie U.A (Netherlands)', 94: 'AEUS LLC (Nevada)', 93: 'Annico- Eagle Sweden AB (Sweden)', 111: '1715495 Ontario Inc. (Ontario)', 112: 'Servicios Agnico Estle Mexico, SA do CV (Mexico)', 115: 'Tenedora Amico Eagle Mexico S.A. de C.V. Mexico]', 119: 'Agrico Eagle Mines Mexico Cooperatin U.A.', 121: 'Agnico-Engie Finland Oy (Finland)'}
	fin=np.array(fin)
	fina=fin.tolist()
	# print(fina)
	ps=np.array(ps)
	ps=ps.tolist()
	final_nodes=fina
	final_nodes.sort()
	# print("mmmm")
	# print(ps)
	# print("mmmm")
	# print(final_nodes)
	lengthy = len(final_nodes)
	nody = [[] for i in range(lengthy)]
	# nody=[][]
	nody[0].append(final_nodes[0])
	node_val = [[]for i in range(lengthy)]
	node_val[0].append(ps.index(final_nodes[0]))
	# print(nody)
	a=0
	for i in range(1,lengthy):
		if ((abs(final_nodes[i][0] - final_nodes[i-1][0]))<=10):
			nody[a].append(final_nodes[i])
			node_val[a].append(ps.index(final_nodes[i]))
		else:
			a=a+1
			nody[a].append(final_nodes[i])
			node_val[a].append(ps.index(final_nodes[i]))
	# print("NODY:")
	# print(nody)
	# print(node_val)
	# print("NODE INDEX")
	# print(node_val)

	g = nx.Graph(graph.edges)
	gi = nx.to_directed(graph)
	# print(graph.edges)
	j=[]
	index=[]
	for j in fina:
		index.append(ps.index(j))
	index.sort()

	plt.show()
	
	# print("++++++++++++++++++++++")
	# print(g.number_of_nodes())
	# print("..............................................")
	# print(lengthy)
	# print(nody[0][0])
	count=0
	for i in nody:
		# print(i)
		if len(i)==0:
			continue
		else:
			count=count+1
	# print("..............................................")
	# print(count)
	# print(len(nody[1]))
	# print("..............................................")
	return count,nody,ps,g,te

nody=[]
fin=[]
te={}
cord_dic=[]
def sk_se(cor):
	image  = cv2.imread('imagedraw.jpg',0)
	ret,img = cv2.threshold(image, 0, 255,cv2.THRESH_OTSU)
	binary = img > filters.threshold_otsu(img)
	ske = skeletonize(~binary).astype(np.uint16)

	# build graph from skeleton
	graph = sknw.build_sknw(ske)
	# draw image
	plt.imshow(img, cmap='gray')
	# print(nx.info(graph))

	# draw edges by pts
	for (s,e) in graph.edges():
	    ps = graph[s][e]['pts']
	    plt.plot(ps[:,1], ps[:,0], 'blue')
	    # tolerance = 1
	# print(graph.edges)
	cord=graph.edges
	    # simple_polyline = approximate_polygon(ps, tolerance)
	    # plt.plot(simple_polyline[1:-1, 1], simple_polyline[1:-1, 0], '.m')
	    # print(simple_polyline[1:-1, 1],simple_polyline[1:-1, 0])
	# draw node by o
	nodes = graph.nodes()
	ps = np.array([nodes[i]['o'] for i in nodes])
	plt.plot(ps[:,1], ps[:,0], 'r.')
	# print(ps)
	# print("____________________")
	# print(graph.nodes)
	# print("____________________")
	# # title and show
	plt.title('Built Graph with Nodes(Red) & Edges(Green)')
	# 
	plt.savefig('knw_output.png')
	plt.show()
	def FindPoint(x1, y1, x2, y2, x, y): 
	    if (x >= y1 and x <= y2 and y >= x1 and y <= x2): 
	    	# print("kkkkk")
	    	return True
	    else :
	    	# print("aaaa")
	    	return False


	fin=[]
	def prnt(dic,ps,cor):
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
			# print(x)
			# print(y)
			if FindPoint(x1,y1,x2,y2,x,y):
			# print("gggg")
				fin.append(i)
				cord_dic.append(dic)
				a=[x,y]
				te.update({(ps.index(a)): dic})
				break;
	  
	cor = np.array(cor)
	ps = np.array(ps)
	for dic in cor:
		prnt(dic,ps,cor)
	# ocr_text={0: 'AGNICO EAGLE MINES LIMITED (NYSE', 10: 'West Pequcp Project LLC (Nevada)', 12: 'Amico Eagle Mexico, SA de CV', 14: 'Genex Exploration Gorp (Yukon)', 19: 'Agnico Eagle AB (Sweden)', 17: 'Agnice Eagle (Barbados) Lif (Barbados )', 33: 'Ojanv Resources Oy (Finland)', 34: 'Agnios-Eagle (USA) Limited (Nevada)', 39: 'Resources AB (Sweden)', 41: 'Servicios Pinos Altos, SA de CV (Mexicol', 74: 'Penne Insurance Inc. (Barbados)', 73: '1641315 Ontario Inc. (Ontario)', 78: 'Exploration LLC (Nevada)', 82: 'Minera Agave, S.A. de C.V. (Mexico)', 85: 'Agnico-Eagle Mines Sweden Cooperatie U.A (Netherlands)', 94: 'AEUS LLC (Nevada)', 93: 'Annico- Eagle Sweden AB (Sweden)', 111: '1715495 Ontario Inc. (Ontario)', 112: 'Servicios Agnico Estle Mexico, SA do CV (Mexico)', 115: 'Tenedora Amico Eagle Mexico S.A. de C.V. Mexico]', 119: 'Agrico Eagle Mines Mexico Cooperatin U.A.', 121: 'Agnico-Engie Finland Oy (Finland)'}
	# print(fin)
	fin=np.array(fin)
	fina=fin.tolist()
	# print(fina)
	ps=np.array(ps)
	ps=ps.tolist()
	final_nodes=fina
	final_nodes.sort()
	# print("mmmm")
	# print(final_nodes)
	lengthy = len(final_nodes)
	nody = [[] for i in range(lengthy)]
	# nody=[][]
	nody[0].append(final_nodes[0])
	node_val = [[]for i in range(lengthy)]
	node_val[0].append(ps.index(final_nodes[0]))
	# print(nody)
	a=0
	for i in range(1,lengthy):
		if ((final_nodes[i][0] - final_nodes[i-1][0])<=10):
			nody[a].append(final_nodes[i])
			node_val[a].append(ps.index(final_nodes[i]))
		else:
			a=a+1
			nody[a].append(final_nodes[i])
			node_val[a].append(ps.index(final_nodes[i]))
	# print("NODY:")
	# print(nody)
	# print(node_val)
	# print("NODE INDEX")
	# print(node_val)

	g = nx.Graph(graph.edges)
	gi = nx.to_directed(graph)
	# print(graph.edges)
	j=[]
	index=[]
	for j in fina:
		index.append(ps.index(j))

	res = {index[i]: cord_dic[i] for i in range(len(index))} 
	index.sort()

	plt.show()

	# print("++++++++++++++++++++++")
	# print(g.number_of_nodes())
	return nody,ps,g,te


def fillbox(path,thresh_image,coordinates):
# path = 'test11.jpg'
	
	image = cv2.imread(path, 0) 
		
	# Window name in which image is displayed 
	# window_name = 'Image'

	# Start coordinate, here (100, 50) 
	# represents the top left corner of rectangle 
	for i in range(len(coordinates)):
		start_point=(coordinates[i][0],coordinates[i][1])
		end_point=(coordinates[i][2],coordinates[i][3])
		color = (0, 0, 0) 
		thickness = -1
		image = cv2.rectangle(image, start_point, end_point, color, thickness) 
	cv2.imwrite(thresh_image,image)



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

	# If you are using a Jupyter notebook, uncomment the following line.
	# %matplotlib inline

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
	    # add_item(ocr_text,res,n)
	    # print(n)
	    # ten.update({n:res})
	    return res,prec,shape

def main():
	image = cv2.imread(path_original)

	workbook = xlsxwriter.Workbook('graph.xls')
	worksheet = workbook.add_worksheet()
	workbook.close()
	count,nody,ps,g,te= sknwii(path_black,cor)
	book_ro = open_workbook("graph.xls")
	book = copy(book_ro)  # creates a writeable copy
	sheet1 = book.get_sheet(0)  # get a first sheet
	sheet1.write(0,0,'ID')
	sheet1.write(0,1,'Child')
	sheet1.write(0,2,'Immediate Parent')
	sheet1.write(0,3,'Shape Percentage')
	sheet1.write(0,4,'Shapes')
	sheet1.write(0,5,'City')
	sheet1.write(0,6,'Country')
	sheet1.write(0,7,'Own Percentage')
	row=1
	te=np.array(te)
	te=te.tolist()
	for i in range(count):
		coloring(i,nody,image,path_original,cor)
		nody,ps,g,te= sk_se(cor)
		for j in range(len(nody[i])):
			# print("in 2nd loop")
			# county=0
			flag=0
			for k in range(len(nody[i+1])):
				source=ps.index(nody[i][j])
				destination=int(ps.index(nody[i+1][k]))
				# print(source,destination)
				# print("in 3rd loop")
				# print(nx.has_path(g,source,destination))/
				
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

						print("here also")
						# city,w=citycountname(city)
					else:
						city =' '
						w = ' '




					kk=res
					per= re.findall('\d*%',kk)
					if per:
						res=re.sub(r'\d*%'," ",kk)
					else:
						per='100%'
					sheet1.write(row,2,res)

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
						except Exception as e:
							print(e)
							city=''
							w=''
						start = sem.find( '(' )
						if start != -1:
							res = sem[0:start-1]
					else:
						city =' '
						w = ' '

						

					sheet1.write(row,0,row)
					sheet1.write(row,1,res)
					sheet1.write(row,3,prec)
					sheet1.write(row,4,shape)
					sheet1.write(row,5,city)
					sheet1.write(row,6,w)
					sheet1.write(row,7,per)
	
					# sheet1.write(row,0,result)
					# sheet1.write(row,1,textt(te[destination],destination,path_original))
					# print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
					# print(row)
					# county = county+1
					row=row+1
					flag=1
			if flag==0:
				for l in range(len(nody[i+2])):
					source=ps.index(nody[i][j])
					try:
						destination=int(ps.index(nody[i+2][l]))
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

								print("here also")
								# city,w=citycountname(city)
							else:
								city =' '
								w = ' '




							kk=res
							per= re.findall('\d*%',kk)
							if per:
								res=re.sub(r'\d*%'," ",kk)
							else:
								per='100%'
							sheet1.write(row,2,res)

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
								except Exception as e:
									print(e)
									city=''
									w=''
								start = sem.find( '(' )
								if start != -1:
									res = sem[0:start-1]
							else:
								city =' '
								w = ' '

								

							sheet1.write(row,0,row)
							sheet1.write(row,1,res)
							sheet1.write(row,3,prec)
							sheet1.write(row,4,shape)
							sheet1.write(row,5,city)
							sheet1.write(row,6,w)
							sheet1.write(row,7,per)
			
							# sheet1.write(row,0,result)
							# sheet1.write(row,1,textt(te[destination],destination,path_original))
							# print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
							# print(row)
							# county = county+1
							row=row+1						# sheet1.write(row,0,result)
					except Exception as e: print(e)
						# sheet1.write(row,1," ")
						# row=row+1
						# continue

		
		

	book.save("graph.xls")







main()



