import tkinter
import requests
import os
import concurrent.futures
from tkinter.filedialog import askopenfilename
from pathlib import Path
from http import HTTPStatus

class ImageDownloader:
	def __init__(self, src_path):
		self.src_path = src_path
		self.des_dir = os.path.join('raw_imgs', src_path[src_path.rfind('\\') + 1:-4])

	def download(self, output_filename, url):
		headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_11_5) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/50.0.2661.102 Safari/537.36'}
		response = requests.get(url, headers = headers)
		if response.status_code == HTTPStatus.OK:
			with open(os.path.join(self.des_dir, output_filename + '.png'), 'wb') as img:
				img.write(response.content)
		else:
			for status in list(HTTPStatus):
				if status.value == response.status_code:
					print(status.description)
			
	def run(self):
		with open('urls/downloadedImg.txt', 'r+') as downloaded_img, open(self.src_path) as ready_to_download:
			if not Path(self.des_dir).exists() :
				os.makedirs(self.des_dir)
				
			downloaded_img_list = list(downloaded_img)	
			ready_to_download_list = list(ready_to_download)	
			counter = 0
			
			with concurrent.futures.ThreadPoolExecutor(max_workers=25) as executor:
				for url in ready_to_download_list:
					if url not in downloaded_img_list:
						executor.submit(self.download , str(counter), url[:-1])
						downloaded_img.write(url)
						counter += 1					
			
if __name__ == '__main__':
	tkinter.Tk().withdraw()
	selected_path = askopenfilename()	
	image_downloader = ImageDownloader(selected_path)
	image_downloader.run()