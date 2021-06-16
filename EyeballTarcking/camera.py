from django.shortcuts import render,redirect
from cv2 import cv2
import os,urllib.request
import numpy as np
from django.conf import settings
from django.http.response import StreamingHttpResponse
from gaze_tracking import GazeTracking
from django.contrib import messages
import dlib
import pickle



#gaze = GazeTracking()
#camera = cv2.VideoCapture(0)
#print('monojit camera outside function')
def gen_frames():
	gaze = GazeTracking()
	camera = cv2.VideoCapture(0)
	while True:
		success,frame=camera.read()
		if not success:
			break
		else:
			gaze.refresh(frame)
			frame=gaze.annotated_frame()
			text=""
			#print(text)
			if gaze.is_blinking():
				text="blinking"
			elif gaze.is_right():
				text="looking right"
			elif gaze.is_left():
				text = "looking left"
			elif gaze.is_center():
				text="looking center"
			resize = cv2.resize(frame,(1000,530),interpolation=cv2.INTER_LINEAR)
			frame_flip=cv2.flip(resize,1)
			cv2.putText(frame_flip, text, (90, 60), cv2.FONT_HERSHEY_DUPLEX, 1.6, (147, 58, 31), 2)
			_,buffer=cv2.imencode('.jpg',frame_flip)
			frame=buffer.tobytes()
			yield(b'--frame\r\n'
					b'Content-Type:image/jpeg\r\n\r\n'+ frame + b'\r\n')

def leave(request):
	if request.method == 'POST':
		return redirect('/') 

def leaveprof(request):
	if request.method == 'POST':
		return redirect('/')

			



