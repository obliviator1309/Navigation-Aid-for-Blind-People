# -*- coding: utf-8 -*-
import cv2
from keras.models import load_model
import numpy as np
from statistics import mode
import imutils
import pyttsx3

# Some Utility Functions
def get_labels():
	return {0:'angry',1:'disgust',2:'fear',3:'happy',
		4:'sad',5:'surprise',6:'neutral'}

def load_detection_model(model_path):
	detection_model = cv2.CascadeClassifier(model_path)
	return detection_model

def detect_faces(detection_model, gray_image_array):
	return detection_model.detectMultiScale(gray_image_array, 1.3, 5)

def draw_bounding_box(face_coordinates, image_array, color):
	x, y, w, h = face_coordinates
	cv2.rectangle(image_array, (x, y), (x + w, y + h), color, 2)

def apply_offsets(face_coordinates, offsets):
	x, y, width, height = face_coordinates
	x_off, y_off = offsets
	return (x - x_off, x + width + x_off, y - y_off, y + height + y_off)

def draw_text(coordinates, image_array, text, color, x_offset=0, y_offset=0,
												font_scale=2, thickness=2):
	x, y = coordinates[:2]
	cv2.putText(image_array, text, (x + x_offset, y + y_offset),
				cv2.FONT_HERSHEY_SIMPLEX,
				font_scale, color, thickness, cv2.LINE_AA)

def preprocess_input(x, v2=True):
	x = x.astype('float32')
	x = x / 255.0
	if v2:
		x = x - 0.5
		x = x * 2.0
	return x

detection_model_path = '/home/fizzing/AI/minor2/project2/eMojify/haarcascade_frontalface_default.xml'
emotion_model_path = '/home/fizzing/AI/minor2/project2/eMojify/model.hdf5'
emotion_labels = get_labels()

frame_window = 10
emotion_offsets = (20, 40)

face_detection = load_detection_model(detection_model_path)
emotion_classifier = load_model(emotion_model_path, compile=False)
emotion_target_size = emotion_classifier.input_shape[1:3]

emotion_window = []

#cv2.namedWindow('window_frame')
video_capture = cv2.VideoCapture(1)
a=0
temp=[]
while True:
	bgr_image = video_capture.read()[1]
	bgr_image = imutils.rotate_bound(bgr_image, 90)
	gray_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2GRAY)
	rgb_image = cv2.cvtColor(bgr_image, cv2.COLOR_BGR2RGB)
	faces = detect_faces(face_detection, gray_image)

	for face_coordinates in faces:

		x1, x2, y1, y2 = apply_offsets(face_coordinates, emotion_offsets)
		gray_face = gray_image[y1:y2, x1:x2]
		try:
			gray_face = cv2.resize(gray_face, (emotion_target_size))
		except:
			continue

		gray_face = preprocess_input(gray_face, True)
		gray_face = np.expand_dims(gray_face, 0)
		gray_face = np.expand_dims(gray_face, -1)
		emotion_prediction = emotion_classifier.predict(gray_face)
		emotion_probability = np.max(emotion_prediction)
		emotion_label_arg = np.argmax(emotion_prediction)
		emotion_text = emotion_labels[emotion_label_arg]
		emotion_window.append(emotion_text)

		if len(emotion_window) > frame_window:
			emotion_window.pop(0)
		try:
			emotion_mode = mode(emotion_window)
		except:
			continue

		if emotion_text == 'angry':
			color = emotion_probability * np.asarray((255, 0, 0))
		elif emotion_text == 'sad':
			color = emotion_probability * np.asarray((0, 0, 255))
		elif emotion_text == 'happy':
			color = emotion_probability * np.asarray((255, 255, 0))
		elif emotion_text == 'surprise':
			color = emotion_probability * np.asarray((0, 255, 255))
		else:
			color = emotion_probability * np.asarray((0, 255, 0))

		color = color.astype(int)
		color = color.tolist()

		draw_bounding_box(face_coordinates, rgb_image, color)
		draw_text(face_coordinates, rgb_image, emotion_mode,
				  color, 0, -45, 1, 1)

		a = a+1
		if a%40==0:
			temp = []
		if emotion_mode not in temp:
			print(emotion_mode)
			temp.append(emotion_mode)
			engine = pyttsx3.init()
			engine.setProperty('voice', 'hindi')
			rate = engine.getProperty('rate')
			engine.setProperty('rate', rate-10)
			engine.say(emotion_mode)
			engine.runAndWait()

	bgr_image = cv2.cvtColor(rgb_image, cv2.COLOR_RGB2BGR)
	#print("display now")
	#cv2.imshow('test', rgb_image)
	cv2.imshow('window_frame', bgr_image)
	#print("display end")
	if cv2.waitKey(1) & 0xFF == ord('q'):
		f = open("flags.txt","w")
		f.write("0")
		f.close()
		cv2.destroyAllWindows()
		break
