import time
from tensorflow.keras.datasets import mnist
from tensorflow.keras.models import Sequential
from tensorflow.keras.layers import Dense, Flatten
from tensorflow.keras.utils import to_categorical
from CNN import plot_history

(x_train, y_train), (x_test, y_test) = mnist.load_data()

print(f"Размерность обучающих изображений: {x_train.shape}")
print(f"Размерность обучающих меток: {y_train.shape}")
print(f"Количество тестовых примеров: {x_test.shape[0]}")

x_train = x_train.astype('float32') / 255
x_test = x_test.astype('float32') / 255

num_classes = 10
y_train_ohe = to_categorical(y_train, num_classes=num_classes)
y_test_ohe = to_categorical(y_test, num_classes=num_classes)

model = Sequential([
    Flatten(input_shape=(28, 28)),
    Dense(256, activation='relu', name='Hidden_1'),
    Dense(128, activation='relu', name='Hidden_2'),
    Dense(num_classes, activation='softmax', name='Output_Layer')
])
model.summary()

model.compile(optimizer='adam',
              loss='categorical_crossentropy',
              metrics=['accuracy'])

start = time.time()
history_extended = model.fit(x_train, y_train_ohe,
                            epochs=20,
                            batch_size=32,
                            validation_data=(x_test, y_test_ohe),
                            verbose=1)
finish = time.time() - start
print(finish)

plot_history(history_extended)