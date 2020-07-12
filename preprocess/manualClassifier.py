from tkinter import *
from tkinter.filedialog import askdirectory
import os
from PIL import Image, ImageTk
from pathlib import Path
import sys

class MyApplication:
	def __init__(self, src_dir, des_log, limit):
		keys_and_funcs = [('Left', self.previous), ('Right', self.next), ('z', self.press_z), ('x', self.press_x),
						('c', self.press_c), ('v', self.press_v), ('b', self.press_b), ('n', self.press_n), 
						('space', self.press_space),('Up', self.press_up)]
		self.des_dir = ['neutral', 'happy', 'sad', 'suprise', 'angry', 'fear', 'disgust', 'deleted']
		self.root = Tk()
		for key, func in keys_and_funcs:
			self.root.bind('<' + key + '>', func)
		
		self.log_file = des_log
		self.start_pos = 0
		self.log = []
		
		for emotion in des_log:
			self.log.append(int(emotion[:-1]))
			self.start_pos += 1
		self.pos = self.start_pos
		self.progress = self.start_pos				

		self.imgs = []
		name_list = list(os.listdir(src_dir))
		
		if limit != None:
			name_list = name_list[:limit]
		
		for img_name in name_list:
			path = os.path.join(src_dir, img_name)
			try:
				img = Image.open(path).resize((500,500), Image.ANTIALIAS)
				self.imgs.append(img)
			except:
				os.remove(path)

		self.img_count = len(self.imgs)
		self.log = self.log + [None] * (self.img_count - self.start_pos)

		if self.start_pos != self.img_count:
			self.cur_img = self.imgs[self.start_pos]
			self.canvas = Canvas(self.root, height=500, width=500)
			self.label = Label(self.root, text='None', font=("Courier", 30))
			
			self.draw_canvas()
			self.draw_label()			
		
	def draw_canvas(self):
		filename = ImageTk.PhotoImage(self.cur_img)
		self.canvas.image = filename
		self.canvas.create_image(0,0,anchor='nw',image=filename)
		self.canvas.pack()		
	
	def draw_label(self):
		text = ""
		if self.log[self.pos] != None:
			text = self.des_dir[self.log[self.pos]]
		else :
			text = "None"
			
		self.label.config(text=text)
		self.label.pack()		
		
	def next(self, event):
		if self.pos < self.img_count - 1 and self.log[self.pos] != None:
			self.pos += 1
			self.cur_img = self.imgs[self.pos]
			
			self.draw_canvas()
			self.draw_label()
			
			if self.pos > self.progress:
				self.progress = self.pos			
			
	def previous(self, event):
		if self.pos > self.start_pos:
			self.pos -= 1
			self.cur_img = self.imgs[self.pos]
			self.draw_canvas()
			self.draw_label()
			self.draw_label()

	def press_z(self, event):
		self.log[self.pos] = 0 #neu
		self.draw_label()
		
	def press_x(self, event):
		self.log[self.pos] = 1 #hap
		self.draw_label()
		
	def press_c(self, event):
		self.log[self.pos] = 2 #sad
		self.draw_label()
		
	def press_v(self, event):
		self.log[self.pos] = 3 #sup
		self.draw_label()
		
	def press_b(self, event):
		self.log[self.pos] = 4 #ang
		self.draw_label()
	
	def press_n(self, event):
		self.log[self.pos] = 5 #fea
		self.draw_label()	
	
	def press_space(self, event):
		self.log[self.pos] = 6 #dis	
		self.draw_label()

	def press_up(self, event):
		self.log[self.pos] = 7 #del
		self.draw_label()		
	
	def run(self):
		if self.start_pos < self.img_count:
			self.root.mainloop()
			for emotion in self.log[self.start_pos:self.progress+1]:
				if emotion != None:
					self.log_file.write(str(emotion) + '\n')
	
			if self.progress == self.img_count - 1 and self.log[self.progress] != None:	 #save
				names = []
				for dir in self.des_dir[:-1]:
					names.append(len(os.listdir(os.path.join('dataset' , dir))))

				for emo, img in zip(self.log[self.start_pos:], self.imgs[self.start_pos:]):
					if emo != 7: #
						img = img.resize((48,48), Image.ANTIALIAS)#outputing!
						img.save(os.path.join('dataset', self.des_dir[emo], str(names[emo]) + '.png'))
						names[emo] += 1					
		else:
			print('outputed!')
	
if __name__ == '__main__':
	tmp = Tk()
	tmp.withdraw()	
	src_dir = askdirectory()	
	tmp.destroy()
	
	des_log = os.path.join('dataset', src_dir[src_dir.rfind('/') + 1:] + '.txt' )
	with open(des_log, 'a+') as log:
		pass
	with open(des_log, 'r+') as log:
		arg = None
		if len(sys.argv) == 2:
			arg = int(sys.argv[1])
		else :
			arg = None
		myapp = MyApplication(src_dir, log, arg)
		myapp.run()