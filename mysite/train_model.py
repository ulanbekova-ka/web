import pandas as pd
import numpy as np
import os
import librosa
import librosa.display
from tensorflow.python.keras.models import Sequential, save_model
from tensorflow.python.keras.layers import Dense, LSTM, Dropout


paths = []
labels = []

for dirname, _, filenames in os.walk('/Users/kulanbekova/PycharmProjects/learningAI/kaggle/input/input'):
    for filename in filenames:
        if filename.endswith('.wav'):
            paths.append(os.path.join(dirname, filename))
            label = filename.split('_')[-1]
            label = label.split('.')[0]
            labels.append(label.lower())

    if len(paths) == 2800:
        break
print('Dataset is Loaded')

## Create a dataframe
df = pd.DataFrame()
df['speech'] = paths
df['label'] = labels
df.head()


def extract_mfcc(filename):
    y, sr = librosa.load(filename, duration=3, offset=0.5)
    mfcc = np.mean(librosa.feature.mfcc(y=y, sr=sr, n_mfcc=40).T, axis=0)
    return mfcc

X_mfcc = df['speech'].apply(lambda x: extract_mfcc(x))
X = [x for x in X_mfcc]
X = np.array(X)

X = np.expand_dims(X, -1)

from sklearn.preprocessing import OneHotEncoder
enc = OneHotEncoder()
y = enc.fit_transform(df[['label']])
y = y.toarray()

model = Sequential([
    LSTM(256, return_sequences=False, input_shape=(40,1)),
    Dropout(0.2),
    Dense(128, activation='relu'),
    Dropout(0.2),
    Dense(64, activation='relu'),
    Dropout(0.2),
    Dense(7, activation='softmax')
])

model.compile(loss='categorical_crossentropy', optimizer='adam', metrics=['accuracy'])
model.summary()

history = model.fit(X, y, validation_split=0.2, epochs=50, batch_size=64)


save_model(model, '/Users/kulanbekova/PycharmProjects/project/mysite/recommenderSystem/static/recommenderSystem/speech_rec.h5')