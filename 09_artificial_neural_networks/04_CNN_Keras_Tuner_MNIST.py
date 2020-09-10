from kerastuner import HyperModel
from kerastuner.tuners import Hyperband
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


# import Keras Tuner Hypermodel Class
class CNNHyperModel(HyperModel):
    def __init__(self, input_shape, num_classes):
        self.input_shape = input_shape
        self.num_classes = num_classes

    def build(self, hp):
        model = keras.Sequential()
        model.add(
            Conv2D(
                filters=32,
                kernel_size=(3),
                strides=(2, 2),
                activation='relu',
            )
        )
        model.add(
            Conv2D(
                filters=hp.Choice(
                    'num_filters_1',
                    values=[16, 32],
                    default=16,
                ),
                activation='relu',
                kernel_size=3
            )
        )
        model.add(BatchNormalization())
        model.add(MaxPooling2D(pool_size=(3, 3), strides=(2, 2)))
        model.add(BatchNormalization())
        model.add(
            Dropout(rate=hp.Float(
                'dropout_1',
                min_value=0.0,
                max_value=0.5,
                default=0.25,
                step=0.05,
            ))
        )
        model.add(
            Conv2D(
                filters=10,
                kernel_size=(3),
                strides=(2, 2),
                activation='relu',
            )
        )
        model.add(Flatten())
        model.add(
            Dropout(rate=hp.Float(
                'dropout_2',
                min_value=0.0,
                max_value=0.5,
                default=0.25,
                step=0.05,
            ))
        )
        model.add(BatchNormalization())
        model.add(Dense(self.num_classes, activation='softmax'))

        model.compile(optimizer='rmsprop',
                      loss='categorical_crossentropy',
                      metrics=['accuracy']
                      )
        return model


(X_train, y_train), (X_test, y_test) = mnist.load_data()

X_train_reshaped = np.expand_dims(X_train.astype('float32'), axis=3)
X_test_reshaped = np.expand_dims(X_test.astype('float32'), axis=3)
y_train_reshaped = to_categorical(y_train.astype('float32'))
y_test_reshaped = to_categorical(y_test.astype('float32'))

K.clear_session()

INPUT_SHAPE = (28, 28, 1)
NUM_CLASSES = 10


# Hypermodel definition
hypermodel = CNNHyperModel(input_shape=INPUT_SHAPE, num_classes=NUM_CLASSES)

# Define tuner
HYPERBAND_MAX_EPOCHS = 40
MAX_TRIALS = 20
SEED = 1
EXECUTION_PER_TRIAL = 2

tuner = Hyperband(
    hypermodel,
    max_epochs=HYPERBAND_MAX_EPOCHS,
    objective='val_accuracy',
    seed=SEED,
    executions_per_trial=EXECUTION_PER_TRIAL,
    directory='hyperband',
    project_name='MNIST'
)

# Search space summary of tuner
tuner.search_space_summary()

# Start the tuning
N_EPOCH_SEARCH = 40
tuner.search(
        X_train_reshaped,
        y_train_reshaped,
        epochs=N_EPOCH_SEARCH,
        validation_split=0.1
        )

# Summary of the results
tuner.results_summary()

# Retrieve best model
best_model = tuner.get_best_models(num_models=1)[0]

# Evaluate best model
loss, accuracy = best_model.evaluate(X_test_reshaped, y_test_reshaped)

print(f"""
The hyperparameter search is complete. The optimal number of filters
in the first convoluted layer is
{best_model.get('num_filters_1')},
the optimal dropout rate for the first dropout layer is
{best_model.get('dropout_1')},
and the optimal dropout rate for the second dropout layer is
{best_model.get('dropout_2')}.
""")

print(f'Loss rate on best model: {loss}')
print(f'Accuracy on best model: {accuracy}')
