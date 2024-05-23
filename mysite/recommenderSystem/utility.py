from __future__ import division, print_function
import os
import cv2
from deepface import DeepFace
import numpy as np
import librosa
import wave
import pandas as pd
from tensorflow.python.keras.models import load_model

emotion_labels = ('angry', 'disgust', 'fear', 'happy', 'sad', 'neutral', 'surprise')


def emotion_by_face(image_data):
    nparr = np.frombuffer(image_data, np.uint8)
    image = cv2.imdecode(nparr, cv2.IMREAD_COLOR)
    result = DeepFace.analyze(image, enforce_detection=False)
    emotion = result[0]['dominant_emotion']
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


def get_genres_by_emotion(emotion):
    if emotion == 'neutral':
        return ["Action", "Histor", "Classic", "Business", "Biography", "Science", "Psychology", "Sci-Fi"]
    elif emotion == 'disgust':
        return ["Horror", "Thriller", "Mystery", "Fantasy", "Music", "Crime", "Western", "War"]
    elif emotion == 'fear':
        return ["Thriller", "Suspense", "Horror", "Travel", "Music", "Crime", "War", "Sci-Fi"]
    elif emotion == 'happy':
        return ["Comedy", "Humor", "Action", "Romance", "Mystery", "Detective", "Sport", "Adventure"]
    elif emotion == 'sad':
        return ["Drama", "Romance", "Fiction", "Fantasy", "Psychology", "Music", "War", "Family"]
    elif emotion == 'surprise':
        return ["Thriller", "Suspense", "Action", "Fiction", "Mystery", "Detective", "Adventure"]
    else:
        return ["Business", "Biography", "Self-help", "Fantasy", "Psychology", "Animation", "Family", "Sport"]


def get_ten_books(genres):
    df = pd.read_csv('/Users/kulanbekova/PycharmProjects/project/mysite/recommenderSystem/static/recommenderSystem/datasets/BooksDataset.csv')

    pattern = '|'.join(genres)

    df_filtered = df.dropna(subset=['Category'])
    genre_df = df_filtered[df_filtered['Category'].str.contains(pattern, case=False)]

    random_books = genre_df.sample(10)
    return random_books


def get_ten_movies(genres):
    df = pd.read_csv('/Users/kulanbekova/PycharmProjects/project/mysite/recommenderSystem/static/recommenderSystem/datasets/action.csv')

    pattern = '|'.join(genres)

    df_filtered = df.dropna(subset=['genre'])
    genre_df = df_filtered[df_filtered['genre'].str.contains(pattern, case=False)]

    random_movies = genre_df.sample(10)
    return random_movies
