import cv2
import numpy as np
import time
import threading
import math
import random

from flask import Flask, render_template

print(cv2.__version__)

kernel = (13,13)

starting = None

speedThresh = 0.6
mavSize = 30
timeThresh = 1
running = True

xPrev = 0
yPrev = 0
delta = 1000000
deltas = []
stopped = False
car = False
beginTime = time.time()
timeElapsed = 0
carPresent = False
currentTime = 0
master_stopped = False
numberStopped = 0
numberNotStopped = 0

for i in range (0, mavSize):
	deltas.append(10000)

def resolve_delta(xCurr,yCurr):
	global xPrev
	global yPrev
	global delta
	delta = math.sqrt((yCurr - yPrev) ** 2 + (xCurr - xPrev) **2)
	xPrev = xCurr
	yPrev = yCurr
	return delta

def find_moving_average(arr):
	total = 0
	for a in arr:
		total+=a

	return (total/len(arr))


app = Flask(__name__)

@app.route('/')
def index():

	return render_template('index.html', numStopped = numberStopped, numNotStopped = numberNotStopped)

if __name__ == '__main__':

	if (random.randint(0,2) == 1):
		cap = cv2.VideoCapture('video_files/GreyToyota.mp4')
	else:
		cap = cv2.VideoCapture('video_files/LotsOfCarsTrim.mp4')
	cap = cv2.VideoCapture('video_files/LotsOfCarsTrim.mp4')
	try:
		while(True):
			ret, img = cap.read()
			if(not ret):
				break
			img = cv2.resize(img, (640,320))

			gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
			filtered = cv2.blur(gray,kernel)
		
			if starting is None:
				starting = filtered
			
			image_sub = cv2.absdiff(starting, filtered)
			ret,thresh1 = cv2.threshold(image_sub,20,255,cv2.THRESH_BINARY)

			opening = cv2.morphologyEx(thresh1, cv2.MORPH_OPEN, kernel)

			#find the contours
			opening,contours,hierarchy = cv2.findContours(opening, 1, 2)

			for cnt in contours:

				area = cv2.contourArea(cnt)
				currentTime = time.time()

				if(area > 3000):

					if (not carPresent):
						beginTime = currentTime

					timeElapsed = currentTime - beginTime
					carPresent = True
					x,y,w,h = cv2.boundingRect(cnt)

					d = resolve_delta(x,y)
					deltas.append(d)
					deltas.pop(0)
					moving_average = find_moving_average(deltas)

					if (moving_average < speedThresh):
						cv2.rectangle(img,(x,y),(x+w,y+h),(0,0,255),2)
						#cv2.drawContours(img,contours,-1,(0,0,255),3)
						stopped = True

					else:
						cv2.rectangle(img,(x,y),(x+w,y+h),(0,255,0),2)
						#cv2.drawContours(img,contours,-1,(0,255,0),3)

				else: 
					if (((timeElapsed + beginTime) <= currentTime-0.3) and carPresent):
						master_stopped = stopped
						carPresent = False
						print('Car has exitted the frame!')
						stopped = False

				cv2.imshow('video', img)

			if cv2.waitKey(33) == 27:
				break

		cap.release()
		cv2.destroyAllWindows()				

	except:
		pass
		
	f = open("fileSystem.txt", "a")
	if (master_stopped):
		f.write("1\n")
	else:
		f.write("0\n")
	f.close()

	f = open("fileSystem.txt", "r")
	data=f.read().replace('\n', '')
	for d in data:
		if(d == '1'):
			numberStopped += 1
		else:
			numberNotStopped += 1
	print(numberStopped)
	print(numberNotStopped)
	app.run(debug=True, use_reloader=False, host='0.0.0.0')

