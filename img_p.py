import os
from PIL import Image
import numpy as np
import cv2
import pickle
a=set()
recognizer = cv2.face.LBPHFaceRecognizer_create()

def img(sclass,img_loc):

    recognizer.read("train_folder/"+sclass+"/"+"trainer.yml")##

    fr=open("train_folder/"+sclass+"/"+"labels.pickle","rb")
    og_labels=pickle.load(fr)
    labels = {v:k for k,v in og_labels.items()}
    

    face=cv2.CascadeClassifier(r'cascades/data/haarcascade_frontalface_alt2.xml')
    a=set()

    img = cv2.imread(r'uploads/'+img_loc)

    gray = cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    faces = face.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5,minSize=(10, 10))##

    for (x,y,w,h) in faces:
        gray_face = cv2.resize(gray[y:y+h,x:x+w],(110,110))  #resize()
        gray_face_np = np.array(gray_face, 'uint8')
        id_,conf  =  recognizer.predict(gray_face_np)
        if conf<=80:
            print(conf)
            print(id_)
            if (id_ in labels):
                print(labels[id_])
                a.add(labels[id_])
        else:
            if (id_ in labels):
                print(conf,labels[id_])
        color = (22,0,255)
        stroke = 3
        cv2.rectangle(img, (x,y),(x+w,y+h),color,stroke)

        
    scale = 40

    width = int(img.shape[1] * scale/100)
    height = int(img.shape[0] * scale/100)

    dim = (width,height)

    im = cv2.resize(img, dim, interpolation = cv2.INTER_AREA)

    
    cv2.imwrite('static/detect/'+img_loc,im)
        #cv2.waitKey(10)###
    return(a)
