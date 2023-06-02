# -*- coding: utf-8 -*-
"""NASNetMobile.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/10aDLRCwaRmpGD_8LDDerK_Z4dqacw-Df
"""

import tensorflow as tf
from tensorflow.keras.applications.nasnet import NASNetMobile, preprocess_input
from tensorflow.keras.preprocessing.image import ImageDataGenerator, load_img, img_to_array

image_size = (224, 224)
batch_size = 8

train_path = r'/content/drive/MyDrive/Dataset/Train'
test_path = r'/content/drive/MyDrive/Dataset/Test'

train_datagen = ImageDataGenerator(preprocessing_function=preprocess_input)
test_datagen = ImageDataGenerator(preprocessing_function=preprocess_input)

train_batches = train_datagen.flow_from_directory(train_path,target_size=image_size,batch_size=batch_size,class_mode='binary',shuffle=True)
test_batches = test_datagen.flow_from_directory(test_path,target_size=image_size,batch_size=batch_size,class_mode='binary',shuffle=False)

# creation
base_model = NASNetMobile(weights='imagenet', include_top=False, input_shape=(224, 224, 3))
for layer in base_model.layers:
    layer.trainable = False
x = base_model.output
x = tf.keras.layers.GlobalAveragePooling2D()(x)
x = tf.keras.layers.Dense(128, activation='relu')(x)
x = tf.keras.layers.Dropout(0.5)(x)
predictions = tf.keras.layers.Dense(1, activation='sigmoid')(x)

#compilation
model = tf.keras.models.Model(inputs=base_model.input, outputs=predictions)

#training
model.compile(optimizer='SGD', loss='binary_crossentropy', metrics=['accuracy'])

#evaluation
history=model.fit(train_batches, epochs=20, validation_data=test_batches)

model.save('/content/drive/MyDrive/NASNETMOBILE.h5')

loaded_model = tf.keras.models.load_model('/content/drive/MyDrive/NASNETMOBILE.h5')
print("Model loaded successfully."
     )

class_indices = {0: "cancer", 1: "non-cancer"} 

image_path = r'/content/drive/MyDrive/Dataset/Test/non cancer 1/dataset_jlspo68f92i21.JPEG'

img = load_img(image_path, target_size=image_size)
img_array = img_to_array(img)
img_array = tf.expand_dims(img_array, axis=0)
img_array = preprocess_input(img_array)

prediction = model.predict(img_array)
class_index = tf.argmax(prediction, axis=1).numpy()[0]

class_label = class_indices[class_index]

print(class_label)

import matplotlib.pylab as plt
train_loss=history.history['loss']
val_loss=history.history['val_loss']
train_acc=history.history['accuracy']
val_acc=history.history['val_accuracy']
xc=range(len(val_loss))


plt.figure(1,figsize=(9,5))
plt.plot(xc,train_loss)
plt.plot(xc,val_loss)
plt.xlabel('Epochs')
plt.ylabel('Loss')
plt.title('SGD-Batch_Size=8')
plt.grid(True)
plt.legend(['loss','validation loss'],loc='lower left')
plt.style.use(['classic'])

train_loss=history.history['loss']
val_loss=history.history['val_loss']
train_acc=history.history['accuracy']
val_acc=history.history['val_accuracy']
xc=range(len(val_loss))


plt.figure(1,figsize=(9,5))
plt.plot(xc,train_acc)
plt.plot(xc,val_acc)
plt.xlabel('Epochs')
plt.ylabel('Accuracy')
plt.title('SGD-Batch_Size=8')
plt.grid(True)
plt.legend(['accuracy','validation accuracy'],loc='lower right')
plt.style.use(['classic'])

model.evaluate(test_batches)