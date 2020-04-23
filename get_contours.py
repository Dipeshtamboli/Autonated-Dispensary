def min_max(array):	
	xmin=9999
	xmax=-9999
	ymin=9999
	ymax=-9999
	for i in range(0,len(array)):
		xmin=min(xmin,array[i][0][0])
		xmax=max(xmax,array[i][0][0])
		ymin=min(ymin,array[i][0][1])
		ymax=max(ymax,array[i][0][1])
	return xmin,xmax,ymin,ymax

def area(img):
	return img[0].shape[0]*img[0].shape[1]

def inside(im1,im2):
	b=im1[1][0]>=im2[1][0] and im1[1][1]<=im2[1][1] and im1[1][2]>=im2[1][2] and im1[1][3]<=im1[1][3]
	return b

import cv2
import numpy as np 

def compress(recs):
	recs=sorted(recs,key=area)
	imgs=[]
	pos=[]
	for i in range(0,len(recs)):
		f=0
		for j in range(i+1,len(recs)):
			if inside(recs[i],recs[j]) == True:
				f=1
				break
		if f == 0:
			imgs.append(recs[i][0])
			pos.append([recs[i][1][0],recs[i][1][2]])
	return(imgs,pos)

def get_smaller_images(path='Test1.jpg'):
	gray=cv2.imread(path, 0)
	#Might wanna resize here
	gray = cv2.bilateralFilter(gray, 11, 17, 17)
	edged = cv2.Canny(gray, 30, 200)
	(__,cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cnts = sorted(cnts,key = cv2.contourArea, reverse = True)[:15]
	ret=[]
	for c in cnts:
		xmin,xmax,ymin,ymax=min_max(c)
		# print(min_max(c))
		ret.append((image[ymin:ymax,xmin:xmax,:],[xmin,xmax,ymin,ymax]))
	imgs,pos=compress(ret)
	print(pos)
	return imgs,pos




