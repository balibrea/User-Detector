import cv2
import socket

recognizer = cv2.face.createLBPHFaceRecognizer()
recognizer.load('trainer/trainer.yml')
cascadePath = "Classifiers/face.xml"
faceCascade = cv2.CascadeClassifier(cascadePath)
path = 'dataSet'

isCon = False

host = 'localhost'
port = 2323
size = 1024

s = 0
nbr_predicted = 0


def Open(host, port):
    s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    s.connect((host, port))
    return s


def SendData(conn, intValue):
    size = 7
    bStr_LEDValue = bin(intValue).split('0b')[1].zfill(size)  # Convert from int to binary string
    conn.send(bStr_LEDValue + '\n')  # Newline is required to flush the buffer on the Tcl server


cam = cv2.VideoCapture(0)
font = font = cv2.FONT_HERSHEY_SIMPLEX  # cv2.InitFont(cv2.cv.CV_FONT_HERSHEY_SIMPLEX, 1, 1, 0, 1, 1) #Creates a font
while True:
    ret, im = cam.read()
    gray = cv2.cvtColor(im,cv2.COLOR_BGR2GRAY)
    faces = faceCascade.detectMultiScale(gray, scaleFactor=1.2, minNeighbors=5, minSize=(100, 100), flags=cv2.CASCADE_SCALE_IMAGE)
    for(x, y, w, h) in faces:
        nbr_predicted, conf = recognizer.predict(gray[y:y+h,x:x+w])
        cv2.rectangle(im,(x,y),(x+w,y+h),(0,225,0),2)
        if(nbr_predicted == 32):
             nbr_predicted = 'Imandra'
        elif(nbr_predicted == 12):
             nbr_predicted = 'Tomas'
        elif(nbr_predicted == 33):
             nbr_predicted='Balibrea'

        if conf > 50 and nbr_predicted == 'Balibrea':
            # ===== Put network code Here ===========
            try:
                if not isCon:
                    s = Open(host, port)
                    #print s.recv(size)
                    s.send("0!")
                    isCon = True
                else:
                    #print s.recv(size)
                    s.send("0!")
            except socket.error:
                print "No connection available."
            print "User id: " + nbr_predicted
        else:
            try:
                if not isCon:
                    s = Open(host, port)
                    #print s.recv(size)
                    s.send("01")
                    isCon = True
                else:
                    #print s.recv(size)
                    s.send("01")
            except socket.error:
                print "No connection available."

        #print s.recv(size)
        cv2.putText(im, str(nbr_predicted)+" - " + str(conf), (x, y-10), font, 0.55, (255, 255, 255), 1)
            
    cv2.imshow('User Tracking', im)
    if cv2.waitKey(20) & 0xFF == ord('q'):
        try:
            s.close()
        except AttributeError:
            pass
        break

