from __future__ import division, print_function
import os
import cv2
from deepface import DeepFace
import numpy as np
import librosa
import wave
from keras.models import load_model
import io
from pydub import AudioSegment

emotion_labels = ('angry', 'disgust', 'fear', 'happy', 'sad', 'neutral', 'surprise')


def emotion_by_face(image_file):
    model = DeepFace.build_model("Emotion")
    face_cascade = cv2.CascadeClassifier('/Users/kulanbekova/PycharmProjects/project/mysite/recommenderSystem/static/recommenderSystem/haarcascade_frontalface_default.xml')

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


def emotion_by_voice(audio_file):
    model = load_model('/Users/kulanbekova/PycharmProjects/project/mysite/recommenderSystem/static/recommenderSystem/speech_rec.h5')

    def extract_mfcc(filename):
        y, sr = librosa.load(filename, duration=3, offset=0.5)
        mfcc = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40).T, axis=0)
        return mfcc

    recording_path = blob_to_wav(audio_file)
    X_new = extract_mfcc(recording_path)
    X_new = np.expand_dims(X_new, axis=0)
    predictions = model.predict(X_new)
    predicted_emotion = emotion_labels[np.argmax(predictions)]
    return predicted_emotion


def blob_to_wav(blob):
    audio_data = blob.read()
    output_file_path = os.path.join(os.getcwd(), 'output.wav')
    with wave.open(output_file_path, 'wb') as output_file:
        output_file.setnchannels(1)  # Assuming mono audio
        output_file.setsampwidth(2)  # Assuming 16-bit audio
        output_file.setframerate(44100)  # Assuming 44.1 kHz sample rate
        output_file.writeframes(audio_data)

    return output_file_path