import os
import cv2
import numpy as np
from keras.preprocessing.image import img_to_array
from keras.models import load_model

img_path_base = 'testset'
emos = ['neutral', 'happy', 'sad', 'suprise', 'angry', 'fear', 'disgust']
model = load_model('es.h5')

for label, emo in enumerate(emos):
	img_dir_name = os.path.join(img_path_base, emo)
	img_dir = list(os.listdir(img_dir_name))
	total_num = len(img_dir)
	
	actual_num = 0
	for img_name in img_dir:
		img_full_path = os.path.join(img_dir_name, img_name)
		image = cv2.imread(img_full_path)
		image = image.astype('float') / 255.0
		image = img_to_array(image)
		image = np.expand_dims(image, axis=0)
		
		proba = model.predict(image)[0]
		idx = np.argmax(proba)
		if idx == label:
			actual_num += 1
	ratio = (actual_num / total_num) * 100
	print('{0: <16}'.format(emo), '{0:.2f} % total = {1}'.format(ratio, total_num))
		
