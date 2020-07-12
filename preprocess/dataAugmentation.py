import os
import cv2
import random
import pickle
import numpy as np
from sklearn.utils import shuffle
from keras.preprocessing.image import ImageDataGenerator, img_to_array
import PIL
import sys
# 定義參數

IMAGE_DIMS = (48, 48, 3)

data = []
labels = []

# 隨機抓取圖片路徑
print('[INFO] loading images...')

#倍率
n = [1,1,2,2,2,2,3]

img_path_base = 'dataset'
emos = ['neutral', 'happy', 'sad', 'suprise', 'angry', 'fear', 'disgust']

for label, emo in enumerate(emos):
	img_dir = os.path.join(img_path_base, emo)
	for img_name in os.listdir(img_dir):
		img_full_path = os.path.join(img_dir, img_name)
		image = cv2.imread(img_full_path)
		image = cv2.resize(image, (IMAGE_DIMS[1], IMAGE_DIMS[0]))
		image = img_to_array(image)
		data.append(image)
		
		labels.append(label)
	
# 圖片正規化
data = np.array(data, dtype='float') / 255.0
labels = np.array(labels)


data, labels = shuffle(data, labels, random_state=999997)

# 資料增強

aug = ImageDataGenerator(
    rotation_range=25, width_shift_range=0.1,
    height_shift_range=0.1, shear_range=0.2, 
    zoom_range=0.2, horizontal_flip=True, fill_mode='nearest')

for img,l in zip(data,labels): 
    i = 0
    img = img.reshape(1,48,48,3)
    target_dir = os.path.join(img_path_base, emos[l])
    for batch in aug.flow(img,batch_size=32,save_to_dir=target_dir,save_prefix='aug_' + str(random.randint(0,99999)),save_format='png'):
        i += 1
        if i > n[l] - 1:
            break