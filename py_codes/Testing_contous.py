import cv2
import numpy as np
from math import atan,degrees
'''
This script basically breaks down a large image into smaller images according to object contours, and returns the smaller images to 
the sliding windows script
'''
def min_max(array):	
	'''
	Returns bounding box of a contour
	'''
	xmin=9999
	xmax=-9999
	ymin=9999
	ymax=-9999
	for i in range(0,len(array)):
		xmin=min(xmin,array[i][0][0])
		xmax=max(xmax,array[i][0][0])
		ymin=min(ymin,array[i][0][1])
		ymax=max(ymax,array[i][0][1])
	return xmin-20,xmax+20,ymin-20,ymax+20

def dist(p1,p2):
	return(int(((p1[0]-p2[0])**2+(p1[1]-p2[1])**2)**(0.5)))
def adjacent(box1,box2):
	'''
	Tells whether two boxes are adjacent or not depending upon the distance between their centroids
	'''
	threshold=10
	# if(abs(box1[1][0]-box2[1][1])<=threshold or abs(box1[1][1]-box2[1][0])<=threshold or abs(box1[1][2]-box2[1][3])<threshold or abs(box1[1][3]-box2[1][2])<threshold):
	# 	print(abs(box1[1][0]-box2[1][1]))
	# 	print(abs(box1[1][1]-box2[1][0]))
	# 	print(abs(box1[1][2]-box2[1][3]))
	# 	return True 
	if(dist([(box1[1][0]+box1[1][1])/2,(box1[1][2]+box1[1][3])/2],[(box2[1][0]+box2[1][1])/2,(box2[1][2]+box2[1][3])/2])-((((box2[1][1]-box2[1][0]+box1[1][1]-box1[1][0])/2)**2+((box2[1][3]-box2[1][2]+box1[1][3]-box1[1][2])/2)**2)**0.5)<=threshold):
		return True

def rotate(image,contour,pos):
	'''
	Rotates an image such that its minimum are rectangle is perpendicular to the edges
	WARNING- unstable implementation, use at your own risk
	'''
	rect=cv2.minAreaRect(contour)
	box=cv2.boxPoints(rect)
	box=np.int0(box)
	p1=[box[0][0]-pos[0],box[0][1]-pos[2]]
	p2=[box[1][0]-pos[0],box[1][1]-pos[2]]
	p3=[box[2][0]-pos[0],box[2][1]-pos[2]]
	# p4=[box[3][0]-pos[0],box[3][1]-pos[2]]
	# print([p1,p2,p3,p4])
	ht = dist(p1,p2)
	w = dist(p2,p3)
	print("ht=",ht,"w=",w)
	M=cv2.moments(contour)
	cx = int(M['m10']/M['m00'])
	cy = int(M['m01']/M['m00'])

	cx = cx-pos[0]+max(ht,w)
	cy = cy-pos[2]+max(ht,w)
	shape=(image.shape[0]+2*max(ht,w),image.shape[1]+2*max(ht,w),image.shape[2])
	canvas=np.zeros(shape,np.uint8)
	angle=degrees(atan(float((p1[0]-p2[0])/(p1[1]-p2[1]))))
	print("angle=",angle)
	cx = canvas.shape[1]//2
	cy = canvas.shape[0]//2
	rotMat=cv2.getRotationMatrix2D((cx,cy),-angle,1)
	canvas[max(ht,w):image.shape[0]+max(ht,w) , max(ht,w):image.shape[1]+max(ht,w) , :] = image[:,:,:]

	canvas = cv2.warpAffine(canvas,rotMat,(canvas.shape[0],canvas.shape[1]))
	return(canvas[cy-ht//2:cy+ht//2,cx-w//2:cx+w//2,:])

def generate_bigger_contour(box1,box2,image):
	'''
	Merges two adjacent contours
	'''
	xmin=min(box1[1][0],box2[1][0])
	xmax=max(box1[1][1],box2[1][1])
	ymin=min(box1[1][2],box2[1][2])
	ymax=max(box1[1][3],box2[1][3])
	return(image[ymin:ymax,xmin:xmax,:],[xmin,xmax,ymin,ymax])

def area(img):
	return img[0].shape[0]*img[0].shape[1]

def aspect_ratio(img):
	return float(img[0].shape[1]/img[0].shape[0])

def inside(im1,im2):
	b=im1[1][0]>=im2[1][0] and im1[1][1]<=im2[1][1] and im1[1][2]>=im2[1][2] and im1[1][3]<=im1[1][3]
	return b

def compress(recs,img):
	recs=sorted(recs,key=area)
	recs=[x for x in recs if area(x)>10000]
	recs=[x for x in recs if aspect_ratio(x)>0.2499999999 and aspect_ratio(x)<4]
	imgs=[]	
	pos=[]
	rec_=[]
	flag = 0

	for k in range(0,5):
		recs=sorted(recs,key=area)
		recs=[x for x in recs if area(x)>10000]
		recs=[x for x in recs if aspect_ratio(x)>0.2499999999 and aspect_ratio(x)<4]
		imgs=[]	
		pos=[]
		rec_=[]
		rec__=[]
		for i in range(0,len(recs)):
			#print(i)
			f=0 	
			for j in range(i+1,len(recs)):
				if inside(recs[i],recs[j]) == True:
					f=1
					break
			if f == 0:
				#print(j)
				#imgs.append(rotate(recs[i][0],recs[i][2],recs[i][1]))
				rec_.append([recs[i][0],recs[i][1],recs[i][2],0])
			
		for i in range(len(rec_)):
			for j in range(i+1,len(rec_)):
				if(adjacent(rec_[i],rec_[j])):
					rec_[i][3]=1
					rec_[j][3]=1

					img_small,pos_small=generate_bigger_contour(rec_[i],rec_[j],img)
					# cv2.imshow("",rec_[i][0])
					# cv2.waitKey()
					# cv2.imshow("",rec_[j][0])
					# cv2.waitKey()
					# cv2.imshow("",img_small)
					# cv2.waitKey(0)
					if(flag==1):
						cv2.imshow("",img_small)
						cv2.waitKey(0)
						imgs.append(img_small)
						pos.append(pos_small)
						flag = 2
					else:
						rec__.append([img_small,pos_small,0])
			if(rec_[i][3]==0 and flag>=1):
				imgs.append(rec_[i][0])
				pos.append([rec_[i][1][0],rec_[i][1][2]])
				flag = 2
			else:
				rec__.append(rec_[i])
		if len(recs)==len(rec__):
			flag = 1
		recs=rec__
		if flag == 2:
			break
	return(list(reversed(imgs)),list(reversed(pos)))

def get_smaller_images(path='Picture 17.jpg'):
	image=cv2.imread(path)
	#Might wanna resize here
	gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
	gray = cv2.bilateralFilter(gray, 11, 17, 17)
	cv2.imshow("Image",image)
	cv2.waitKey(0)
	edged = cv2.Canny(gray, 10, 75)
	cv2.imwrite("edged1.jpg",edged)
	(__,cnts, _) = cv2.findContours(edged.copy(), cv2.RETR_TREE, cv2.CHAIN_APPROX_SIMPLE)
	cnts = sorted(cnts,key = cv2.contourArea, reverse = True)
	ret=[]
	#cv2.drawContours(image,cnts,-1,(255,0,0),3)
	for c in cnts:
		xmin,xmax,ymin,ymax=min_max(c)
		ret.append((image[ymin:ymax,xmin:xmax,:],[xmin,xmax,ymin,ymax],c))
	#cv2.imwrite("Contoured1.jpg",image)
	imgs,pos=compress(ret,image)
	print(pos)
	return imgs,pos

if __name__=="__main__":
	import matplotlib.pyplot as plt
	imgs,_ = get_smaller_images()
	for i in range(len(imgs)):
		cv2.imwrite(str(i)+"a.jpg",imgs[i])


