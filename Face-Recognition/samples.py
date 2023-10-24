import cv2

cam = cv2.VideoCapture(0, cv2.CAP_DSHOW)
cam.set(3, 640)
cam.set(4, 480)

detector = cv2.CascadeClassifier(cv2.data.haarcascades+'haarcascade_frontalface_default.xml')

face_id = input('Enter User Id(Numeric): ')

print('Taking Samples of User')

count = 0
while True:
    ret, frame = cam.read()
    cvt_img = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    faces = detector.detectMultiScale(cvt_img, 1.3, 5)
    
    for (x, y, w, h) in faces:
        cv2.rectangle(cvt_img, (x, y), (x+w, y+h), (255, 0, 0), 2)
        count += 1
        
        cv2.imwrite("Jarvis/Face-Recognition/samples/face." + str(face_id) + '.' + str(count) + ".jpg", cvt_img[y:y+h, x:x+h])
        cv2.imshow('frame', frame)
        
    key = cv2.waitKey(100) & 0xff
    if key == 27:
        break
    elif count >= 50:
        break

print('Samples Taken, closing...')
cam.release()
cv2.destroyAllWindows()