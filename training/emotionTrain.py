import os
import cv2
import argparse
import random
import pickle
import numpy as np
from imutils import paths
from sklearn.utils import shuffle
from keras.preprocessing.image import ImageDataGenerator, img_to_array
from keras.optimizers import Adam
from sklearn.preprocessing import LabelBinarizer
from sklearn.model_selection import train_test_split
from EmotionXDD_network import SmallerVGGNet
import PIL
# 定義參數
from keras.models import load_model
ap = argparse.ArgumentParser()

ap.add_argument('-m', '--model', required=True, help='path to output model')
ap.add_argument('-rm', '--rmodel', required=False, help='path to input rmodel')
ap.add_argument('-e', '--epochs', required=False, help='how many epochs u want to train')
ap.add_argument('-bs', '--batch_size', required=False, help='batch')

args = vars(ap.parse_args())

EPOCHS = 150
LR = 1e-3
BS = 32

if args['epochs'] != None:
    EPOCHS = int(args['epochs'])

if args['batch_size'] != None:
    BS = int(args['batch_size'])


IMAGE_DIMS = (48, 48, 3)

data = []
labels = []

# 隨機抓取圖片路徑
print('[INFO] loading images...')

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

# 標籤二值化
lb = LabelBinarizer()
labels = lb.fit_transform(labels)

# 模型初始化
print('[INFO] compiling model...')

model = None

if args['rmodel'] != None:
    model = load_model(args['rmodel'])
else:
    model = SmallerVGGNet.build(width=IMAGE_DIMS[1], height=IMAGE_DIMS[0], depth=IMAGE_DIMS[2], classes=len(lb.classes_))
opt = Adam(lr=LR, decay=LR / EPOCHS)
model.compile(loss='categorical_crossentropy', optimizer=opt, metrics=['accuracy'])

# 開始訓練
H = model.fit(
    data,
	labels,
    validation_split=0.2,
    batch_size=BS,
    epochs=EPOCHS, verbose=1)

# 保存模型
print('[INFO] serializing network...')

model.save(args['model'])
