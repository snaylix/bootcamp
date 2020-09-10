from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import (Dense,
                                     Flatten,
                                     Conv2D,
                                     MaxPooling2D,
                                     BatchNormalization,
                                     Dropout)
from tensorflow import keras
from tensorflow.keras.utils import to_categorical
from tensorflow.keras import backend as K
import numpy as np


(X_train, y_train), (X_test, y_test) = mnist.load_data()

X_train_reshaped = np.expand_dims(X_train, axis=3)
X_test_reshaped = np.expand_dims(X_test, axis=3)
y_train_reshaped = to_categorical(y_train)
y_test_reshaped = to_categorical(y_test)

print(X_train_reshaped.shape)
print(X_test_reshaped.shape)
print(y_train_reshaped.shape)
print(y_test_reshaped.shape)

K.clear_session()

INPUT_SHAPE = (28, 28, 1)
NUM_CLASSES = 10

model = Sequential([
    Conv2D(filters=64,
           kernel_size=(3),
           strides=(2, 2),
           activation='relu',
           input_shape=INPUT_SHAPE),
    Conv2D(filters=16,
           kernel_size=(3),
           activation='relu'),
    BatchNormalization(),
    MaxPooling2D(pool_size=(3, 3), strides=(2, 2)),
    BatchNormalization(),
    Dropout(0.5),
    Conv2D(filters=10, kernel_size=(3, 3), strides=(2, 2), activation='relu'),
    Flatten(),
    Dropout(0.5),
    BatchNormalization(),
    Dense(NUM_CLASSES, activation='softmax')
    ])

model.summary()

model.compile(optimizer='rmsprop',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

history = model.fit(X_train_reshaped,
                    y_train_reshaped,
                    epochs=20,
                    batch_size=500,
                    verbose=1,
                    validation_data=(X_test_reshaped, y_test_reshaped),
                    validation_split=0.1)
