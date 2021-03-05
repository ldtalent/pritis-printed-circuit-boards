import cv2
import numpy
import imutils
import skimage
from easygui import *
from PIL import Image, ImageTk
import tkinter as tk
from tkinter import filedialog as fd
from skimage.metrics import structural_similarity

def func():
	print("Select your Reference Image")
	path1a = fd.askopenfilename()
	print("Select your Test Image")
	path1b = fd.askopenfilename()
	
	imageA = cv2.imread(path1a)
	imageB = cv2.imread(path1b)

	imageA = cv2.resize(imageA,(1200,600),interpolation=cv2.INTER_LINEAR)
	imageB = cv2.resize(imageB,(1200,600),interpolation=cv2.INTER_LINEAR)

	grayA = cv2.cvtColor(imageA, cv2.COLOR_BGR2GRAY)
	grayB = cv2.cvtColor(imageB, cv2.COLOR_BGR2GRAY)


	# Structural Similarity Index (SSIM)
	(score, diff) = structural_similarity(grayA, grayB, full=True)
	diff = (diff*255).astype("uint8")
	print("SSIM: {}".format(score))

	thresh = cv2.threshold(diff, 0, 255, cv2.THRESH_BINARY_INV | cv2.THRESH_OTSU)[1]

	cnts = cv2.findContours(thresh.copy(), cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE)
	cnts = imutils.grab_contours(cnts)

	#loop over the contours after threshold process
	p = 0
	for c in cnts:
		p=p+1
		(x, y, w, h) = cv2.boundingRect(c)
    		#cv2.rectangle(imageA, (x, y), (x+w, y+h), (0, 0, 255), 1)
		cv2.rectangle(imageB, (x, y), (x+w, y+h), (0, 0, 255), 1)
	print("Total number of defects in the image:",p)
	print("\n\n")

	kernel = numpy.ones((5, 5), numpy.uint8)

	#Dilation Morphology --> used to expand the original image
	dilation = cv2.dilate(thresh,kernel,iterations = 1)

	#Erosion Morphology --> used to shrink down the original image
	erosion = cv2.erode(thresh,kernel,iterations = 1)

	#Gradient is used to get the difference between Erosion and Dilation
	gradient = cv2.morphologyEx(thresh, cv2.MORPH_GRADIENT, kernel)

	#Opening --> Erosion followed by Dilation
	opening = cv2.morphologyEx(thresh, cv2.MORPH_OPEN, kernel)

	#Closing --> Dilation followed by Erosion
	closing = cv2.morphologyEx(thresh, cv2.MORPH_CLOSE, kernel)
	

	cv2.imshow("Displaying Defects", imageB)
	cv2.waitKey(0)
	cv2.destroyAllWindows()

while 1:
  #disp = "img.jpg"
  msg="PCB DEFECT DETECTION"
  choices = ["Detect","Exit"]
  reply   = buttonbox(msg, choices=choices)
  if reply ==choices[0]:
        func()
  if reply ==choices[1]:
        print("Thank you!")
        quit()

