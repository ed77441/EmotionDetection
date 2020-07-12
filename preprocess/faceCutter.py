import dlib
import cv2
import imutils
import os
from pathlib import Path
import concurrent.futures

def process_img(img, des_dir, original_filename):
	img = imutils.resize(img, width=1400)
	detector = dlib.get_frontal_face_detector()
	face_rects = detector(img, 0)

	for i, d in enumerate(face_rects):
		x1 = d.left()
		y1 = d.top()
		x2 = d.right()
		y2 = d.bottom()
			
		chopped_img = img[y1:y2, x1:x2]
		cv2.imwrite(os.path.join(des_dir, str(i) + '_' + original_filename), chopped_img)
		
		
src_dir_parent = 'raw_imgs'
des_dir_parent = 'processed_imgs'

if __name__ == '__main__':
	with open(os.path.join(des_dir_parent, 'processed_dir.txt'), 'r+') as processed_dir, concurrent.futures.ProcessPoolExecutor(max_workers=30) as executor:
		processed_dir_list = list(processed_dir)
		counter = 0
		for i, str in enumerate(processed_dir_list):
			processed_dir_list[i] = str[:-1]
		print(processed_dir_list)
		
	
		for src_dir in os.listdir(src_dir_parent):
			des_dir = os.path.join(des_dir_parent, src_dir)
			src_dir = os.path.join(src_dir_parent, src_dir)
			
			if src_dir not in processed_dir_list:

				if not Path(des_dir).exists():
					os.makedirs(des_dir)
				for filename in os.listdir(src_dir):
					img = cv2.imread(os.path.join(src_dir, filename), 0)
					print(os.path.join(src_dir, filename))
					if type(img) != type(None):
						executor.submit(process_img, img, des_dir, filename)
				processed_dir.write(src_dir + '\n')
				counter += 1
		print('{0} {1} {2} been processed!'.format(counter,  'dir' if counter == 1 else 'dirs' ,'has' if counter == 1 else 'have'))