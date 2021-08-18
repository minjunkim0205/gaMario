# 02. kerasNeuralNetwork.py
import tensorflow as tf
import numpy as np

model = tf.keras.Sequential([
    tf.keras.layers.Dense(9, input_shape=(13 * 16,), activation='relu'),
    tf.keras.layers.Dense(6, activation='sigmoid')
])

print(model.summary())

date = np.random.randint(0, 3, (13 * 16), dtype=np.int)
print(date)

predict = model.predict(np.array([date]))[0]
print(predict)

result = (predict > 0.5).astype(np.int)
print(result)