from django.core.files.storage import default_storage
from django.core.files.base import ContentFile
from django.conf import settings

from django.core.exceptions import ValidationError

import cv2
import numpy as np
import os, sys
import glob
import pickle
import dlib
import tensorflow as tf
from tensorflow.keras.preprocessing import image
import imutils

detector = dlib.get_frontal_face_detector()

face_shape_model = tf.keras.models.load_model('face-shape-recognizer.h5')

labels = ['Heart', 'Oblong', 'Oval', 'Round', 'Square']

def face_detect(image):
    os.environ['TF_CPP_MIN_LOG_LEVEL'] = '2'

    image_path = default_storage.save("tmp/temp.jpg", ContentFile(image.read()))
    tmp_file = os.path.join(settings.MEDIA_ROOT, image_path)

    try:
        img = cv2.imread(tmp_file)
        gray = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)
        dets = detector(gray, 0)

        if len(dets) == 0:
            predicted_label = "Face not found!"

        for det in dets:
            x1 = det.left()
            y1 = det.top()
            x2 = det.right()
            y2 = det.bottom()

            crop_img = gray[y1:y2, x1:x2]
            resize_img = cv2.resize(crop_img, (190,250))

            img = np.expand_dims(resize_img, axis=0)
            img = np.expand_dims(img, axis=-1)
            img = np.vstack([img])
            print(img.shape)
            y_pred = np.argmax(face_shape_model.predict(img,verbose=0), axis=1)[0]

            predicted_label = labels[y_pred]
        
        response = {"result": predicted_label}
    except:
        response = {"result": None}
    
    default_storage.delete(tmp_file)
    
    return response

