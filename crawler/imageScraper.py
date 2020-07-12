import sys
import time
import os
import shutil
from selenium import webdriver
from pathlib import Path
from img_downloader import ImageDownloader

if len(sys.argv) >= 2:
	driver = webdriver.Chrome('venv\Scripts\chromedriver.exe')

	query = sys.argv[1]
	
	if len(sys.argv) > 2:
		for keyword in sys.argv[2:]:
			query += "+" + keyword
			
	driver.get('https://www.google.com/search?q='+query+'&source=lnms&tbm=isch')
	time.sleep(1.5)

	with open('get_urls.js', 'r') as jsfile:
		target_txt = query + '.txt'
		
		src_path = os.path.join('C:/Users/ed774/Downloads', target_txt)
		des_path = os.path.join('urls', target_txt)
		
		get_urls_script = jsfile.read()
		driver.execute_script(get_urls_script)
		script_end = False
		while not script_end:
			time.sleep(0.05)
			if Path(src_path).exists():
				script_end = True
		driver.close()
		
		if Path(des_path).exists(): #it's already downloaded before
			os.remove(src_path)
			print("it's already downloaded before")
		else:
			shutil.move(src_path , des_path)
			image_downloader = ImageDownloader(des_path)
			image_downloader.run()
		print('Done.')
else:
	print("Args must include query keyword!!")