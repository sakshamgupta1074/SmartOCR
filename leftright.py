
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
from io import BytesIO
import io
import json
from shapely.geometry import Polygon
import re
from geopy.geocoders import Nominatim
import scipy.misc
from scipy import ndimage
import imageio


geolocator = Nominatim(timeout=3,user_agent="countrychecker")

#to color levels
def color_black(path,cor):
	image = cv2.imread(path)
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

		# cv2.imshow("Polygon", image)
	cv2.imwrite('colored_black.jpg', image)
	
# binary erosion of image to plot graph
def erosion(path):
	im = imageio.imread(path)
	im = ndimage.binary_erosion(im).astype(np.float32)
	imageio.imwrite('erosion.jpg', im)

#to find city,state and country from the 1 given in org chart.
def citycountname(cityname):
	location = geolocator.geocode(cityname,language='en')
	loc_dict = location.raw
	sub=','
	stateb=len(loc_dict['display_name'].rsplit(',')[0:-1])
	if stateb==1:
		return ('-',cityname,loc_dict['display_name'].rsplit(', ' , 1)[1])
	if stateb>1:
		return (cityname,loc_dict['display_name'].rsplit(', ')[-2],loc_dict['display_name'].rsplit(', ' , 1)[1])
	elif sub not in loc_dict['display_name']:
		return ('-','-',loc_dict['display_name'].rsplit(',' , 1)[0])


#to color levels.
def coloring(xii,nodyii,imageii,path_black,coordinates,ps):
	height, width = imageii.shape[:2]
	# nody=[[[57.0, 492.0]], [[172.0, 262.0], [172.66666666666666, 401.3333333333333], [172.66666666666666, 506.3333333333333], [172.66666666666666, 716.3333333333334], [172.75, 629.0]], [[254.0, 342.0], [255.66666666666666, 191.33333333333334], [255.66666666666666, 402.3333333333333], [255.75, 524.0]], [[337.75, 418.0], [338.0, 210.0], [338.6666666666667, 716.3333333333334], [338.75, 825.0], [338.75, 929.0]], [[421.6666666666667, 969.3333333333334], [422.0, 209.5]], [[504.75, 615.0], [505.6666666666667, 139.33333333333334], [506.0, 261.0]], [[588.75, 925.0], [589.0, 287.0]], [], [], [], [], [], [], [], [], [], [], [], [], [], [], []]
	x0=0
	# ##print(nodyii)
	##print(nodyii)
	#print(ps[nodyii[xii][0]])
	y_cor=(ps[nodyii[xii][0]][1])
	##print(y_cor)
	try:
		y1=y_cor-20
		##print("in try coloring")
		
		
	except:
		y1=0
		##print("in except")
		
	y0=0
	x1=width
	im = Image.open(path_black)
	draw = ImageDraw.Draw(im)
	draw.rectangle((y0,x0,y1,x1), fill=(255,255,255), outline=(255,255,255))
	##print("aaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaaa")
	im.save('imagedraw.jpg')
	path='imagedraw.jpg'
	fillbox(path,'imagedraw.jpg',coordinates)
	# erosion.erosion('imagedraw.jpg')

#to plot main graph
def sknwii(path_black,cor):
	image  = cv2.imread(path_black,0)
	ret,img = cv2.threshold(image, 0, 255,cv2.THRESH_OTSU)
	binary = img > filters.threshold_otsu(img)
	ske = skeletonize(~binary).astype(np.uint16)
	nody=[[]]
	te={}
	node_val={}
	# build graph from skeleton
	graph = sknw.build_sknw(ske)
	# draw image
	plt.imshow(img, cmap='gray')
	# ##print(nx.info(graph))

	# draw edges by pts
	for (s,e) in graph.edges():
		ps = graph[s][e]['pts']
		plt.plot(ps[:,1], ps[:,0], 'blue')
		# tolerance = 1
	# ##print(graph.edges)
	cord=graph.edges
		
	# draw node by o
	nodes = graph.nodes()
	ps = np.array([nodes[i]['o'] for i in nodes])
	plt.plot(ps[:,1], ps[:,0], 'r.')
	

	plt.title('Built Graph with Nodes(Red) & Edges(Green)')
	
	plt.savefig('knw_output.png')
	plt.show()
	def FindPoint(x1, y1, x2, y2, x, y): 
		if (x >= y1 and x <= y2 and y >= x1 and y <= x2): 
			
			return True
		else :
			
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
			
			if FindPoint(x1,y1,x2,y2,x,y):
				fin.append(i)
				cord_dic.append(dic)
				a=[x,y]
				te.update({(ps.index(a)): dic})
				
				break;
	
	ps = np.array(ps)
	ps=ps.tolist()
	for dic in cor:
		prnt(dic,ps,cor)
	
	#print(te)  
	fin=np.array(fin)
	fina=fin.tolist()
	for i in fina:
		plt.plot(i[1], i[0], 'bo')
		text=ps.index([i[0],i[1]])
		
		matplotlib.pyplot.text(i[1], i[0], str(text),fontsize=12,color='white')

	
	ps=np.array(ps)
	ps=ps.tolist()
	final_nodes=fina
	
	final_nodes.sort(key = lambda x: x[1])
	
	lengthy = len(cor)
	values=list(te.values())
	nody = [[] for i in range(lengthy)]
	
	nody[0].append(cor[0])
	node_val = [[]for i in range(lengthy)]
	node_val[0].append(list(te.keys())[list(te.values()).index(cor[0])])
	a=0
	for i in range(1,lengthy):
		if (abs(cor[i][0] - cor[i-1][0])<=10):
			nody[a].append(cor[i])
			node_val[a].append(list(te.keys())[list(te.values()).index(cor[i])])

		else:
			a=a+1
			nody[a].append(cor[i])
			node_val[a].append(list(te.keys())[list(te.values()).index(cor[i])])
	
	
	count=0
	for i in node_val:
		# ##print(i)
		if len(i)==0:
			continue
		else:
			count=count+1

	return count,node_val,ps,graph,te
nody=[]
fin=[]
te={}
cord_dic=[]

#to plot level graphs
def sk_se(cor):
	image  = cv2.imread('imagedraw.jpg',0)
	ret,img = cv2.threshold(image, 0, 255,cv2.THRESH_OTSU)
	binary = img > filters.threshold_otsu(img)
	ske = skeletonize(~binary).astype(np.uint16)
	nody=[[]]
	te={}
	node_val=[[]]
	# build graph from skeleton
	graph = sknw.build_sknw(ske)
	# draw image
	plt.imshow(img, cmap='gray')
	

	# draw edges by pts
	for (s,e) in graph.edges():
		ps = graph[s][e]['pts']
		plt.plot(ps[:,1], ps[:,0], 'blue')
		# tolerance = 1
	
	cord=graph.edges
		
	nodes = graph.nodes()
	ps = np.array([nodes[i]['o'] for i in nodes])
	plt.plot(ps[:,1], ps[:,0], 'r.')
	
	# title and show
	plt.title('Built Graph with Nodes(Red) & Edges(Green)')
	# # 
	plt.savefig('knw_output.png')
	plt.show()


	def FindPoint(x1, y1, x2, y2, x, y): 
		if (x >= y1 and x <= y2 and y >= x1 and y <= x2): 
		
			return True
		else :
			
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
			
			if FindPoint(x1,y1,x2,y2,x,y):
			
				fin.append(i)
				cord_dic.append(dic)
				a=[x,y]
				te.update({(ps.index(a)): dic})
				break;
	  

	
	for dic in cor:
		prnt(dic,ps,cor)

	if len(te) == 0:
		return node_val,ps,graph,te
	fin=np.array(fin)
	fina=fin.tolist()
	
	ps=np.array(ps)
	ps=ps.tolist()
	final_nodes=fina
	
	final_nodes.sort(key = lambda x: x[1])

	lengthy = len(cor)
	values=list(te.values())
	nody = [[] for i in range(lengthy)]

	nody[0].append(cor[0])
	node_val = [[]for i in range(lengthy)]
	node_val[0].append(list(te.keys())[list(te.values()).index(cor[0])])
	
	a=0
	for i in range(1,lengthy):
		if (abs(cor[i][0] - cor[i-1][0])<=10):
			nody[a].append(cor[i])
			node_val[a].append(list(te.keys())[list(te.values()).index(cor[i])])

		else:
			a=a+1
			nody[a].append(cor[i])
			node_val[a].append(list(te.keys())[list(te.values()).index(cor[i])])
	
	
	for i in fina:
		plt.plot(i[1], i[0], 'go')
		text=ps.index([i[0],i[1]])
		
		matplotlib.pyplot.text(i[1], i[0], str(text),fontsize=12,color='red')

	no=[[]]
	for i in range(lengthy):
		for j in range(len(node_val[i])):
			try:
				no[i][j]=ps[node_val[i][j]]
			except Exception as e:
				print(e)
				
	return node_val,ps,graph,te
	
	
#to fill entity to plot graph
def fillbox(path,thresh_image,coordinates):

	
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


#to ocr image
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
		##print("From Azure Cognitive Service, retrieve your endpoint and subscription key.")
		##print("\nSet the COMPUTER_VISION_ENDPOINT environment variable, such as \"https://westus2.api.cognitive.microsoft.com\".\n")
		missing_env = True

	if 'COMPUTER_VISION_SUBSCRIPTION_KEY' in os.environ:
		subscription_key = os.environ['COMPUTER_VISION_SUBSCRIPTION_KEY']
	else:
		##print("From Azure Cognitive Service, retrieve your endpoint and subscription key.")
		##print("\nSet the COMPUTER_VISION_SUBSCRIPTION_KEY environment variable, such as \"1234567890abcdef1234567890abcdef\".\n")
		missing_env = True

	if missing_env:
		##print("**Restart your shell or IDE for changes to take effect.**")
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

#main function for module left to right
def main(path_original,path_black,cor,scount,workbook):
	nody=[]
	fin=[]
	te={}
	cord_dic=[]
	count=0
	image = cv2.imread(path_original)

	

	if scount!="Org_Chart-1":
		sheet = workbook.add_worksheet(scount)
	else:
		sheet = workbook.add_worksheet("Org_Chart-1") 
	bold = workbook.add_format({'bold': True})
	format1 = workbook.add_format({'border': 5,'bold': True,'align': 'center','bg_color': '#FFC7CE'})
	center = workbook.add_format({'align': 'center'})
	format2 = workbook.add_format({'align': 'center','border': 2})
	format3 = workbook.add_format({'border': 5,'bold': True,'align': 'center','bg_color': 'cyan'})
	format4 = workbook.add_format({'align': 'center','border': 2,'bg_color': '#FF0000','bold': True})
	format5 = workbook.add_format({'align': 'center','border': 2,'bg_color': '#008000','bold': True})

	count,node_val,ps,g,te= sknwii(path_black,cor)
	sheet.write(0,0,'Unique ID',format1)
	sheet.set_column('A:A', 15)
	sheet.write(0,1,'Child',format1)
	sheet.set_column('B:B', 35)
	sheet.write(0,2,'Immediate Parent',format1)
	sheet.set_column('C:C', 35)
	sheet.write(0,5,'Shape Percentage',format1)
	sheet.set_column('F:F', 20)
	sheet.write(0,4,'Shapes',format1)
	sheet.set_column('E:E', 20)
	sheet.write(0,6,'City',format1)
	sheet.set_column('G:G', 20)
	sheet.write(0,7,'State',format1)
	sheet.set_column('H:H', 20)
	sheet.write(0,8,'Country',format1)
	sheet.set_column('I:I', 20)
	sheet.write(0,9,'Relationship Type',format1)
	sheet.set_column('J:J', 55)
	sheet.write(0,3,'Own Percentage',format1)
	sheet.set_column('D:D', 15)
	idd='UID1'
	row=2
	te=np.array(te)
	te=te.tolist()
	
	result,prec,shape=textt(te[(node_val[0][0])],(node_val[0][0]),path_original)

	sem = result
	res=result
	kk=res
	per= re.findall('\d*%',kk)
	if per:
		res=re.sub(r'\d*%'," ",kk)
	else:
		per='NA'
	city = re.search('\(([^)]+)', sem)

	if city:
		city=city.group(1)
		res=re.sub("[\(\[].*?[\)\]]", "", sem)
		try:
			city,state,w=citycountname(city)
		except Exception as e:
			print(e)
			city='-'
			w='-'
			state='-'
		start = sem.find( '(' )
		if start != -1:
			res = sem[0:start-1]
	else:
		city ='-'
		w = '-'
		state='-'
	prec=round(float(prec),2)
	prec=str(prec)+'%'
	sheet.write(1,1,res,format2)
	sheet.write(1,0,'UID1',format3)
	sheet.write(1,5,prec,format2)
	sheet.write(1,4,shape,format2)
	sheet.write(1,6,city,format2)
	sheet.write(1,8,w,format2)
	sheet.write(1,7,state,format2)
	sheet.write(1,3,'',format2)
	sheet.write(1,2,'',format2)
	sheet.write(1,9,' If Own Percentage > 50 then CONTROL else IMMATERIAL',format3)

	for i in range(count):
		
		coloring(i,node_val,image,path_black,cor,ps)
		node_val,ps,g,te= sk_se(cor)
		
		if len(te)==0:
			break
		
		for j in range(len(node_val[i])):
			
			flag=0
		
			for k in range(len(node_val[i+1])):
				source=(node_val[i][j])
				destination=(node_val[i+1][k])
				
				
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
						city ='-'
						w = '-'
						state='-'

					kk=res
					per= re.findall('\d*%',kk)
					if per:
						res=re.sub(r'\d*%'," ",kk)
					else:
						per='NA'
					sheet.write(row,2,res,format2)

					result,prec,shape=textt(te[destination],destination,path_original)
					sem = result
					res=result
					kk=res
					per= re.findall('\d*%',kk)
					if per:
						res=re.sub(r'\d*%'," ",kk)
						
					else:
						per='NA'


					try:
						if int(str(per[0])[:-1])>50:
							sheet.write(row,9,"CONTROL",format5)
						elif int(str(per[0])[:-1])<50:
							sheet.write(row,9,"IMMATERIAL SIGNIFICANT INFLUENCE",format4)

						elif per=='NA':
							sheet.write(row,9,'NA',format2)
					except:
						sheet.write(row,9,'NA',format2)


					city = re.search('\(([^)]+)', sem)

					if city:
						city=city.group(1)
						res=re.sub("[\(\[].*?[\)\]]", "", sem)
						try:
							city,state,w=citycountname(city)
						except Exception as e:
							print(e)
							continue
							city='-'
							w='-'
							state='-'
						start = sem.find( '(' )
						if start != -1:
							res = sem[0:start-1]
					else:
						city ='-'
						w = '-'
						state='-'
					try:
						res=re.sub(r'\d*%'," ",res)
						city=re.sub(r'\d*%'," ",city)
						w=re.sub(r'\d*%'," ",w)
					except Exception as e:
						print(e)
					prec=round(float(prec),2)
					prec=str(prec)+'%'  
					idd='UID'+str(row)
					sheet.write(row,0,idd,format3)
					sheet.write(row,1,res,format2)
					sheet.write(row,5,prec,format2)
					sheet.write(row,4,shape,format2)
					sheet.write(row,6,city,format2)
					sheet.write(row,7,state,format2)
					sheet.write(row,8,w,format2)
					sheet.write(row,3,str(per[0]),format2)
					row=row+1
					flag=1
			if flag==0:
				for l in range(len(node_val[i+2])):
					source=(node_val[i][j])
					try:
						destination=(node_val[i+2][l])
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
								city ='-'
								w = '-'
								state='-'
							kk=res
							per= re.findall('\d*%',kk)
							if per:
								res=re.sub(r'\d*%'," ",kk)
							else:
								per='NA'
							sheet.write(row,2,res,format2)

							result,prec,shape=textt(te[destination],destination,path_original)
							sem = result
							res=result
							city = re.search('\(([^)]+)', sem)
							kk=res
							per= re.findall('\d*%',kk)
							if per:
								res=re.sub(r'\d*%',' ',kk)
								# #print(per)
							else:
								per='NA'
							try:

								if int(str(per[0])[:-1])>50:
									sheet.write(row,9,"CONTROL",format5)
								elif int(str(per[0])[:-1])<50:
									sheet.write(row,9,"IMMATERIAL SIGNIFICANT INFLUENCE",format4)

								elif per=='NA':
									sheet.write(row,9,'NA',format2)
							except:
								sheet.write(row,9,'NA',format2)
							if city:
								city=city.group(1)
								res=re.sub("[\(\[].*?[\)\]]", "", sem)
								try:
									city,state,w=citycountname(city)
								except Exception as e:
									print(e)
									continue
									city='-'
									w='-'
									state='-'
								start = sem.find( '(' )
								if start != -1:
									res = sem[0:start-1]
							else:
								city ='-'
								w = '-'
								state='-'
							try:
								res=re.sub(r'\d*%'," ",res)
								city=re.sub(r'\d*%'," ",city)
								w=re.sub(r'\d*%'," ",w)
							except Exception as e:
								print(e)
							prec=round(float(prec),2)
							prec=str(prec)+'%'
							idd='UID'+str(row)
							sheet.write(row,0,idd,format3)
							sheet.write(row,1,res,format2)
							sheet.write(row,5,prec,format2)
							sheet.write(row,4,shape,format2)
							sheet.write(row,6,city,format2)
							sheet.write(row,7,state,format2)
							sheet.write(row,8,w,format2)
				
							sheet.write(row,3,str(per[0]),format2)

							row=row+1                   
					except Exception as e:
						print(e)
						continue



	


#call function of left to right org chart
def lefttoright(path,corpoints,scount,workbook):
	path_original=path
	color_black(path_original,corpoints)
	erosion('colored_black.jpg')
	path_black='erosion.jpg'
	corpoints.sort()
	main(path_original,path_black,corpoints,scount,workbook)



