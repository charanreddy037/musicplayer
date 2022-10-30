from tkinter.filedialog import askdirectory
from tkinter import*
from tkinter import ttk
import pygame
import os
import time
from mutagen.mp3 import MP3
from mutagen.id3 import ID3,APIC,error
from PIL import ImageTk,Image
import speech_recognition as sr
import random


root = Tk()
pygame.mixer.init()

root.title('music-player')
#change size
w = 470;h = 740
#root.geometry('{}x{}'.format(w,h))
root.minsize(w,h)
#root.attributes('-alpha',0.9)
#changing colour
roli='white'
roda='black'
toli='#E74C3C'
toda='#B03A2E'
mili='#3498DB'
mida='#1A5276'
boli='#48C9B0'
boda='#117864'
root.config(bg=roli)
#FRAMES
Top_frame = Frame(root, bg=toli,padx=10,pady=10)
Middle_frame = Frame(root, bg=mili,padx=5,pady=15)
Bottom_frame = Frame(root, bg=boli,padx=10,pady=10)
volume_frame=Frame(root,bg=mili,padx=10,pady=50)

#animate frame
animate_frame=Frame(root,bg="#ff8533",height=h,width=w)
animate_frame.place(x=0,y=0)
#Label(animate_frame,bg="yellow",height=10,width=470)

#anim function=============
def anim():
	for x in range(741):
		animate_frame.place(x=0,y=-4*x)
		animate_frame.update()

#lets rock btn in animate to hide animate_frame
logo=PhotoImage(file='./assets/iiitklogo.png')
fk=Label(animate_frame,image=logo,height=200,width=470,bg='#39e600')
fk.place(anchor='c',x=235,y=370)
#loading widget
load=Label(animate_frame,text='Loading...')
load.place(anchor='c',x=235,y=500)
#progress bar for loading player
pro_load=ttk.Progressbar(animate_frame,orient=HORIZONTAL,length=300,mode='determinate')
pro_load.place(anchor='c',x=235,y=540)
l=-1

def loading():
		global l
		if l<=10:
				txt='Loading'+('.'*l)+(str(10*l)+'%')
				load.config(text=txt)
				load.after(150,loading)
				pro_load['value']=10*l
				l+=1
		else:
				anim()
#opening load screen
loading()

#all photos
pause_play_img=PhotoImage(file="./assets/pp.png")
play_img=PhotoImage(file="./assets/play.png")
pause_img=PhotoImage(file="./assets/pause.png")
next_img=PhotoImage(file="./assets/next.png")
pre_img=PhotoImage(file="./assets/previous.png")
not_shuffle_img=PhotoImage(file="./assets/not_shuffle.png")
not_loop_img=PhotoImage(file="./assets/not_loop.png")
shuffle_img=PhotoImage(file="./assets/shuffle.png")
loop_img=PhotoImage(file="./assets/loop.png")
fav_off=PhotoImage(file="./assets/fav_black.png")
fav_on=PhotoImage(file="./assets/fav_red.png")
fav_copy=PhotoImage(file="./assets/fav_red_copy.png")
close_img=PhotoImage(file="./assets/close.png")
add_img=PhotoImage(file="./assets/plus.png")
delete_img=PhotoImage(file="./assets/delete.png")
choose_img=PhotoImage(file="./assets/folder.png")
theme_img=PhotoImage(file="./assets/theme.png")
nav_img=PhotoImage(file="./assets/list.png")
volume_img=PhotoImage(file="./assets/volume.png")
mute_img=PhotoImage(file="./assets/mute.png")
home_img=PhotoImage(file="./assets/home.png")
theme_img=PhotoImage(file="./assets/theme.png")
about_img=PhotoImage(file="./assets/about.png")

#mic,search images
mic_img=PhotoImage(file="./assets/mic.png")
search_img=PhotoImage(file="./assets/search.png")

#------List boxes--------
list1=Listbox(Middle_frame,width=25,bg='black',fg='white'
		,selectbackground='green', selectforeground='white',font='bold')
list2=Listbox(Middle_frame)
fav_listbox=Listbox(Middle_frame,width=25,bg='white',fg='purple',selectbackground='black'
		,selectforeground='white',font='bold')
n,no=0,0
playlist=[]



#============================Main functions ===========================
#functions

def play() :
		play_time()
		p_p.config(image=pause_img,command=pause)
		pygame.mixer.music.unpause()

def pause() :
		p_p.config(image=play_img,command=play)
		pygame.mixer.music.pause()

def dire():#choose_directory
		global playlist
		global time_bar
		#global list1

		a = '00:00'
		time_bar.config(text =f'{a}/{a}')
		p_p.config(image=pause_play_img,command=starting)
		pygame.mixer.music.stop()
		playlist.clear()
		list1.delete('0','end')
		dirc=askdirectory()
		if len(dirc) != 0 :
				os.chdir(dirc)
				for files in os.listdir():
						if files.endswith(".mp3"):
								if files not in playlist:
										playlist.append(files)
										list1.insert(END,files)

def browse_file():
		global filename_path
		filename_path = filedialog.askopenfilename()
		add_to_playlist(filename_path)

def add_to_playlist(filename):
		if len(playlist) == 0:
				list1.delete('0','end')
		filename = os.path.basename(filename)
		if filename not in playlist:
				playlist.append(filename)
		list1.insert(END, filename)
		list2.insert(END, filename_path)

def nex() :
		global no
		global n
		global shfl
		global l00p

		if l00p == 1:
				no = no
		else:
				if shfl == 0:
						if n%2==0 :
								n+=1
						if no == list1.size()-1 :
								no=0
						else :
								no=no+1
				elif shfl == 1:
						temp = no
						no = random.randint(0,len(playlist))
						if temp == no:
								no = no-1

		song_name = list1.get(no)
		for i in range(list2.size()) :
				a=list2.get(i)
				b=a.split('/')
				if song_name==b[-1] :
						song_name=a
						break

		#print(song_name)
		if song_name.endswith('.mp3'):
				#Active song selection
				list1.selection_clear(0,END)
				list1.activate(no)
				list1.selection_set(no,last=None)
				play()
				pygame.mixer.music.load(song_name)
				pygame.mixer.music.play()
		else:
				 
				nex()
		play_time()
		song_namee=list1.get(ACTIVE)
		if song_namee in fav_list:
				fav_btn.config(image=fav_on,command=fav_red_fn)
		else:
				fav_btn.config(image=fav_off,command=fav_black_fn)

def pre() :
		global no
		global n
		global shfl
		global l00p

		if l00p == 1:
				no = no
		else:
				if shfl == 0:
						if n%2==0 :
								n+=1
						if no == 0 :
								no=list1.size()-1
						else :
								no=no-1
				elif shfl == 1:
						temp = no
						no = random.randint(0,len(playlist))
						if temp==no:
								no = no+1

		song_name = list1.get(no)
		for i in range(list2.size()) :
				a=list2.get(i)
				b=a.split('/')
				if song_name==b[-1]:
						song_name=a
						break

		if song_name.endswith('.mp3'):
				#Active song selection
				list1.selection_clear(0,END)
				list1.activate(no)
				list1.selection_set(no,last=None)
				play()
				pygame.mixer.music.load(song_name)
				pygame.mixer.music.play()
		else:
				pre()
		play_time()
		song_namee=list1.get(ACTIVE)
		if song_namee in fav_list:
				fav_btn.config(image=fav_on,command=fav_red_fn)
		else:
				fav_btn.config(image=fav_off,command=fav_black_fn)

def go(event):
		global no
		result.place_forget()
		cancel.place_forget()
		no=list1.curselection()[0]
		song_name=list1.get(no)
		l = 0
		for i in playlist:
				if i == song_name:
						no = l
				l += 1
		#print('no = ',no)

		if song_name.endswith('.mp3'):
				for i in range(list2.size()):
						a=list2.get(i)
						b=a.split('/')
						if song_name==b[-1]:
								song_name=a
								break
				#Active song selection
				list1.selection_clear(0,END)
				list1.activate(no)
				list1.selection_set(no,last=None)

				pygame.mixer.music.load(song_name)
				pygame.mixer.music.play()

				p_p.config(image=pause_img)
				p_p.place(anchor='c',relx=.5, rely=.5)
				root.update()
		play_time()
		song_namee=list1.get(ACTIVE)
		if song_namee in fav_list:
			fav_btn.config(image=fav_on,command=fav_red_fn)
		else:
			fav_btn.config(image=fav_off,command=fav_black_fn)

def searchplay(event):
		global p_p
		global no

		result.place_forget()
		cancel.place_forget()
		no=result.curselection()
		song_name=result.get(no)
		root.update()
		l = 0
		for i in playlist:
				if i == song_name:
						no = l
				l += 1
		#print('no = ',no)
		if song_name.endswith('.mp3'):
				#print(song_name)
				for i in range(list2.size()) :
						a=list2.get(i)
						b=a.split('/')
						if song_name==b[-1]:
								song_name=a
								break
				#Active song selection
				list1.selection_clear(0,END)
				list1.activate(no)
				list1.selection_set(no,last=None)

				pygame.mixer.music.load(song_name)
				pygame.mixer.music.play()
				p_p.config(image=pause_img)
				p_p.place(anchor='c',relx=.5, rely=.5)
				root.update()
		play_time()

global shfl,l00p
shfl = 0;l00p = 0
def shuffle():
		global shfl
		if shfl == 0:
				shfl = 1
				shufflebtn.config(image=shuffle_img)
				root.update()
		else:
				shfl = 0
				shufflebtn.config(image=not_shuffle_img)
				root.update()
		#print(shfl)
def Loop_fn():
		global l00p  
		if l00p == 0:
					l00p = 1
					loopbtn.config(image=loop_img)
					root.update()
		else:
					l00p = 0
					loopbtn.config(image=not_loop_img)
					root.update()



#========placing
Top_frame.grid(row=0, column=0,  sticky='nsew',padx=10,pady=10)
Middle_frame.grid(row=1, column=0,  sticky='nsew',padx=10)
Bottom_frame.grid(row=2, column=0,  sticky='nsew',padx=10,pady=10)
#volume_frame.grid(row=2,column=1,sticky='nsew',padx=10,pady=10)

#=======gridSize
root.grid_rowconfigure(0, minsize=10, weight=1)
root.grid_rowconfigure(1, minsize=380, weight=1)
root.grid_rowconfigure(2, minsize=40, weight=1)
root.grid_columnconfigure(0, minsize=50, weight=1)

#=============search box and voice ====================================
def search():
		global playlist
		global result

		check=[]
		result.delete(0,END)
		st = str(textbox.get(1.0,2.0)).strip()
		cnt = 0
		l=len(st)
		while(l>0):
				for i in playlist:
						if i.upper().startswith(st.upper()):
										if (i not in check):
												result.insert(END,i)
												check.append(i)
												cnt = +1
				st=st[:-1]
				l=len(st)
		if cnt==0:
				result.insert(END,"---Not found---")

		result.place(anchor='c',relx=.5, rely=.2)
		cancel.place(anchor='c',relx=.8,rely=.2)
def dispr(e):
		result.place_forget()
		cancel.place_forget()
def Cancel():
		result.place_forget()
		cancel.place_forget()
		textbox.delete(1.0,END)


textbox = Text(Top_frame, width = 30,height=1)
textbox.place(anchor='c',relx=.5, rely=.3)
textbox.bind('<Enter>',dispr)
result = Listbox(root,width=35, height=3)
cancel = Button(root,borderwidth=0,text='X',pady=0,command=Cancel,bg='green',fg = 'white')
#result.place(anchor='c',relx=.4, rely=.3)
search = Button(Top_frame,image=search_img,bg=toli,activebackground=toli,borderwidth=0, command=search)
search.place(anchor='c',relx=.9, rely=.3)
result.bind('<Double-1>',searchplay)

#===voice---------

def speak_func():
		global textbox
		global song_status

		r1 = sr.Recognizer()
		r2 = sr.Recognizer()
		textbox.delete(1.0,END)
		root.update()
		with sr.Microphone() as source:
			#print('speak now...')
			textbox.config(bg='black',fg='white')
			textbox.insert(1.0,'    Speak now...')
			root.update()
			audio = r1.listen(source, phrase_time_limit=2)
		try:
				get = r2.recognize_google(audio)
				a = get
		except sr.UnknownValueError :
				#print('error')
				a = 'error'
		except sr.RequestError as e:
				#print('failed'.format(e))
				a = 'failed'
		#voicebtn.config(bg = 'green')
		textbox.delete(1.0,END)
		textbox.insert(1.0,a)
		root.update()
		#print('speak completed')
		#print('--------')
		if a != 'error' and a != 'failed':

				#search functiion
				global playlist
				global result
				check=[]
				result.delete(0,END)
				st = a.strip()
				cnt = 0
				l=len(st)
				while(l>0):
						for i in playlist:
								if i.upper().startswith(st.upper()):
												if (i not in check):
														result.insert(END,i)
														check.append(i)
														cnt = +1
						st=st[:-1]
						l=len(st)
				if cnt==0:
						result.insert(END,"----Not Found----")
				result.place(anchor='c',relx=.5, rely=.2)
				result.config(bg='black',fg='white')
				cancel.place(anchor='c',relx=.8,rely=.2)
				textbox.config(bg = 'white',fg='black')
				root.update()

voicebtn = Button(Top_frame,image=mic_img,borderwidth=0,bg=toli,activebackground=toli, command=lambda:speak_func())
voicebtn.place(anchor='c',relx=.5, rely=.8)
#*********************MIDDLE Frame // playlist properties ---------------------------------
def del_play_list():
		list1.delete('0','end')
		list1.insert(END,"no songs in playlist")
		playlist.clear()
		p_p.config(image=pause_play_img,command=None)
		pygame.mixer.music.stop()
		#pygame.quit()

def PlayListBox():
		global choose
		global delbtn
		#choose=Button(Middle_frame,text="choose_directory",command=dire)
		list1.place(anchor='c',relx=.4, rely=.4)
		choose.place(anchor='c',relx=.2, rely=.8)
		delbtn.place(anchor='c',relx=.6, rely=.8)
		add_song.place(anchor='c',relx=.4, rely=.8)
		PlayListbtn.config(text='Back',command=pl_Back)
		#pygame.mixer.music.stop()
		root.update()

def pl_Back():
		global choose
		choose.place_forget()
		fav_listbox.place_forget()
		list1.place_forget()
		delbtn.place_forget()
		add_song.place_forget()
		PlayListbtn.config(text='PlayList',command=PlayListBox)

list1.bind('<Double-1>', go)
PlayListbtn = Button(Middle_frame,text="PlayList",width=10,font='bold',command=PlayListBox)
PlayListbtn.grid(column=0,row=4,padx=10,pady=10)
add_song=Button(Middle_frame,image=add_img,command=browse_file,bg=mili,activebackground=mili,borderwidth=0)
choose=Button(Middle_frame,image=choose_img,command=dire,bg=mili,activebackground=mili,borderwidth=0)
delbtn = Button(Middle_frame,image=delete_img,command=del_play_list,bg=mili,activebackground=mili,borderwidth=0)
#--starting
"""
list1.place(anchor='c',relx=.4, rely=.4)
choose.place(anchor='c',relx=.2, rely=.8)
PlayListbtn.config(text='Back',command=pl_Back)
delbtn.place(anchor='c',relx=.6, rely=.8)
add_song.place(anchor='c',relx=.4, rely=.8)
"""

#===================Status bar==================================================

def play_time(): #playtime for song
		global no
		global p_bar
		global song_status
		current_time = pygame.mixer.music.get_pos() / 1000
		c_ctime = time.strftime('%M:%S', time.gmtime(current_time))
		#status_bar.config(text =str(c_ctime))
		time_bar.after(1000,play_time)
		song_name = list1.get(no)
		for i in range(list2.size()) :
				a=list2.get(i)
				b=a.split('/')
				if song_name==b[-1] :
						song_name=a
						break
		#print(song_name)
		if song_name != '' and song_name.endswith('.mp3'):
				s1 = MP3(song_name)
				s1_l = s1.info.length
				song_ttime = time.strftime('%M:%S', time.gmtime(s1_l))
				#if c_ctime == song_ttime:
				#   p_bar['value'] = 100

				A = (current_time/s1_l)*100
				#print(A)
				if A>=100:
						p_bar['value']=100
						time.sleep(1)
						nex()
						root.update()
				else:
						p_bar['value'] =  A
						time_bar.config(text =f'{c_ctime}/{song_ttime}')
						root.update()
				#root.update_idletasks()
				#time.sleep(1)


		else :
				a = '00:00'
				time_bar.config(text =f'{a}/{a}')
				p_bar['value'] = 0

time_bar = Label(Middle_frame,text=0,pady=3,width=10,bg='#D2B4DE')
time_bar.place(anchor='c',relx=.9,rely=1)

#===========volume function========
def volume(x):
		volume=int(x)/100
		pygame.mixer.music.set_volume(volume)
		if volume==0:
					vol_btn.config(image=mute_img)
		else:
				vol_btn.config(image=volume_img)                     
def vol_dissapear():
		volume_slider.place_forget()
		vol_btn.config(command=vol_visible)
		root.update()

def vol_visible():
		volume_slider.place(anchor='w',relx=.9,rely=.4)
		vol_btn.config(command=vol_dissapear)
		root.update()

#volume slide
volume_slider=Scale(Middle_frame,from_=100,to=0,orient=VERTICAL,command=volume,length=200,width=9,activebackground='#D2B4DE',troughcolor='black',borderwidth=0)
volume_slider.set(25)
#volume_slider.place(anchor='w',relx=.8,rely=.4)

vol_btn = Button(Middle_frame,image=volume_img,bg=mili,activebackground=mili,command=vol_visible,borderwidth=0)
vol_btn.place(anchor='w',relx=.9,rely=.7)

if len(os.listdir()) != 0:
		#filename = os.path.dirname(os.listdir())
		#list2.insert(filename)
		for files in os.listdir():
						if files.endswith(".mp3") :
								if files not in playlist:
										playlist.append(files)
										list1.insert(END,files)

if len(playlist)==0:
		list1.insert(END,"no songs in playlist")
a = '00:00'
time_bar.config(text =f'{a}/{a}')

#==============Progress bar============
p_bar = ttk.Progressbar(Middle_frame,orient=HORIZONTAL,length=300,mode='determinate')
p_bar.place(anchor='c',relx=.4,rely=1)
p_bar['value'] = 100

#**********************************===============================================

#------------------------------------------------------------------

# start of the program
def starting():
		global song_status
		song_name=list1.get(0)
		if song_name.endswith('.mp3'):
				for i in range(list2.size()) :
						a=list2.get(i)
						b=a.split('/')
						if song_name==b[-1] :
								song_name=a
								break
				pygame.mixer.music.load(song_name)
				pygame.mixer.music.play()
				#Active song selection
				list1.selection_clear(0,END)
				list1.activate(no)
				list1.selection_set(no,last=None)
				p_p.place(anchor='c',relx=.5, rely=.5)
				play_time()
		play()

fav_list=[]
def fav_fn():
		fav_btn.config(image=fav_on,command=fav_red_fn)
		song_name=list1.get(ACTIVE)
		fav_list.append(song_name)
def fav_black_fn():
		song_name=list1.get(ACTIVE)
		if song_name in fav_list:
				fav_btn.config(image=fav_on,command=fav_red_fn)
		else:
				fav_list.append(song_name)
				fav_btn.config(image=fav_on,command=fav_red_fn)
		# print(fav_list)
def fav_red_fn():
		fav_btn.config(image=fav_off,command=fav_black_fn)
		song_name=list1.get(ACTIVE)
		if song_name in fav_list:
				fav_list.remove(song_name)


#buttons---
prebtn=Button(Bottom_frame,image=pre_img,command=pre,borderwidth=0,bg=boli,activebackground=boli)
prebtn.place(anchor='c',relx=.3, rely=.5)
p_p = Button(Bottom_frame,image=pause_play_img,command=starting,borderwidth=0,bg=boli,activebackground=boli)
p_p.place(anchor='c',relx=.5, rely=.5)
nextbtn=Button(Bottom_frame,image=next_img,command=nex,borderwidth=0,bg=boli,activebackground=boli)
nextbtn.place(anchor='c',relx=.7, rely=.5)
shufflebtn = Button(Bottom_frame,image=not_shuffle_img,borderwidth=0,bg=boli,activebackground=boli,command = shuffle)
loopbtn = Button(Bottom_frame,image=not_loop_img,borderwidth=0,bg=boli,activebackground=boli,command = Loop_fn)
shufflebtn.place(anchor='c',relx=.1, rely=.5)
loopbtn.place(anchor='c',relx=.9, rely=.5)
fav_btn=Button(Bottom_frame,image=fav_off,borderwidth=0,bg=boli,activebackground=boli,command=fav_fn)
fav_btn.place(anchor='c',relx=.9,rely=.1)

#side navigation bar====================
#nav frame
nav_frame=Frame(root,bg="#154360",height=740,width=175)
nav_frame.place(x=-200,y=0)
Label(nav_frame,bg="#76D7C4",fg='white',height=3,width=200).place(x=0,y=0)
#nav open/close function
def nav_cls_fn():
				for x in range(201):
						nav_frame.place(x=-8*x,y=0)
						root.update()
				light_btn.place_forget()
				dark_btn.place_forget()
def nav_open_fn():
				for x in range(-200,0):
						nav_frame.place(x=4,y=0)
						root.update()
				g=10
				#options functions
				options_fn=[home_fn,open_fav_List,th_fn,about_fn]
				for i in range(len(options)):
						option_btn=Button(nav_frame,image=img_option[i],text=options[i],compound='left',bg="#76D7C4",activebackground="#76D7C4",font='bold',borderwidth=0,
									command=options_fn[i])
				#options btns in nav_frame
						for x in range(76,g,-1):
								option_btn.place(x=20,y=8*x)
								#option_btn.place(x=20,y=10)
								#root.update()
						g+=10
				#close btn in nav Frame // Animation
				"""
				close_btn.place(x=-20,y=5)
				for i in range(40):
						close_btn.place(x=4*i,y=5)
						#close_btn.place(x=4,y=5)
						#root.update()
				"""
				close_btn.place(x=125,y=8)

close_btn=Button(nav_frame,image=close_img,bg="#76D7C4",activebackground="#76D7C4",borderwidth=0,command=nav_cls_fn)

def FavListbox():
		fav_listbox.place(anchor='c',relx=.4, rely=.4)
		PlayListbtn.config(text='playlist',command=PlayListBox)
		root.update()
		PlayListbtn.place_forget()
		
#options in nav bar and their functions
options=[" Home"," Favourite"," Theme"," About"]
img_option=[home_img,fav_copy,theme_img,about_img]
# optins functions
def home_fn():
	global la
	for x in range(201):
		nav_frame.place(x=-10*x,y=0)
		Top_frame.update()
	fav_listbox.place_forget()
	PlayListBox()
	la.place_forget()

def open_fav_List():
		global la 
		fav_listbox.delete(0,END)
		for x in range(201):
				nav_frame.place(x=-10*x,y=0)
				Top_frame.update()
		for i in range(len(fav_list)):
				fav_listbox.insert(END,fav_list[i])
		choose.place_forget()
		add_song.place_forget()
		#PlayListbtn.place_forget()
		PlayListbtn.config(text='Favourites',font='bold',bg='pink')
		root.update()
		delbtn.place_forget()
		list1.place_forget()
		fav_listbox.place(anchor='c',relx=.4, rely=.4)
		la.place_forget()

		#PlayListbtn.config(text='Favourite',command=FavListbox)
def fav_onclick(event):
		global no

		result.place_forget()
		cancel.place_forget()
		no1=fav_listbox.curselection()
		song_name=fav_listbox.get(no1)
		l = 0
		for i in playlist:
				if i == song_name:
						no = l
				l += 1
		#print('no = ',no)

		if song_name.endswith('.mp3'):
				for i in range(list2.size()):
						a=list2.get(i)
						b=a.split('/')
						if song_name==b[-1]:
								song_name=a
								break
				#Active song selection
				list1.selection_clear(0,END)
				list1.activate(no)
				list1.selection_set(no,last=None)

				#Active song selection in fav list//
				fav_listbox.selection_clear(0,END)
				fav_listbox.activate(no1)
				fav_listbox.selection_set(no1,last=None)

				pygame.mixer.music.load(song_name)
				pygame.mixer.music.play()
				
				p_p.config(image=pause_img)
				p_p.place(anchor='c',relx=.5, rely=.5)
				root.update()
		play_time()

fav_listbox.bind('<Double-1>',fav_onclick)


#==========menu bar==============
#--modes
#light and dark functions
def light():
		for x in range(201):
			nav_frame.place(x=-10*x,y=0)
			nav_frame.update()
		light_btn.place_forget()
		dark_btn.place_forget()
		root.config(bg=roli)
		Top_frame.config(bg=toli)
		Middle_frame.config(bg=mili)
		add_song.config(bg=mili,activebackground=mili)
		choose.config(bg=mili,activebackground=mili)
		delbtn.config(bg=mili,activebackground=mili)
		Bottom_frame.config(bg=boli)
		list1.config(bg='white',fg='black')
		voicebtn.config(bg=toli,activebackground=toli)
		search.config(bg=toli,activebackground=toli)
		shufflebtn.config(bg=boli,activebackground=boli)
		prebtn.config(bg=boli,activebackground=boli)
		p_p.config(bg=boli,activebackground=boli)
		nextbtn.config(bg=boli,activebackground=boli)
		loopbtn.config(bg=boli,activebackground=boli)
		fav_btn.config(bg=boli,activebackground=boli)
		nav_btn.config(bg=toli,activebackground=toli)
		vol_btn.config(bg=mili,activebackground=mili)
def dark():
		for x in range(201):
				nav_frame.place(x=-10*x,y=0)
				nav_frame.update()
		light_btn.place_forget()
		dark_btn.place_forget()
		root.config(bg=roda)
		Top_frame.config(bg=toda)
		Middle_frame.config(bg=mida)
		add_song.config(bg=mida,activebackground=mida)
		choose.config(bg=mida,activebackground=mida)
		delbtn.config(bg=mida,activebackground=mida)
		Bottom_frame.config(bg=boda)
		voicebtn.config(bg=toda,activebackground=toda)
		search.config(bg=toda,activebackground=toda)
		shufflebtn.config(bg=boda,activebackground=boda)
		prebtn.config(bg=boda,activebackground=boda)
		p_p.config(bg=boda,activebackground=boda)
		nextbtn.config(bg=boda,activebackground=boda)
		loopbtn.config(bg=boda,activebackground=boda)
		list1.config(bg='black',fg='white')
		fav_btn.config(bg=boda,activebackground=boda)
		nav_btn.config(bg=toda,activebackground=toda)
		vol_btn.config(bg=mida,activebackground=mida)
#dark ,light radio buttons
dark_btn=Radiobutton(nav_frame,text="Dark",value=1,height=1,bg='#AF7AC5',command=dark)
light_btn=Radiobutton(nav_frame,text="Light",value=2,height=1,bg='#AF7AC5',command=light)


def th_fn():
		for i in range(-40,20):
				dark_btn.place(x=i,y=296)
				nav_frame.update()
		for i in range(250,100,-1):
				light_btn.place(x=i,y=296)
				nav_frame.update()

global la
im = Image.open('./assets/aa.png')
im = im.resize((440,380), Image.ANTIALIAS)
im1 = ImageTk.PhotoImage(im)
la = Label(Middle_frame,image=im1,height=500,width=500,bg='#C39BD3')
la.image=im1
def about_fn():
	global la
	for x in range(201):
		nav_frame.place(x=-8*x,y=0)
		Top_frame.update()
	PlayListbtn.place_forget()
	root.update()
	la.place(anchor='c',relx=.5,rely=.5)
	root.update()
#nav btn
nav_btn=Button(Top_frame,image=nav_img,bg=toli,activebackground=toli,command=nav_open_fn,borderwidth=0)
nav_btn.place(anchor='c',relx=.1, rely=.3)


root.mainloop()
