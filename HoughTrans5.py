import cv2
import numpy as np
import math
from numpy import interp
from HardwareControl_1 import *
import time



seed_pt =[] 

seed_pt.append(311)
seed_pt.append(261)

def onmouse(event, x, y, flags, param):
       	if flags & cv2.EVENT_FLAG_LBUTTON:
			seed_pt.append(x) 
			seed_pt.append(y)
			print seed_pt






def checkOpt(img):
		i=0
	
		blankImage1=np.zeros(img.shape,np.uint8)
		#cv2.line(blankImage1,(0,seed_pt[1]),(img.shape[1],seed_pt[1]),255,4)
		cv2.line(blankImage1,(0,seed_pt[1]-50),(img.shape[1],(seed_pt[1]-50)),25,1)

		blankImage1 &=img
		
		_,img1 = cap.read()
	
		
		gray  = cv2.cvtColor(blankImage1 ,cv2.COLOR_BGR2GRAY)
		#img = cv2.Canny(gray,10,80,apertureSize = 3)
	
		blankImage1 = gray.copy()

		contours,hierarchy=cv2.findContours(blankImage1,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)

		for cnt in contours:
			i=i+1
			cv2.drawContours(blankImage1,cnt,-1,(255,255,255),2)


		cv2.imshow("Obstacle Line",blankImage1)
		cv2.setMouseCallback("Obstacle Line",onmouse)
		cv2.waitKey(0)
		#cv2.waitKey(0)

		if i >1 :
			return 1

		return 0

def checkDivrgn(img,img2):
	

		point = []
		count =0
		
		blankImage1=np.zeros(img.shape,np.uint8)
		#cv2.line(blankImage1,(0,seed_pt[1]),(img.shape[1],seed_pt[1]),255,4)
		cv2.line(blankImage1,(0,seed_pt[1]-50),(img.shape[1],(seed_pt[1]-50)),250,1)

		blankImage1 &=img
		

		#cv2.imshow("divrgn img1",blankImage1)
		#cv2.waitKey(0)
		
		gray  = cv2.cvtColor(blankImage1 ,cv2.COLOR_BGR2GRAY)
		#img = cv2.Canny(gray,10,80,apertureSize = 3)
	
		blankImage1 = gray.copy()

		contours,hierarchy=cv2.findContours(blankImage1,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)



		for cnt in contours:
			count = count +1 
			cv2.drawContours(blankImage1,cnt,-1,(255,0,0),3)

		img1 = np.zeros(img.shape,np.uint8)
		#minLineLength = 100
		#maxLineGap = -60
		minLineLength = 50
		maxLineGap = -120
		lines = cv2.HoughLinesP(edges,1,(np.pi/190),5,minLineLength,maxLineGap)

		#print lines

		for x1,y1,x2,y2 in lines[0]:
	    		cv2.line(img1,(x1,y1),(x2,y2),(0,250,0),7)
			
			point.append(x1)
			point.append(x2)

		print "Dirvgn"
		print point
		

		blankImage1 = cv2.cvtColor(blankImage1 ,cv2.COLOR_GRAY2BGR)

		blankImage1 |=img2
		cv2.imshow("divrgn img1",blankImage1)
		cv2.imshow("Image12399",img1)
		cv2.waitKey(0)
		
		point.sort()
		print "Diff",(point[0] - point[len(point)-1])
		if count == 2 : 

			if(( point[len(point)-1]-point[0])  > 550):
				print "Divrgn1234"
				return 1	
			else :
				print "May be "
	
		else:
			print "no Divrgn  "

		return 0	
				
	
def getAngle(img):

		midPoints = []
		
		blankImage1=np.zeros(img.shape,np.uint8)
		#cv2.line(blankImage1,(0,seed_pt[1]),(img.shape[1],seed_pt[1]),255,4)
		cv2.line(blankImage1,(0,seed_pt[1]-13),(img.shape[1],(seed_pt[1]-13)),255,4)

		blankImage1 &=img
		

		
		gray  = cv2.cvtColor(blankImage1 ,cv2.COLOR_BGR2GRAY)
		#img = cv2.Canny(gray,10,80,apertureSize = 3)
	
		blankImage1 = gray.copy()

		contours,hierarchy=cv2.findContours(blankImage1,cv2.RETR_LIST,cv2.CHAIN_APPROX_NONE)



		for cnt in contours:
			
			cv2.drawContours(blankImage1,cnt,-1,(255,255,255),4)
			M=cv2.moments(cnt)
			#print M 
			if (M['m00']!= 0): 
				midPoints.append(int(M['m10']/M['m00']))
				midPoints.append(int(M['m01']/M['m00']))
 			 
 			#cv2.imshow("Image1234",blankImage1)
			#cv2.waitKey(0)


		#print midPoints
		x1=midPoints[0]
		y1=midPoints[1]
		#x2=midPoints[2]
		#y2=midPoints[3]
		
		
		x2= seed_pt[0]
		y2= seed_pt[1]


		

		cv2.line(blankImage1,(x1,y1),(x2,y2),255,2)
		
		X=math.fabs(y2-y1)/math.sqrt((math.pow(math.fabs(x2-x1),2) + math.pow(math.fabs(y2-y1),2)))
		theta=np.arcsin(X)
		theta = math.degrees(theta)
	
		
		cv2.imshow("GETAngle Line",blankImage1)
		cv2.waitKey(0)

		#if (y1<y2) and (x1<x2):
		#	theta = 180 - theta

		#elif (y1>y2) and (x1>x2):
		#	theta = 180 - theta

		if x2 > x1 and y2 > y1:

			theta = 180 - theta
	
		cv2.imshow("Image1234",blankImage1)
		#cv2.waitKey(0)
				

		cv2.destroyWindow("Image1234")
		
		return theta


def  gammaTrans(img , x):


	size = (256,1,1)
	lut = np.zeros(size,dtype=np.uint8)	

	for i in range(0,256):
		lut[i,0] = interp(pow(interp(i,[0,255],[0,1]),x),[0,1],[0,255])

	img=cv2.LUT(img,lut)
	
	return img


cap = cv2.VideoCapture(1)
obj1 = HardwareControl()
obj1.serialOn()

frame = 0 


for i in range(0,20) :
	_,img = cap.read()

while(1):


	for i in range(0,10) :
		 _,img = cap.read()


	_,img = cap.read()
	
	#img = cv2.imread('sampleImg6.jpg')
	#img = gammaTrans(img,2)	

	img = cv2.GaussianBlur(img,(5,5),0)


	#img1 = img.copy()
	frame = frame + 1
	
	gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	edges = cv2.Canny(gray,40,120,apertureSize = 3)
	
	#temp Data


	
	##temp End

	#cv2.imshow("main",img)
	cv2.imshow("edges",edges)
	#cv2.waitKey(0)
	
	img1 = np.zeros(img.shape,np.uint8)
	#minLineLength = 100
	#maxLineGap = -60
	minLineLength = 50
	maxLineGap = -120
	lines = cv2.HoughLinesP(edges,1,(np.pi/190),5,minLineLength,maxLineGap)

	#print lines

	for x1,y1,x2,y2 in lines[0]:
	    cv2.line(img1,(x1,y1),(x2,y2),(0,250,0),5)
	cv2.line(img1,(0,(seed_pt[1]+5)),(img.shape[1],(seed_pt[1]+5)),(200,0,0),1)
	
	
	cv2.line(img1,(0,(seed_pt[1]-155)),(img.shape[1],(seed_pt[1]-155)),(200,0,0),1)
	

	blankImage1=np.zeros((img.shape[0]+2,img.shape[1]+2),np.uint8)		
	cv2.floodFill(img1,blankImage1,(seed_pt[0],seed_pt[1]), (255, 255, 255))
	#cv2.imshow("HoughP",img1)

	size1 = (256,1,1)
	lut = np.zeros(size1,dtype=np.uint8)

	for i in range(0,254):
		lut[i,0] = 0

	for i in range(255,256):
		lut[i,0] = 255
	
	img1=cv2.LUT(img1,lut)

	cv2.imshow("swa",img1)

	#cv2.waitKey(0)

	#gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	#edges = cv2.Canny(gray,0,127,apertureSize = 3)

		

	if  checkOpt(img1) :

		
		if checkDivrgn(img1,img):

			print "stop divgn"	
		else :
			print "stop opt"	
		
		obj1.forwardStop()
		obj1.write()	
		break

	

	angle = getAngle(img1)
	print angle
	img |= img1

	cv2.imshow("Final",img)

	#cv2.waitKey(0)


	#angle = 25
	
		
	if int(angle) > 90 :
		
	   	if int(angle)>105:
			angle = 105

		diff = int(angle) - 90
		angle = 90- diff

		angle = int(angle)
		obj1.angle = angle-2
		#obj1.setAngle()
		print obj1.angle
		#obj1.resetAngle()
		#obj1.write()
		
	elif angle < 90 :
		if int(angle)<75:
			angle = 75
		diff = 90 - int(angle)
		angle = 90 + diff-4

		angle = int(angle)
		obj1.angle = angle
		#obj1.setAngle()
		print obj1.angle
		#obj1.resetAngle()
		#obj1.write()
	else:
		angle = 90
		obj1.angle = angle
		#obj1.setAngle()
		print obj1.angle
		#obj1.resetAngle()
		#obj1.write()

	
	##print "RAngle"
	#print obj1.getAngle()
	#print "RAngle"
	
	#cv2.waitKey(0)
	obj1.setAngle()		
	#obj1.forward()
	obj1.write()

	#obj1.forward()
	
	obj1.writeAngle()
	#obj1.forwardStop()
	
	obj1.resetAngle()
	obj1.forward()
	obj1.write()
	#obj1.forward()
	#obj1.write()
	
	#cv2.waitKey(0)
	time.sleep(0.6)
	#for i in range(0,10000,1):
		#print "forward"

	obj1.forwardStop()
	obj1.write()
		
	#if(cv2.waitKey(0)==1048608):
	if(frame == 30)	:	
		obj1.forwardStop()
		obj1.write()	
		print "stop"		
		break
	print "continued"			
		
		
	#cv2.setMouseCallback("Final",onmouse)
	
	

	
	cv2.imshow("Final123",img)
		
	cv2.setMouseCallback("Final123",onmouse)
	cv2.waitKey(0)
	
	#gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
	
	
	

	#imgn = cv2.bitwise_not(gray)

	#cv2.imshow("Final1",imgn)
	#cv2.waitKey(0)
	"""
	if(cv2.waitKey(0)==1048608):
			
			print "stop"		
			break
	print "continued"			
		
	"""	
		


cap.release()
cv2.destroyAllWindows()
