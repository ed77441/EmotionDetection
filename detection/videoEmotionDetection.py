import cv2
import imutils
import numpy as np
import os
import time
import multiprocessing
import dlib
from keras.preprocessing.image import img_to_array
from keras.models import load_model
import argparse
import timeit
import tensorflow as tf
from keras.backend.tensorflow_backend import set_session

class semaphore:
	def __init__(self):
		self.assignment = multiprocessing.Event()
		self.report = multiprocessing.Event()
		
	def reset(self):
		self.assignment.clear()
		self.report.clear()
		
	def waitAssignment(self):
		self.assignment.wait()
		
	def signalAssignment(self):
		self.assignment.set()
		
	def waitReport(self):
		self.report.wait()
		
	def signalReport(self):
		self.report.set()

def adjustSize(width, height):
	if width >= 1280:
		width = 1280
		height = 720
	return (int(width), int(height))

def reader(inq, video_name, flag):
	cap = cv2.VideoCapture(video_name)
	width = cap.get(cv2.CAP_PROP_FRAME_WIDTH )
	height = cap.get(cv2.CAP_PROP_FRAME_HEIGHT )
	
	width, height = adjustSize(width, height)
	
	counter = 0
	group = []
	firstTime = True
	while cap.isOpened():
		grabbed, frame = cap.read()
		if not grabbed:
			break
		frame = cv2.resize(frame, (width, height))
		group.append(frame)
		
		if len(group) == 5:		#5張一組
			inq.put(group)
			group = []

	flag.value = 0 				#表示reader結束
	cap.release()
	print('reader done!')

def displayer(outq, video_name, result_name, processor_flag):
	tmp_cap = cv2.VideoCapture(video_name)
	print(tmp_cap.get(cv2.CAP_PROP_FPS))
	width = tmp_cap.get(cv2.CAP_PROP_FRAME_WIDTH )
	height = tmp_cap.get(cv2.CAP_PROP_FRAME_HEIGHT )
	
	width, height = adjustSize(width, height)
	print('****************',type(width),type(height),width, height)
	fourcc = cv2.VideoWriter_fourcc('M','P','4','V')
	out = cv2.VideoWriter(result_name, fourcc, tmp_cap.get(cv2.CAP_PROP_FPS), (width, height))
	tmp_cap.release()
	
	while True:
		success = False
	
		while not success:
			try:
				frame = outq.get(timeout=0.5)
				success = True
			except:
				if all(flag == 0 for flag in processor_flag[0]):
					break
		
		if not success:
			break

		out.write(frame)

	out.release()
	print('displayer done!')

def processor(inq, outq, syncq, lk, sem, id , model_name, reader_flag, flag):
	config = tf.ConfigProto()
	config.gpu_options.per_process_gpu_memory_fraction = 0.3
	set_session(tf.Session(config=config))
	
	model = load_model(model_name)
	emos = ['neutral', 'happy', 'sad', 'suprise', 'angry', 'fear', 'disgust']
	template_dict = {'x1':None, 'y1':None, 'x2': None,'y2': None, 'emo': None}
	detector = dlib.get_frontal_face_detector()
	while True:
		lk.acquire()
		
		success = False

		while not success:
			try:
				group = inq.get(timeout=0.5)
				success = True
			except:
				if reader_flag.value == 0:
					lk.release()
					break
					
		if not success:
			break
		
		sem.reset()
		syncq.put(id)
		lk.release()
		
		# parallelism region start--------------------
		pfs = []
		faces, scores, idx = detector.run(group[0], 0)
		for i, d in enumerate(faces):
			x1 = d.left()
			y1 = d.top()
			x2 = d.right()
			y2 = d.bottom()
			
			face = group[0][y1:y2, x1:x2]
			face = cv2.resize(face, (48, 48))
			face = face.astype('float') / 255.0
			face = img_to_array(face)
			face = np.expand_dims(face, axis=0)

			proba = model.predict(face)[0]
			idx = np.argmax(proba)

			#cv2.rectangle(group[0], (x1, y1), (x2, y2), (0, 255, 0), 4, cv2.LINE_AA)
			cloned = template_dict.copy()  
			cloned['x1'] = x1            
			cloned['x2'] = x2             
			cloned['y1'] = y1             
			cloned['y2'] = y2              
			cloned['emo'] = emos[idx]
			pfs.append(cloned)
			
		for i in range(5):
			for pf in pfs:
				cv2.rectangle(group[i], (pf['x1'], pf['y1']), (pf['x2'],pf['y2']), (0, 255, 0), 4, cv2.LINE_AA)
				cv2.putText(group[i], pf['emo'], (pf['x1'], pf['y1']-10), cv2.FONT_HERSHEY_DUPLEX, 0.6, (255, 255, 255), 1, cv2.LINE_AA)
		#parallelism region end ----------------------------------


		# output to ouputqueue
		sem.waitAssignment()	#等待協調者發出許可

		for frame in group:
			outq.put(frame)

		sem.signalReport()		#給協調者發出訊號
	new_one = flag[0] 
	new_one[id] = 0
	flag[0] = new_one
	print('processor {}, done!'.format(id))
		
def coordinator(parsed_args, worker_nums):
	manager = multiprocessing.Manager()
	
	reader_flag = manager.Value('i', 1)
	raw_list = [1 for _ in range(worker_nums)] #[1,1,1,...]
	processor_flag = manager.list([raw_list])
	syncq = manager.Queue()
	inq = manager.Queue()
	outq = manager.Queue()

	lk = manager.Lock()
	slist = []
	ps = []
	rp =  multiprocessing.Process(target=reader, args=(inq, parsed_args['video'], reader_flag))
	dp =  multiprocessing.Process(target=displayer, args=(outq, parsed_args['video'], parsed_args['result'], processor_flag))
	
	rp.start()
	dp.start()
	ps.append(rp)
	ps.append(dp)

	for i in range(worker_nums):
		sem = semaphore()
		slist.append(sem)
		p = multiprocessing.Process(target=processor, args=(inq, outq, syncq, lk, sem, i, parsed_args['model'], reader_flag, processor_flag))
		ps.append(p)
		p.start()

	
	while True:
		success = False
		
		while not success:
			try:
				id = syncq.get(timeout=0.5)
				success = True
			except:
				if all(flag == 0 for flag in processor_flag[0]):
					break
		
		if not success:
			break

		sem = slist[id]
		sem.signalAssignment()
		sem.waitReport()
		
	for p in ps:
		p.join()
	print('main process done!')

if __name__ == '__main__':
	start = timeit.default_timer()
	ap = argparse.ArgumentParser()
	ap.add_argument('-m', '--model', required=True, help='path to trained model model')
	ap.add_argument('-v', '--video', required=True, help='path to input video')
	ap.add_argument('-r', '--result', required=True, help='result path to input file')
	args = vars(ap.parse_args())
	
	worker_nums = 3
	coordinator(args, worker_nums)
	stop = timeit.default_timer()
	print('Time: ', stop - start)  
