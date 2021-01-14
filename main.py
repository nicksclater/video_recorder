
import tkinter as tk
from tkinter import filedialog
import subprocess
import os
from time import gmtime

from config_file import *


## sample streams

# stream1 = "https://www.radiantmediaplayer.com/media/big-buck-bunny-360p.mp4"
# stream2 = "udp://127.0.0.1:1234"

## code

os.chdir(working_dir)
window = tk.Tk()
window.resizable(False, False)
window.title('Mission Recorder')
window.configure(background='gray90')

mission = tk.StringVar()
mission.set('')
time = tk.IntVar()
time.set('')
log = tk.StringVar()
duration = tk.StringVar()
duration.set('10 mins')


options = ['30 secs', '60 secs', '5 mins', '10 mins', '30 mins']
options_sec = {'30 secs':30, '60 secs':60, '5 mins':300, '10 mins':600, '30 mins':1800}


record_label = ['Not Recording', 'Recording']
record = False

def start_stop_pressed():

	global record
	seconds = options_sec[duration.get()]
	if mission.get() == '':
		mission.set('mission')

	if not record:

		if not os.path.exists(mission.get()):
			os.makedirs(mission.get())

		subprocess.Popen(f"ffmpeg -re -i {stream1} -c copy -movflags +empty_moov+separate_moof -f\
		 stream_segment -segment_time {seconds} -segment_atclocktime 1 -reset_timestamps 1 -strftime 1\
		  '{mission.get()}-%H%M%S.mp4'", shell=True, cwd=f'{mission.get()}')

		label3.config(bg='green', fg='gray0', text=record_label[1])
		record = True
		window.update()
	
	else:

		label3.config(bg='red', fg='white', text=record_label[0])
		record = False
		window.update()
		subprocess.Popen('pkill -15 ffmpeg', shell=True)

def view_btn_pressed():

	try:
		video_file = filedialog.askopenfilename(initialdir=f'/Users/nicksclater/Desktop/{mission.get()}',filetypes=[("video clip", "*mp4")])
		if video_file != '':
			subprocess.Popen(['vlc', video_file])
	except:
		pass

def join_btn_pressed():

	try:
		subprocess.Popen(f'for i in *.mp4; do echo file $i >> files.txt; done', shell=True, cwd=f'{mission.get()}')
		subprocess.Popen(f'ffmpeg -f concat -i files.txt -c copy {mission.get()}.mp4', shell=True, cwd=f'{mission.get()}')
	except:
		pass

def search_btn_pressed():

	try:
		files = os.listdir(mission.get())

		files = [i for i in files if i.endswith('.mp4')]
		files = [i for i in files if not i == f'{mission.get()}.mp4']
		print(files)

		for i in range(len(files)):
		    
		    if files[i][-10] == '-':
		        files[i] = files[i][:-11]+'0'+files[i][-10:]

		print(files)
		files = sorted(files, key=lambda x: int(x[-10:-4]))
		print(files)

		for i in range(len(files)):
		    if int(files[i][-10:-4]) < time.get() < int(files[i + 1][-10:-4]):
		        subprocess.Popen(['vlc', f'{mission.get()}/{files[i]}'])
		        break
	except:
		pass

def log_btn_pressed():

	if mission.get() == '':
		mission.set('mission')

	if not os.path.exists(mission.get()):
			os.makedirs(mission.get())

	subprocess.Popen(f"echo '{gmtime()[3]}:{gmtime()[4]}:{gmtime()[5]}z - {log.get()}' >> {mission.get()}/{mission.get()}_log.txt ", shell=True)
	subprocess.Popen(f"echo  >> {mission.get()}/{mission.get()}_log.txt", shell=True)
	log.set('')
	
	
## GUI design

label1 = tk.Label(window, font=('arial', 14), text='Enter Mission ID:', background='gray90')
label1.grid(row=0, column=0, pady=(10,0))

mission_ent = tk.Entry(window, textvariable=mission, font=('arial', 14), justify='center', highlightbackground='gray90')
mission_ent.grid(row=0, column=1, padx=(5,5), pady=(10,0))

label2 = tk.Label(window, font=('arial', 14), text='File Duration', padx=10, pady=5, background='gray90')
label2.grid(row=1, column=0)

set_duration = tk.OptionMenu(window, duration, *options)
set_duration.config(width=20, font=('arial', 14), background='gray90')
set_duration.grid(row=1, column=1)

start_stop_btn = tk.Button(window, text='Start/Stop Recording',command=start_stop_pressed, font=('arial', 14), highlightbackground='gray90')
start_stop_btn.grid(row=2, column=0, padx=(5,5))

label3 = tk.Label(window, font=('arial', 14), text=record_label[0], background='red', fg='white')
label3.grid(row=2, column=1, sticky='EW', padx=(5,5))

time_search_btn = tk.Button(window, text='Search Time', command=search_btn_pressed,font=('arial', 14), highlightbackground='gray90')
time_search_btn.grid(row=3, column=0, sticky='EW', padx=(5,5))

time_ent = tk.Entry(window, textvariable=time, font=('arial', 14), justify='center', highlightbackground='gray90')
time_ent.grid(row=3, column=1, padx=(5,5))

view_btn = tk.Button(window, text='View Clip', command=view_btn_pressed, font=('arial', 14), highlightbackground='gray90')
view_btn.grid(row=4, column=0, sticky='EW', padx=(5,5))

join_all_btn = tk.Button(window, text='Join All', command=join_btn_pressed, font=('arial', 14), highlightbackground='gray90')
join_all_btn.grid(row=4, column=1, sticky='EW', padx=(5,5))

log_btn = tk.Button(window, text='Log', command=log_btn_pressed, font=('arial', 14), highlightbackground='gray90')
log_btn.grid(row=5, column=0, padx=(5,5), sticky='EW')

log_ent = tk.Entry(window, textvariable=log, font=('arial', 12), justify='left', highlightbackground='gray90')
log_ent.grid(row=5, column=1, sticky='WE')


window.mainloop()

