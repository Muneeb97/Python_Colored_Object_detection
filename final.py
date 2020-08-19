#complete with RGB object tracking, grid and position detection
import cv2
import numpy as np

cap=cv2.VideoCapture('http://192.168.137.157:4747/video')

def draw_grid(img, line_color=(0, 0, 0), thickness=1, type_=cv2.LINE_AA, pxstep=128, pystep=96):

    x = pxstep
    y = pystep
    while x < img.shape[1]:
        #print(x,'x_grid')
        cv2.line(img, (x, 0), (x, img.shape[0]), color=line_color, lineType=type_, thickness=thickness)
        x += pxstep

    while y < img.shape[0]:
        #print(y,'y_grid')
        cv2.line(img, (0, y), (img.shape[1], y), color=line_color, lineType=type_, thickness=thickness)
        y += pystep

def loc(x,y, pxstep=128, pystep=96):
	row=1
	col=1
	x_prv=0
	y_prv=0
	x_nxt=pxstep
	y_nxt=pystep
	z_r=True
	z_c=True

	while z_c == True:
		if(x <= x_nxt and x >= x_prv) : 
			print('column # ',col)
			z_c = False
		else:
			x_prv = pxstep
			x_nxt += pxstep 
			col += 1
	while z_r == True:
		if(y <= y_nxt and y >= y_prv) : 
			print('row # ',row)
			z_r = False
		else:
			y_prv = pystep
			y_nxt += pystep 
			row += 1

def cont_r(contours_r,img) :
	if len(contours_r)>0:
		contour_r= max(contours_r,key=cv2.contourArea)
		area = cv2.contourArea(contour_r)
		if area>800: 
			x,y,w,h = cv2.boundingRect(contour_r)	
			img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
			img=cv2.circle(img,(int((2*x+w)/2),int((2*y+h)/2)),5,(255,0,0),-1)
			img=cv2.line(img,(5,5),(int((2*x+w)/2),int((2*y+h)/2)),(0,255,0),2)
			loc(int((2*x+w)/2),int((2*y+h)/2))

			xc=int((2*x+w)/2) 
			yc=int((2*y+h)/2)

			s= 'x:'+ str(xc)+ 'y:'+str(yc)
			
			cv2.putText(img,s+'R',(x-20,y-5),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255),1,cv2.LINE_AA)

def cont_b(contours_b,img):
	if len(contours_b)>0:
		contour_b= max(contours_b,key=cv2.contourArea)
		area = cv2.contourArea(contour_b)
		if area>800: 
			x,y,w,h = cv2.boundingRect(contour_b)	
			img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
			img=cv2.circle(img,(int((2*x+w)/2),int((2*y+h)/2)),5,(255,0,0),-1)
			img=cv2.line(img,(5,5),(int((2*x+w)/2),int((2*y+h)/2)),(0,255,0),2)
			loc(int((2*x+w)/2),int((2*y+h)/2))

			xc=int((2*x+w)/2) 
			yc=int((2*y+h)/2)

			s= 'x:'+ str(xc)+ 'y:'+str(yc)
			
			cv2.putText(img,s+'B',(x-20,y-5),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255),1,cv2.LINE_AA)
	
def cont_g(contours_g,img):
	if len(contours_g)>0:
		contour_g= max(contours_g,key=cv2.contourArea)
		area = cv2.contourArea(contour_g)
		if area>800: 
			x,y,w,h = cv2.boundingRect(contour_g)	
			img = cv2.rectangle(img,(x,y),(x+w,y+h),(255,0,0),2)
			img=cv2.circle(img,(int((2*x+w)/2),int((2*y+h)/2)),5,(255,0,0),-1)
			img=cv2.line(img,(5,5),(int((2*x+w)/2),int((2*y+h)/2)),(0,255,0),2)
			loc(int((2*x+w)/2),int((2*y+h)/2))

			xc=int((2*x+w)/2) 
			yc=int((2*y+h)/2)

			s= 'x:'+ str(xc)+ 'y:'+str(yc)
			
			cv2.putText(img,s+'G',(x-20,y-5),cv2.FONT_HERSHEY_SIMPLEX, 0.5, (0,0,255),1,cv2.LINE_AA)


while(1):
	_, img = cap.read()
	if img is None:
		break
	
	draw_grid(img)
	    
	hsv=cv2.cvtColor(img,cv2.COLOR_BGR2HSV)

	blue_lower=np.array([110,50,50],np.uint8)
	blue_upper=np.array([130,255,255],np.uint8)
	
	lower_red = np.array([155,25,0])
	upper_red = np.array([179,255,255])

	lower_green= np.array([36, 25, 25])
	upper_green= np.array([70, 255,255])

	red=cv2.inRange(hsv,lower_red,upper_red)	
	blue=cv2.inRange(hsv,blue_lower,blue_upper)	
	green=cv2.inRange(hsv,lower_green,upper_green)

	kernal = np.ones((5 ,5), "uint8")

	blue=cv2.dilate(blue,kernal)
	red=cv2.dilate(red,kernal)
	green=cv2.dilate(green,kernal)

	img=cv2.circle(img,(5,5),5,(0,0,255),-1)
	img_c=img

	(contours_b,hierarchy_b)=cv2.findContours(blue,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	(contours_r,hierarchy_r)=cv2.findContours(red,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
	(contours_g,hierarchy_g)=cv2.findContours(green,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

	cont_b(contours_b,img)
	#------------------------------------------------------
	cont_r(contours_r,img)
	#------------------------------------------------------
	cont_g(contours_g,img)


	cv2.imshow("Mask_b",blue)
	cv2.imshow("Mask_r",red)
	cv2.imshow("Mask_g",green)
	cv2.imshow("RGB Object Tracking",img)
	
	if cv2.waitKey(1)== ord('q'):
		break

cap.release()
cv2.destroyAllWindows()