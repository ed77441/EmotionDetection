import os
import argparse
import imutils
import pickle
import cv2
import dlib
import numpy as np
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import timeit


emos = ['neutral', 'happy', 'sad', 'suprise', 'angry', 'fear', 'disgust']

template_dict = {'x1':None, 'y1':None, 'x2': None,'y2': None, 'emo': None}        #------#
pfs = []       #------#


def show(frame, fcount): #------#
	global pfs           #------#
	if fcount % 5 == 0: #------#
		faces, scores, idx = detector.run(frame, 0)
		try:
			pfs = []  #------#
				
			for i, d in enumerate(faces):
				x1 = d.left()
				y1 = d.top()
				x2 = d.right()
				y2 = d.bottom()
				
				# 圖片預處理
				face = frame[y1:y2, x1:x2]
				face = cv2.resize(face, (48, 48))
				face = face.astype('float') / 255.0
				face = img_to_array(face)
				face = np.expand_dims(face, axis=0)

				# 表情分類
				proba = model.predict(face)[0]

				idx = np.argmax(proba)
				#for emo, degree in zip(emos, proba):
				#	print(emo, '{:f}'.format(degree))


				# 框臉並標示分類結果
				cv2.rectangle(frame, (x1, y1), (x2, y2), (255, 255, 255), 2, cv2.LINE_AA)
				cv2.putText(frame, emos[idx], (x1, y1-10), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)
				cloned = template_dict.copy()  #------#
				cloned['x1'] = x1              #------#
				cloned['x2'] = x2              #------#
				cloned['y1'] = y1              #------#
				cloned['y2'] = y2              #------#
				cloned['emo'] = emos[idx]      #------#
				pfs.append(cloned)             #------#
		except:
			pass
	else:               #------#
		for pf in pfs:              #------#
			cv2.rectangle(frame, (pf['x1'], pf['y1']), (pf['x2'],pf['y2']), (255, 255, 255), 2, cv2.LINE_AA)               #------#
			cv2.putText(frame, pf['emo'], (pf['x1'], pf['y1']-10), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)              #------#
	return frame

# 定義參數

start = timeit.default_timer()
ap = argparse.ArgumentParser()
ap.add_argument('-m', '--model', required=True, help='path to trained model model')
ap.add_argument('-r', '--result', required=True, help='path to label binarizer')
ap.add_argument('-i', '--image', required=False, help='path to input image')
ap.add_argument('-v', '--video', required=False, help='path to input video')
args = vars(ap.parse_args())

# 載入模型及標籤
model = load_model(args['model'])

#lb = pickle.loads(open(args['labelbin'], 'rb').read())
detector = dlib.get_frontal_face_detector()

if args['image']:
    frame = cv2.imread(args['image'])
    frame = show(frame, 0)        #------#
    # 顯示結果並儲存
    cv2.imshow('Emotion Recognition', frame)
    cv2.imwrite('result.jpg', frame)
    
    # 釋放資源
    cv2.waitKey(0)
    cv2.destroyAllWindows()
else:


    cap = cv2.VideoCapture(1)
    #fourcc = cv2.VideoWriter_fourcc('M','P','4','V')
    #out = cv2.VideoWriter(args['result'], fourcc, 30.0, (1280, 720))
    # 設定輸出影片格式
    counter = 0       #------#
    while (cap.isOpened()):
        ret, frame = cap.read()
        
        if not ret:
            break
        
        frame = cv2.resize(frame, (880, 495)) 
        frame = show(frame, counter)
        cv2.imshow('test', frame)
        if cv2.waitKey(10) == 27:
            break
        #out.write(frame)
        counter += 1

#    out.release()
    cap.release()
    cv2.destroyAllWindows()
    stop = timeit.default_timer()
    print('Time: ', stop - start)  
