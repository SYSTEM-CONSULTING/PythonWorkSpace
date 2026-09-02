import tensorflow as tf
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Input



# a simple model

model = Sequential([
    Input(shape=(784,)),
    Dense(64, activation='relu'),
    Dense(10, activation='softmax')
])

# so wars vorher ohne input aber warning !!
# model = Sequential([
#    Dense(64, activation='relu', input_shape=(784,)),
#    Dense(10, activation='softmax')
# ])

# Compile the model
model.compile(
    optimizer='adam',
    loss='sparse_categorical_crossentropy',
    metrics=['accuracy']
)

# Summary of the model
model.summary()
