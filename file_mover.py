#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import * 
root = Tk() 
import os, os.path,shutil
import sqlite3 as lite
import sys

class Program:
    run = False
    cleared = True
    files_moved = 0
    files_list = []
    dst_list = []
    length = 0
    src = ""
    dst = ""
    file_type = ""
    type_list = []

    def move_music(self):

        """Copies files from source directory to destination directory"""
        self.files_moved = len(self.files_list)
        print self.files_moved
        for files in self.files_list:
            file_index = self.files_list.index(files)
            #removes complete path from file name
            (root,file_name) = os.path.split(files)
            
            bryan.copied_files.insert(END, "copying %s" % file_name)
            bryan.copied_files.update()
            bryan.copied_files.see(END)
            
            if not os.path.exists(self.dst_list[file_index]): 
                os.makedirs(self.dst_list[file_index])

            shutil.copyfile(files, "%s/%s" % (self.dst_list[file_index],file_name))
        return self.files_moved
        



    def transfer_music(self):

        """scans source and destination directories for duplicates, directory existence and number of files to be
            moved"""
        self.src = bryan.file_src.get()
        self.dst = bryan.file_dst.get()
        self.type_list = bryan.file_type.get().split(",")
         
        
        #"walks" through destination directory and creates list of existing files to prevent duplicates when 
        #copying
        def walk():
            list1 = []
            list2 = []
            for root,dirs,files in os.walk(self.dst):
                list1 += files
            for f in list1:
                (files,extension) = os.path.splitext(f)
                if extension in self.type_list:
                    list2.append(f)

            return list2

        files_in_dst = walk()

        #checks if user's source directory exists
        if not os.path.isdir(self.src):
            bryan.copied_files.insert(END, "The source directory doesn't exist!")
            bryan.copied_files.update()
            return

        #evaluates directory before copying/removing process begins to alert user of amount of files to be moved
        def evaluate_directory (src,dst,files_in_dst):
            
            listOfFiles = os.listdir(src)

            for file in listOfFiles:
                (files,extension) = os.path.splitext(file)
                if file.startswith("."):
                    pass
                elif os.path.isdir("%s/%s" % (src,file)):
                    new_src = "%s/%s" % (src,file)
                    new_dst = "%s/%s" % (dst,file)
                    evaluate_directory(new_src, new_dst,files_in_dst)
                elif extension in self.type_list and not os.path.exists("%s/%s" % (dst,file)):
                        if any(s.endswith(file) for s in self.files_list):
                            pass
                        elif any(t.endswith(file) for t in files_in_dst):
                            pass
                        else:
                            self.files_list.append("%s/%s" % (src,file))
                            self.dst_list.append(dst)
    
            print len(self.files_list)
            return len(self.files_list)
        
        bryan.copied_files.insert(END,
         "%d files will be copied and moved. Would you like to remove from source, also?" 
         % (evaluate_directory(self.src, self.dst, files_in_dst)))
        
        #prevents multiple clear, remove, continue buttons from being created
        if self.run:
            return

        #checks if listbox is cleared. If not cleared, creates clear button 
        if self.cleared:
            bryan.clear_button.grid(row=0,column=1,sticky=W)

        bryan.continue_button.grid(row=0,column=2,sticky=W)
        bryan.remove_button.grid(row=0,column=3,sticky=W)
        self.run = True
        self.cleared = False

    
    def continues(self,removed = False):

        """initiates copying of files to new directory"""
        for x in self.files_list: print x
        bryan.copied_files.insert(END,"%d files were copied and moved to %s" % (self.move_music(), self.dst))
        bryan.copied_files.see(END)
        bryan.continue_button.grid_remove()
        bryan.remove_button.grid_remove()
        
        if not removed:
            self.run = False
            self.files_list = []
            self.dst_list = []
    
    def clear(self):

        """clears listbox"""

        bryan.copied_files.delete(0,END)
        bryan.clear_button.grid_remove()
        bryan.continue_button.grid_remove()
        bryan.remove_button.grid_remove()
        self.run = False
        self.cleared = True

    
    def remove(self):

        """initiates copying of files to new directory and deletion of copied files from source directory"""

        bryan.remove_button.grid_remove()
        bryan.continue_button.grid_remove()
        self.continues(True)
        
        #writes file names to listbox and removes files from source
        for files in self.files_list:
            (root,fil) = os.path.split(files)
            bryan.copied_files.insert(END,"removing %s" % fil)
            bryan.copied_files.update()
            bryan.copied_files.see(END)
            os.remove(files)

        #removes directory(folder) if directory contains no files
        for root,dirs,files in os.walk(self.src):
            lists = os.listdir(root)
            if len(lists) == 0:
                os.removedirs(root)
            else:
                pass
        bryan.copied_files.insert(END,"%d files were removed from %s" % (self.files_moved, self.src))
        bryan.copied_files.see(END)
        self.files_list = []
        self.dst_list = []
        self.run = False

class Window:

    buttonframe=Frame(root)
    srcframe=Frame(root)
    listframe=Frame(root)
    
    src_lab = Label(srcframe, bg="black", fg="#33CCCC", text="Source:")
    dst_lab = Label(srcframe, bg="black", fg="#33CCCC", text="Destination:")
    file_lab = Label(srcframe, bg="black", fg="#33CCCC", text="File Type:")
    file_src = Entry(srcframe,insertbackground="#33CCCC",bg="black",fg="#33CCCC")
    file_dst = Entry(srcframe,insertbackground="#33CCCC",bg="black",fg="#33CCCC")
    file_type = Entry(srcframe,insertbackground="#33CCCC",bg="black",fg="#33CCCC")
    scrollbar = Scrollbar(listframe)
    copied_files = Listbox(listframe, width = 60,bg="black",fg="#33CCCC", yscrollcommand=scrollbar.set)
    menubar = Menu(root)
    filemenu = Menu(menubar, tearoff=0)
    submit = Button(buttonframe, text="Submit") 
    clear_button = Button(buttonframe,text="clear")
    continue_button = Button(buttonframe, text="copy")
    remove_button = Button(buttonframe, text="remove+copy")
    roots = Toplevel()
    roots.title("Defaults")
    roots.protocol("WM_DELETE_WINDOW", roots.withdraw)
    roots.withdraw()

    src_lab_def = Label(roots, bg="black", fg="#33CCCC", text="Source:")
    dst_lab_def = Label(roots, bg="black", fg="#33CCCC", text="Destination:")
    file_lab_def = Label(roots, bg="black", fg="#33CCCC", text="File Type:")
    file_src_def = Entry(roots, insertbackground="#33CCCC",bg="black",fg="#33CCCC")
    file_dst_def = Entry(roots,insertbackground="#33CCCC",bg="black",fg="#33CCCC")
    file_type_def = Entry(roots,insertbackground="#33CCCC",bg="black",fg="#33CCCC")
    save_button = Button(roots,text="Save")

    def defaults(self,second_run=True):

        """Pulls default source, destination and file type from sqlite3 database"""

        if second_run:
            self.defaults_window()

        con = lite.connect('file_mover.db')
        with con:
            cur = con.cursor()
            cur.execute("SELECT * FROM Settings")
            sets = cur.fetchall() 
            self.file_src_defs = sets[0][1]
            self.file_dst_defs = sets[0][2]
            self.file_type_defs = sets[0][3] 
              
            self.file_src.delete(0,END)
            self.file_dst.delete(0,END)
            self.file_type.delete(0,END)
            self.file_src.insert(0, self.file_src_defs)
            self.file_dst.insert(0, self.file_dst_defs) 
            self.file_type.insert(0, self.file_type_defs)

            self.file_src.update()
            self.file_dst.update()
            self.file_type.update()
    

    def submit_button(self):

        """initiates scanning of source directory/ destination directory"""

        #prevents user input from being none
        if not self.file_src.get():
            self.file_src.insert(0,self.file_src_defs)
        if not self.file_dst.get():
            self.file_dst.insert(0,self.file_dst_defs)
        if not self.file_type.get():
            self.file_type.insert(0, self.file_type_defs)
        move.files_list = []
        move.transfer_music()

    
    def create(self):

        """constructs main file mover window. Self is only command"""

        self.submit.config(command = self.submit_button,fg="#33CCCC", bg="black",highlightbackground="#33CCCC",activebackground="#33CCCC",activeforeground="white")
        self.clear_button.config(bg="black",fg="#33CCCC", command = move.clear,highlightbackground="#33CCCC",activebackground="#33CCCC",activeforeground="white")
        self.continue_button.config(bg="black",fg="#33CCCC",  command = move.continues,highlightbackground="#33CCCC",activebackground="#33CCCC",activeforeground="white")
        self.remove_button.config(bg="black",fg="#33CCCC",  command = move.remove,highlightbackground="#33CCCC",activebackground="#33CCCC",activeforeground="white")
        self.filemenu.add_command(label="Defaults", command=self.defaults)
        self.filemenu.config(fg="#33CCCC", bg="black",activebackground="#33CCCC",activeforeground="white")
        self.menubar.add_cascade(label="Settings", menu=self.filemenu)
        self.menubar.config(fg="#33CCCC", bg="black",activebackground="#33CCCC",activeforeground="white")
        root.title("file mover")
        root.config(menu=self.menubar)
        self.src_lab.grid(row=0,column=0,sticky=W)
        self.dst_lab.grid(row=1,column=0,sticky=W)
        self.file_lab.grid(row=2,column=0,sticky=W)
        root.config(bg="black")
        self.file_src.grid(row=0,column=1,sticky=W+E) 
        self.file_dst.grid(row=1,column=1,sticky=W+E)
        self.file_type.grid(row=2,column=1,sticky=W+E)
        self.submit.grid(row=0,sticky=W)
        self.file_src.config(highlightbackground="#33CCCC",width=52)
        self.file_dst.config(highlightbackground="#33CCCC")
        self.file_type.config(highlightbackground="#33CCCC") 
        self.copied_files.grid(row=0,column=0,sticky=W)
        self.copied_files.config(yscrollcommand=self.scrollbar.set,highlightbackground="#33CCCC")
        self.scrollbar.config(command=self.copied_files.yview,bg="#33CCCC",troughcolor="black")
        self.scrollbar.grid(row=0,column=1,sticky=N+S)
        self.srcframe.config(bg="black")
        self.srcframe.grid(row=0,sticky=W+E)
        self.listframe.grid(row=1,sticky=W)
        self.buttonframe.grid(row=2,sticky=W)
        root.mainloop() 
    
    
    def save(self):

        """saves default source and destination directories along with file type to sqlite database 'Settings'"""

        settings = (
            (1,self.file_src_def.get(),self.file_dst_def.get(),self.file_type_def.get())
            )

        con = lite.connect('file_mover.db')
        
        with con:
            cur = con.cursor()    
            cur.execute("DROP TABLE IF EXISTS Settings")
            cur.execute("CREATE TABLE Settings(id INT, src_def TEXT, dst_def TEXT, type_def TEXT)")  
            cur.execute("INSERT INTO Settings VALUES(?,?,?,?)", settings)
        self.roots.withdraw()
        self.defaults(False)   
        print "saved"
    
            
    def defaults_window(self):
        
        """Constructs window for changing of defaults"""
        
        self.roots.config(bg="black")
        self.roots.deiconify()
        self.save_button.config(command=self.save,fg="#33CCCC", bg="black",highlightbackground="#33CCCC",activebackground="#33CCCC",activeforeground="white")
        self.src_lab_def.grid(row=0,column=0,sticky=W)
        self.dst_lab_def.grid(row=1,column=0,sticky=W)
        self.file_lab_def.grid(row=2,column=0,sticky=W)
        self.file_src_def.grid(row=0,column=1,sticky=W)
        self.file_dst_def.grid(row=1,column=1,sticky=W)
        self.file_type_def.grid(row=2,column=1,sticky=W)
        self.save_button.grid(row=3,sticky=W)
        self.file_src_def.delete(0,END)
        self.file_dst_def.delete(0,END)
        self.file_type_def.delete(0,END)
        self.file_src_def.insert(0, self.file_src_defs)
        self.file_dst_def.insert(0, self.file_dst_defs)
        self.file_type_def.insert(0, self.file_type_defs) 

bryan = Window()
move = Program()
bryan.defaults(False)
bryan.create()
