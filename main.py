import os
import pyttsx3
import speech_recognition as sr
import time 

f = open("flags.txt","w")
f.write("1")
f.close()

while(True):
	f = open("flags.txt","r")
	a = f.read(1)
	print(a)
	f.close()
	if(a=='0'):
		r = sr.Recognizer()
		with sr.Microphone() as source:
			print("Speak Anything :")
			audio = r.listen(source)
			try:
				text = r.recognize_google(audio)
				text = text.lower()
				print("You said : {}".format(text))
				if text.find('emotion')!=-1 or text.find('mood')!=-1 or text.find('haal')!=-1 or text.find('bhav')!=-1 : 
					print("-------------------------------------------")
					print("kisi ke andruni emotions to me nhi bta skta")
					print("Lekin chehre ke bhav zaroor bta skta hu") 
					print("-------------------------------------------")
					os.system("python eMojify/main.py")
				elif text.find('who')!=-1 or text.find('kon')!=-1 or text.find('kaun')!=-1 or text.find('face')!=-1 or text.find('chehra')!=-1 : 
					os.system("python face_recognition/facerec_from_webcam_faster.py")
				elif (text.find('distance')!=-1 or text.find('doori')!=-1 or text.find('duri')!=-1) and (text.find('person')!=-1 or text.find('man')!=-1 or text.find('aadmi')!=-1 or text.find('insaan')!=-1 or text.find('hath')!=-1 or text.find('insan')!=-1 or text.find('haath')!=-1) :
					engine = pyttsx3.init()
					engine.setProperty('voice', 'hindi')
					engine.say("Please show your hand towards the camera")
					engine.runAndWait()
					print("Please show your hand towards the camera")
					os.system("python hand_distance/hand_detection.py")
				elif text.find('navigate')!=-1 or text.find('road')!=-1 or text.find('navigation')!=-1 or text.find('direction')!=-1 or text.find('disha')!=-1 or text.find('rasta')!=-1 or text.find('raasta')!=-1 or text.find('directions')!=-1 : 
					os.system("python navigation_blind/Code/detection.py")
				elif text.find('text')!=-1 or text.find('ocr')!=-1 or text.find('likha')!=-1 : 
					engine = pyttsx3.init()
					engine.setProperty('voice', 'hindi')
					rate = engine.getProperty('rate')
					engine.setProperty('rate', rate-30)
					engine.say("Please hold the Camera still over the text")
					engine.runAndWait()
					print("Please hold the Camera still over the text")
					time.sleep(3)
					os.system("python text_recognition/text_recognition.py")
				elif text.find('object')!=-1 : 
					f = open("flags.txt","w")
					f.write("1")
					f.close()
					os.system("python object_detection/object_detection_webcam.py")
				elif text.find('exit')!=-1 or text.find('close')!=-1 or text.find('band')!=-1 or text.find('baand')!=-1 : 
					break
			except:
				print("Maaf kijiye mujhe samajh nhi aaya")
				print("Sorry could not recognize what you said")
				engine = pyttsx3.init()
				engine.setProperty('voice', 'hindi')
				engine.say("Sorry could not recognize what you said")
				engine.runAndWait()
	else:
		os.system("python object_detection/object_detection_webcam.py")
