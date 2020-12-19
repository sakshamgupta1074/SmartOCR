
from skimage.morphology import skeletonize
from skimage import data
from skimage import morphology, filters
import sknw
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import networkx as nx
from skimage.measure import approximate_polygon
matplotlib.use('Agg')
import cv2
image  = cv2.imread('threshold.png',0)
print(image.dtype)
ret,img = cv2.threshold(image, 0, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
binary = img > filters.threshold_otsu(img)
ske = skeletonize(~binary).astype(np.uint16)

# build graph from skeleton
graph = sknw.build_sknw(ske)
print("HHHHHHHHHHHHHHHHHHH")
print(graph)
print("YYYYYYYYYYYYY")
# draw image
plt.imshow(image, cmap='gray')
# draw edges by pts
for (s,e) in graph.edges():
    ps = graph[s][e]['pts']
    plt.plot(ps[:,1], ps[:,0], 'green')
    # tolerance = 1
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
'''
from skimage.morphology import skeletonize
from skimage import data
from skimage import morphology, filters
import sknw
import numpy as np
import matplotlib.pyplot as plt
import matplotlib
import networkx as nx
from skimage.measure import approximate_polygon
matplotlib.use('Agg')
import cv2
image  = cv2.imread('test11-1.jpg',0)
ret,img = cv2.threshold(image, 0, 255,cv2.THRESH_BINARY | cv2.THRESH_OTSU)
binary = img > filters.threshold_otsu(img)
ske = skeletonize(~binary).astype(np.uint16)

# build graph from skeleton
graph = sknw.build_sknw(ske)

# draw image
plt.imshow(img, cmap='gray')

# draw edges by pts
for (s,e) in graph.edges():
    ps = graph[s][e]['pts']
    plt.plot(ps[:,1], ps[:,0], 'green')
    
# draw node by o
nodes = graph.nodes()
ps = np.array([nodes[i]['o'] for i in nodes])
plt.plot(ps[:,1], ps[:,0], 'r.')

# title and show
plt.title('Build Graph')
plt.savefig('knw_output.png')
plt.show()
'''