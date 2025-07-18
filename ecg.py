import pandas as pd
import numpy as np
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import LSTM, Dense
from tensorflow.keras.utils import to_categorical
from sklearn.preprocessing import LabelEncoder

df = pd.read_csv("ecg_dataset_LSDTM.csv")
X = df.drop("Label", axis=1).values
y = LabelEncoder().fit_transform(df["Label"])
y = to_categorical(y)

X = X.reshape((X.shape[0], 100, 1))  # 100 time steps, 1 feature

model = Sequential()
model.add(LSTM(64, input_shape=(100, 1)))
model.add(Dense(2, activation='softmax'))
model.compile(optimizer='adam', loss='categorical_crossentropy', metrics=['accuracy'])
model.fit(X, y, epochs=10, batch_size=16)

model.save("app/model/lstm_model.h5")
print("✅ LSTM model saved.")