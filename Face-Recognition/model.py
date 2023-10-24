import cv2
import numpy as np
from PIL import Image
import os

path = 'Jarvis/Face-Recognition/samples/'

recognizer = cv2.face.LBPHFaceRecognizer_create()
detector = cv2.CascadeClassifier('Jarvis/Face-Recognition/haarcascade_frontalface_default.xml')

def fetch(path):
    imgPaths = [os.path.join(path, dir) for dir in os.listdir(path)]
    sampleFaces = []
    ids = []
    
    for img in imgPaths:
        gray_img = Image.open(img).convert('L')
        img_arr = np.array(gray_img, 'uint8')
        
        id = int(os.path.split(img)[-1].split('.')[1])
        faces = detector.detectMultiScale(img_arr)
        for (x, y, w, h) in faces:
            sampleFaces.append(img_arr[y:y+h, x:x+w])
            ids.append(id)
    
    return sampleFaces, ids

print('Training')

faces, ids = fetch(path)
recognizer.train(faces, np.array(ids))

recognizer.write('Jarvis/Face-Recognition/model/trainer.yml')

print('Model Trained')