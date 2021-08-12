import matplotlib.pyplot as plt
import cv2
import numpy as np
from keras.models import Sequential
from keras.layers import Dense, Flatten, Conv2D, MaxPool2D, Dropout
from keras.optimizers import SGD, Adam
import pandas as pd
import numpy as np
from sklearn.model_selection import train_test split
from sk.learn import shuffle

data = pd.read_csv('file').astype(float)
data.head(10)

X = data.drop('0', axis = 1)
y = data['0']

train_x, test_x, train_y, test_y = train_test_split(X, y, test_size = 0.2)
train_x = np.reshape(train_x.values, (train_x.shape[0], 28,28))
test_x = np.reshape(test_x.values, (test_x.shape[0], 28,28))

print("Train data shape: ", train_x.shape)
print("Test data shape:", test_x.shape)

word_dict = {0:'A', 1:'B', 2:'C', 3:'D', 4:'E', 5:'F', 6:'G', 7:'H', 8:'I', 9:'J', 10:'K', 11:'L', 12: 'M', 13:'N',
             14:'O', 15:'P', 16:'Q', 17:'R', 18:'S', 19:'T', 20:'U', 21:'V', 22:'W', 23:'X', 24:'Y', 25:'Z'}
y_int = np.int(y)
count = np.zeroes(26, dtype = 'int')

for i in y_int:
    count[i] +=1

alphabets = []
for i in word_dict.values():
    alphabets.append(i)

fig, ax = plt.subplots(1,1, figsize = (10,10))
ax.barh(alphabets,count)


plt.xlabel("Number of elements")
plt.ylabel("Alphabets")
plt.grid()
plt.show()

shuff = shuffle(train_x[:100])

fig, ax = plt.subplots(3,3, figsize = (10,10))
axes = ax.flatten()

for i in range(9):
    shu = cv2.threshold(shuff[i], 30, 200, cv2.THRESH_BINARY)
    axes[i].imshow(np.reshape(shuff[i], (28,28)), cmap = "Greys")
    plt.show()

train_X = train_x.reshape(train_x.shape[0], train_x.shape[1], train_x.shape[2],1)
print("New shape : ", train_X.shape)

test_X = test_x.reshape(test_x.shape[0], test_x.shape[1], test_x.shape[2],1)

#to_categorical outputs vectors of probabilities







train_yOHE = to_categorical(train_y, num_classes = 26, dtype = 'int')
test_yOHE = to_categorical(test_y, num_classes = 26, dtype = 'int')

model = Sequential()

model.add(Conv2D(filters = 32, kernel_size=(3,3), activation = 'relu', input_shape = (28,28,1)))
model.add(MaxPool2D(pool_size = (2,2), strides = 2))
model.add(Conv2D(filters =64, kernel_size = (3,3), activation = 'relu', padding = 'same'))
model.add(MaxPool2D(pool_size = (2,2), strides = 2))
model.add(Conv2D(filters = 64, kernel_size = (3,3), activation = 'relu', padding = 'same'))

model.add(MaxPool2D(pool_size=(2,2), strides =2))

model.add(Conv2D(filters = 128, kernel_size =(3,3), activation = 'relu', padding = 'valid'))
model.add(MaxPool2D(pool_size =(2,2), strides=2))

model.add(Flatten())

model.add(Dense(64,activation = "relu"))
model.add(Dense(128, activation = "relu"))

model.add(Dense(26, activation = "softmax"))


model.compile(optimizer = Adam(learning_rate = 0.001), loss = 'categorical_crossentropy', metrics =['accuracy'])


history = model.fit(train_X, train_yOHE, epochs =1, validation_data = (test_x, test_yOHE))

model.summary()
model.save('character model')
