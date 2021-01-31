import os
import pathlib
import tensorflow as tf
import keras
from keras.callbacks import *
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from keras.models import Sequential
from keras.layers import *
import itertools


def create_model():
    model = Sequential([])
    model=Sequential([])

    model.add(Conv2D(64,(3,3),activation="relu",input_shape=(28,28,1)))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(2,2))

    model.add(Conv2D(128,(3,3),activation="relu"))
    model.add(BatchNormalization())
    model.add(MaxPooling2D(2,2))

    model.add(Flatten())
    model.add(BatchNormalization())
    model.add(Dense(256,activation="relu"))
    model.add(BatchNormalization())
    model.add(Dense(26,activation="softmax"))
    model.summary()
    return model

def text_output_from_prediction(res: np.array):
    letter = ['A', 'B', 'C', 'D', 'E', 'F', 'G', 'H', 'I', 'J', 'K', 'L', 'M', 'N', 'D', 'P', 'Q', 'R', 'S', 'T', 'U', 'V', 'W', 'X', 'Y', 'Z']
    return list(itertools.compress(letter, res))

def run():
    model = create_model()
    print("Model created!")
    model.load_weights(
        os.path.join(str(pathlib.Path(__file__).resolve().parent), "asl_model_v2.h5")
    )
    print("Weight Loaded")

    test_data = pd.read_csv(
        "E:\Hackathon\AmericanSignLanguage-Recognizer\sign_mnist_test.csv"
    )

    test_labels = test_data[1:50]['label'].values
    test_data.drop('label', axis=1, inplace=True)
    test_samples = test_data[1:50].values
    # print(test_samples)
    test_samples = test_samples.reshape(-1,28,28,1)
    # print(test_samples)
    model.compile(loss="sparse_categorical_crossentropy",optimizer='adam',metrics=['accuracy'])
    print(    model.evaluate(test_samples, test_labels)[1]*100)
    prediction = model.predict(test_samples)
    print(prediction)

    for i in prediction:
        print(text_output_from_prediction(i))
    # reconstructed_model = keras.models.load_model(
    #     os.path.join(str(pathlib.Path(__file__).resolve().parent), "conv2.h5")
    # )
if __name__ == "__main__":
    print("MAIN")
    run()
