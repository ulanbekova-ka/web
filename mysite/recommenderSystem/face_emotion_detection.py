from __future__ import division, print_function
import cv2
from deepface import DeepFace
import numpy as np

casc_path = '/Users/kulanbekova/PycharmProjects/project/mysite/recommenderSystem/static/recommenderSystem/haarcascade_frontalface_default.xml'


def recognize_emotion(image_file):
    model = DeepFace.build_model("Emotion")
    face_cascade = cv2.CascadeClassifier(casc_path)
    emotion_labels = ('angry', 'disgust', 'fear', 'happy', 'sad', 'neutral', 'surprise')

    image_data = np.frombuffer(image_file.read(), np.uint8)
    image = cv2.imdecode(image_data, cv2.IMREAD_COLOR)
    gray = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    print(gray)
    faces = face_cascade.detectMultiScale(gray, scaleFactor=1.3, minNeighbors=5)
    emotion = ""
    for (x, y, w, h) in faces:
        face_roi = gray[y:y + h, x:x + w]
        resized_face = cv2.resize(face_roi, (48, 48), interpolation=cv2.INTER_AREA)
        normalized_face = resized_face / 255.0
        reshaped_face = normalized_face.reshape(1, 48, 48, 1)
        preds = model.predict(reshaped_face)[0]
        emotion_idx = preds.argmax()
        emotion = emotion_labels[emotion_idx]
    return emotion

