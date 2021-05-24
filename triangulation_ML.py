import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import tensorflow as tf

from globals import TRIANGULATION_SIMULATED_DATA as file


if __name__ == '__main__':
    np.set_printoptions(precision=3, suppress=True)

    usecols = [0,1,2,3,4,5,8,9,10,11]
    names = ("Node_X", "Node_Y", "Anchor_A_X", "Anchor_A_Y", "Anchor_B_X", "Anchor_B_Y", "Beacon_A", "Beacon_B", "Beacon_A_Noise", "Beacon_B_Noise",)
    triangulation_AoA_train = pd.read_csv(file, delimiter='\t', skiprows=1, usecols=usecols, names=names)

    features = triangulation_AoA_train.copy()
    labels_x = features.pop("Node_X")
    labels_y = features.pop("Node_Y")
    beacons_a = features.pop("Beacon_A")        # pop original beacons to use only simulated beacons with noise
    beacons_b = features.pop("Beacon_B")        # pop original beacons to use only simulated beacons with noise

    
    features_train = features[0:-10]            # training data
    lables_train_X = labels_x[0:-10]            # training X results
    lables_train_Y = labels_y[0:-10]            # training Y results

    featues_predict = features[-10:]            # predict


    model_x = tf.keras.Sequential([
        tf.keras.layers.Dense(6, activation=tf.nn.relu, input_shape=[6]),           # shape of train data = 6
        tf.keras.layers.Dense(72, activation=tf.nn.relu),                           # hidden layer 72 nodes - experemental value
        tf.keras.layers.Dense(144, activation=tf.nn.relu), 
        tf.keras.layers.Dense(72, activation=tf.nn.relu),                           # hidden layer 72 nodes - experemental value

        # tf.keras.layers.Dense(144, activation=tf.nn.relu),
        # tf.keras.layers.Dense(144, activation=tf.nn.relu),
        

        # tf.keras.layers.Dense(12, activation=tf.nn.relu),

        tf.keras.layers.Dense(1)                                                    # output 1 value
    ])

    model_y = tf.keras.Sequential([
        tf.keras.layers.Dense(6, activation=tf.nn.relu, input_shape=[6]),           # shape of train data = 6
        tf.keras.layers.Dense(72, activation=tf.nn.relu),                           # hidden layer 72 nodes - experemental value
        tf.keras.layers.Dense(144, activation=tf.nn.relu),
        tf.keras.layers.Dense(72, activation=tf.nn.relu),                           # hidden layer 72 nodes - experemental value

        # tf.keras.layers.Dense(288, activation=tf.nn.relu),
        # tf.keras.layers.Dense(12, activation=tf.nn.relu),
        tf.keras.layers.Dense(1)                                                    # output 1 value
    ])


    optimizer = tf.keras.optimizers.RMSprop(0.001)                                  # accuracy of weights change
    model_x.compile(
        loss='mean_squared_error',
        optimizer=optimizer,
        metrics=['mean_absolute_error', 'mean_squared_error']
    )

    model_y.compile(
        loss='mean_squared_error',
        optimizer=optimizer,
        metrics=['mean_absolute_error', 'mean_squared_error']
    )

    model_x.fit(features_train, lables_train_X, epochs=10000)
    # model_x.fit(features_train, lables_train_X, epochs=5000)
    predicted_x = model_x.predict(featues_predict)

    model_y.fit(features_train, lables_train_Y, epochs=10000)
    # model_y.fit(features_train, lables_train_Y, epochs=5000)
    predicted_y = model_y.predict(featues_predict)

    plt.clf()
    for x, y in zip(predicted_x, predicted_y):
        plt.plot(x, y, 'g x')
    for x, y in zip(labels_x[-10:], labels_y[-10:]):
        plt.plot(x, y, 'b o')
    plt.show()






