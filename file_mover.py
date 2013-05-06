#!/usr/bin/env python

import os, os.path,shutil
from Tkinter import * 
run = False
cleared = True

def move_music(files_list = [], dst_list = [], path = [],length = 0,files_moved = 0):
    for files in range(0,length):
        file_name = files_list[files].replace(path[files],"")
        print "copying " + file_name
        copied_files.insert(END, "copying" + file_name)
        copied_files.update()
        copied_files.see(END)
        if not os.path.exists(dst_list[files]): os.makedirs(dst_list[files])
        shutil.copyfile(files_list[files], dst_list[files] + "/" + file_name)
        files_moved += 1
    return files_moved



def transfer_music(src = "/home/bryan/music3", dst = "/home/bryan/music4",file_type = ".mp3"):
    global run
    global cleared
    files_moved = 0
    files_list = []
    path = []
    dst_list = []

    def walk(dst):
        list1 = []
        list2 = []
        for root,dirs,files in os.walk(dst):
            list1 += files
        for f in list1:
            if f.endswith(file_type):
                list2.append(f)
        return list2

    files_in_dst = walk(dst)
    if not os.path.isdir(src):
        copied_files.insert(END, "The source directory doesn't exist!")
        copied_files.update()
        return

    def f (src,dst,file_type,files_in_dst):
        
        listOfFiles = os.listdir(src)

        for file in listOfFiles:
            if file.startswith("."):
                pass
            elif file.endswith(file_type) and not os.path.exists(dst + "/" + file):
                    if any(s.endswith(file) for s in files_list):
                        pass
                    elif any(t.endswith(file) for t in files_in_dst):
                        pass
                    else:
                        files_list.append(src + "/" + file)
                        path.append(src+"/")
                        dst_list.append(dst)
            elif os.path.isdir(src +"/" + file):
                new_src = src + "/" + file
                new_dst = dst + "/" + file
                f(new_src, new_dst,file_type,files_in_dst)
        return len(files_list)

    length = f(src,dst,file_type,files_in_dst)
    copied_files.insert(END,str(length) + " files will be copied and moved. Would you like to just copy or copy and remove from source?")
    
    def continues():
        copied_files.insert(END,str(move_music(files_list,dst_list,path,length,files_moved)) + " files were copied and moved to " + dst)
        copied_files.see(END)
        continue_button.destroy()
        remove_button.destroy()
        global  run 
        run = False
    
    def clear():
        copied_files.delete(0,END)
        clear_button.destroy()
        continue_button.destroy()
        remove_button.destroy()
        global run
        global cleared
        run = False
        cleared = True

    def remove():
        
        remove_button.destroy()
        continue_button.destroy()
        continues()
        for files in range(0,len(files_list)):
            fil = files_list[files].replace(path[files],"")
            copied_files.insert(END,"removing " + fil)
            copied_files.update()
            copied_files.see(END)
            os.remove(files_list[files])
        for root,dirs,files in os.walk(src):
            
            lists = os.listdir(root)
            
            if len(lists) == 0:
                os.removedirs(root)
            else:
                pass
        copied_files.insert(END,str(length) + " files were copied and removed from "+src+" into "+dst)
        copied_files.see(END)
    
    if run == True:
        return

    clear_button = Button(buttonframe, text="clear", command = clear)
    continue_button = Button(root, text="copy", command = continues)
    remove_button = Button(root, text="remove+copy", command = remove)
    
    if cleared == True:
        clear_button.pack(side=TOP)

    continue_button.pack(side=RIGHT)
    remove_button.pack(side=RIGHT)
    run = True
    cleared = False


root = Tk() 
root.title("file mover")

def button():

    if file_src.get() == "":
        file_src.insert(0,"/home/bryan/music3")
    if file_dst.get() == "":
        file_dst.insert(0,"/home/bryan/music4")
    if file_type.get() == "":
        file_type.insert(0, ".mp3")
    transfer_music(file_src.get(),file_dst.get(),file_type.get())


textframe = Frame(root) 
labelframe = Frame(root)
listframe = Frame(root) 
buttonframe = Frame(root)
button1 = Button(buttonframe, text="Submit", command = button) 
src_lab = Label(labelframe, text="Source:")
dst_lab = Label(labelframe, text="Destination:")
file_lab = Label(labelframe, text="File Type:")
file_src = Entry(textframe)
file_src.insert(0,"/home/bryan/music3")
file_dst = Entry(textframe)
file_dst.insert(0,"/home/bryan/music4") 
file_type = Entry(textframe)
file_type.insert(0, ".mp3")
copied_files = Listbox(listframe, width = 50)
scrollbar = Scrollbar(listframe)
scrollbar.pack(side=RIGHT, fill=Y)
src_lab.grid(row=0,column=0,)
dst_lab.grid(row=0,column=1,padx=130)
file_lab.grid(row=0,column=2)
file_src.pack(side=LEFT) 
file_dst.pack(side=LEFT)
file_type.pack(side=LEFT)
file_src.config(width=22)
file_dst.config(width=25)
file_type.config(width=13)
button1.pack(side=TOP) 
copied_files.pack(side=RIGHT)
labelframe.pack(fill=BOTH)
textframe.pack(fill=BOTH, expand=1) 
buttonframe.pack(fill=BOTH, side=LEFT)
listframe.pack(fill=BOTH, expand=1)
copied_files.config(yscrollcommand=scrollbar.set)
scrollbar.config(command=copied_files.yview)
root.mainloop() 

