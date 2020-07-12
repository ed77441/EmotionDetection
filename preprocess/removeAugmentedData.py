import os

img_path_base = 'dataset'
emos = ['neutral', 'happy', 'sad', 'suprise', 'angry', 'fear', 'disgust']

for label, emo in enumerate(emos):
	img_dir = os.path.join(img_path_base, emo)
	for img_name in os.listdir(img_dir):
		img_full_path = os.path.join(img_dir, img_name)
		if img_name[:3] == 'aug':
			os.remove(img_full_path)
