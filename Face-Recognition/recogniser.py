import cv2

recognizer = cv2.face.LBPHFaceRecognizer_create()
recognizer.read('Jarvis/Face-Recognition/model/trainer.yml')
cascadePath = 'Jarvis/Face-Recognition/haarcascade_frontalface_default.xml'
classifier = cv2.CascadeClassifier(cascadePath)

font = cv2.FONT_HERSHEY_SIMPLEX

id = 2

names = ['', 'kush']

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(3, 640)
cam.set(4, 480)

minW = 0.1*cam.get(3)
minH = 0.1*cam.get(4)

while True:
    ret, frame = cam.read()
    cvt_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    
    faces = classifier.detectMultiScale(
        cvt_img,
        scaleFactor=1.2,
        minNeighbors=5,
        minSize=(int(minW), int(minH)),
    )
    
    for (x, y, w, h) in faces:
        cv2.rectangle(frame, (x, y), (x+w, y+h), (0, 255, 100), 2)
        id, acc = recognizer.predict(cvt_img[y:y+h, x:x+w])
        if acc < 100:
            id = names[id]
            acc = '  {0}%'.format(round(100-acc))
        
        else:
            id = 'unknown'
            acc = '  {0}%'.format(round(100-acc))
        
        cv2.putText(frame, str(id), (x+5, y-5), font, 1, (255, 255, 255), 2)
        cv2.putText(frame, str(acc), (x+5, y+h-5), font, 1, (255, 255, 0), 1)
    
    cv2.imshow('frame', frame)
    
    key = cv2.waitKey(10) & 0xff
    if key == 27:
        break

print('Exiting Program...')
cam.release()
cv2.destroyAllWindows()