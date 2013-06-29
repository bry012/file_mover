#!/usr/bin/env python
# -*- coding: utf-8 -*-

from Tkinter import * 
import tkFileDialog
root = Tk() 
import os, os.path, shutil
import sqlite3 #becuase we are using cx_freeze 
import sys
import copy 

class Program:
    def __init__(self):
        self.run = False
        self.cleared = True
        self.files_moved = 0
        self.files_list = []
        self.dst_list = []
        self.length = 0
        self.src = ""
        self.dst = ""
        self.file_type = ""
        self.type_list = []
        self.exclusion_list = []
    def move_music(self):

        """Copies files from source directory to destination directory"""
        self.files_moved = len(self.files_list)
        for files in self.files_list:
            dst_path = files.replace(self.src,self.dst)
            (root,file_name) = os.path.split(files)
            (dst_root,dst_file) = os.path.split(dst_path)
            GUI.copied_files.insert(END, "copying %s" % file_name)
            GUI.copied_files.update()
            GUI.copied_files.see(END)
            
            if not os.path.exists(dst_root): 
                os.makedirs(dst_root)

            shutil.copyfile(files,dst_root+"/"+dst_file)
        return self.files_moved
        
    def transfer_music(self):
        self.exclusion_list = []
        self.type_list = []
        """scans source and destination directories for duplicates, directory existence and number of files to be
            moved"""
        self.src = GUI.file_src.get()
        self.dst = GUI.file_dst.get()
        
        if not os.path.exists(self.src):
            GUI.copied_files.insert(END,"The source directory doesn't exist.")
        

        else: 
            if not os.path.exists(self.dst):
                   GUI.copied_files.insert(END,"The destination directory doesn't exist. A directory will be created upon copying.")
            #splits input entered in file_type box by ",".
            self.type_list = GUI.file_type.get().split(",")
            
            #iterates through type_list to append file types that are to be excluded to the exclusion list
            for types in self.type_list:
                if types.startswith("-"):
                    file_type = types[1::]
                    self.exclusion_list.append(file_type)

            #walks source directory and destination directory, checks for duplicate files and assigns a list without
            #duplicates to files_in_source
            files_in_source = copy.check_for_duplicates(copy.walk_dir(self.src,self.type_list,self.exclusion_list),\
                                                   copy.walk_dir(self.dst,self.type_list,self.exclusion_list),GUI.copied_files,END)
            self.files_list = files_in_source
            
            #inform the user that file exist and exit the program
            if (len(self.files_list) != 0):
                GUI.copied_files.insert(END,"%d files, %s will be copied and moved."
                 % (len(self.files_list),copy.get_size(files_in_source)))
                GUI.copied_files.insert(END,"Would you like to remove from source, also?") 
                
            else:
                GUI.copied_files.insert(END,'Files already exist in destination.')
                return

            #prevents multiple clear, remove, continue buttons from being created
            if self.run:
                return

            #checks if listbox is cleared. If not cleared, creates clear button 
            if self.cleared:
                GUI.clear_button.grid(row=0,column=1,sticky=W)

            GUI.continue_button.grid(row=0,column=2,sticky=W)
            GUI.remove_button.grid(row=0,column=3,sticky=W)
            self.run = True
            self.cleared = False

    
    def continues(self,removed = False):

        """initiates copying of files to new directory"""

        GUI.copied_files.insert(END,"%d files were copied and moved to %s" % (self.move_music(), self.dst))
        GUI.copied_files.see(END)
        GUI.continue_button.grid_remove()
        GUI.remove_button.grid_remove()
        
        if not removed:
            self.run = False
            self.files_list = []
            self.dst_list = []
    
    def clear(self):

        """clears listbox"""

        GUI.copied_files.delete(0,END)
        GUI.clear_button.grid_remove()
        GUI.continue_button.grid_remove()
        GUI.remove_button.grid_remove()
        self.run = False
        self.cleared = True

    
    def remove(self):
        from copy import remove_files
        """initiates copying of files to new directory and deletion of copied files from source directory"""

        GUI.remove_button.grid_remove()
        GUI.continue_button.grid_remove()
        self.continues(True)
        
        remove_files(self.files_list)

        GUI.copied_files.insert(END,"%d files were removed from %s" % (self.files_moved, self.src))
        GUI.copied_files.see(END)
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
    copied_files = Listbox(listframe, width = 63,bg="black",fg="#33CCCC", yscrollcommand=scrollbar.set)
    menubar = Menu(root)
    filemenu = Menu(menubar, tearoff=0)
    submit = Button(buttonframe, text="Submit") 
    open_ = Button(srcframe, text='Open')#me
    open1_ = Button(srcframe, text='Open')#me

    clear_button = Button(buttonframe,text="clear")
    continue_button = Button(buttonframe, text="copy")
    remove_button = Button(buttonframe, text="remove+copy")
    roots = Toplevel()
    roots.title("Defaults")
    roots.protocol("WM_DELETE_WINDOW", roots.withdraw)
    roots.withdraw()

    open2_ = Button(roots, text='Open')#me
    open3_ = Button(roots, text='Open')#me
    src_lab_def = Label(roots, bg="black", fg="#33CCCC", text="Source:")
    dst_lab_def = Label(roots, bg="black", fg="#33CCCC", text="Destination:")
    file_lab_def = Label(roots, bg="black", fg="#33CCCC", text="File Type:")
    file_src_def = Entry(roots, insertbackground="#33CCCC",bg="black",fg="#33CCCC")
    file_dst_def = Entry(roots,insertbackground="#33CCCC",bg="black",fg="#33CCCC")
    file_type_def = Entry(roots,insertbackground="#33CCCC",bg="black",fg="#33CCCC")
    save_button = Button(roots,text="Save")

    def defaults(self,second_run=True):

        """Pulls default source, destination and file type from sqsqlite33 database"""

        if second_run:
            self.defaults_window()

        con = sqlite3.connect('file_mover.db')
        with con:
            cur = con.cursor()
            cur.execute("CREATE TABLE IF NOT EXISTS Settings(id INT, src_def TEXT, dst_def TEXT, type_def TEXT)")
            cur.execute("SELECT * FROM Settings")
            sets = cur.fetchall()
            if len(sets) > 0: 
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

            else:
                self.file_src_defs = "insert a source path"
                self.file_dst_defs = "insert a destination path"
                self.file_type_defs = "insert a file type"

    

    def submit_button(self):

        """initiates scanning of source directory/ destination directory"""

        #prevents user input from being none
        #prevents programing from running if no input
        empty = False
        if not self.file_src.get():
            self.file_src.insert(0,self.file_src_defs)
            empty = True
        if not self.file_dst.get():
            self.file_dst.insert(0,self.file_dst_defs)
            empty = True
        if not self.file_type.get():
            self.file_type.insert(0, self.file_type_defs)
            empty = True
        if not empty:
            file_mover.files_list = []
            file_mover.exclusion_list = []
            file_mover.transfer_music()

    #give user the opportunity to select a folder 
    def getDirSrc(self,file_src):
        file_src.delete(0,END)
        file_src.insert(0, tkFileDialog.askdirectory(parent=root, title='Select a folder'))
    def getDirDst(self,file_dst):
        file_dst.delete(0,END)
        file_dst.insert(0, tkFileDialog.askdirectory(parent=root, title='Select a folder'))

    def create(self):

        """constructs main file mover window. Self is only argument"""

        self.submit.config(command = self.submit_button,fg="#33CCCC", bg="black",highlightbackground="#33CCCC",activebackground="#33CCCC",activeforeground="white")
        self.clear_button.config(bg="black",fg="#33CCCC", command = file_mover.clear,highlightbackground="#33CCCC",activebackground="#33CCCC",activeforeground="white")
        self.continue_button.config(bg="black",fg="#33CCCC",  command = file_mover.continues,highlightbackground="#33CCCC",activebackground="#33CCCC",activeforeground="white")
        self.remove_button.config(bg="black",fg="#33CCCC",  command = file_mover.remove,highlightbackground="#33CCCC",activebackground="#33CCCC",activeforeground="white")
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

        # get folder buttons 
        self.open_.config(command = lambda:self.getDirSrc(self.file_src),fg="#33CCCC", bg="black",highlightbackground="#33CCCC",activebackground="#33CCCC",activeforeground="white")
        self.open1_.config(command = lambda:self.getDirDst(self.file_dst),fg="#33CCCC", bg="black",highlightbackground="#33CCCC",activebackground="#33CCCC",activeforeground="white")
        self.open_.grid(row=0,column=2,sticky=W)
        self.open1_.grid(row=1,column=2,sticky=W)
       
        self.file_src.config(highlightbackground="#33CCCC",width=55)
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

        """saves default source and destination directories along with file type to sqsqlite3 database 'Settings'"""

        settings = (
            (1,self.file_src_def.get(),self.file_dst_def.get(),self.file_type_def.get())
            )

        con = sqlite3.connect('file_mover.db')
        
        with con:
            cur = con.cursor()    
            cur.execute("DROP TABLE IF EXISTS Settings")
            cur.execute("CREATE TABLE Settings(id INT, src_def TEXT, dst_def TEXT, type_def TEXT)")  
            cur.execute("INSERT INTO Settings VALUES(?,?,?,?)", settings)
        self.roots.withdraw()
        self.defaults(False)   
            
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
        self.open2_.config(command = lambda:self.getDirSrc(self.file_src_def),fg="#33CCCC", bg="black",highlightbackground="#33CCCC",activebackground="#33CCCC",activeforeground="white")
        self.open3_.config(command = lambda:self.getDirDst(self.file_dst_def),fg="#33CCCC", bg="black",highlightbackground="#33CCCC",activebackground="#33CCCC",activeforeground="white")
        self.open2_.grid(row=0,column=2,sticky=W)
        self.open3_.grid(row=1,column=2,sticky=W)
        self.file_src_def.delete(0,END)
        self.file_dst_def.delete(0,END)
        self.file_type_def.delete(0,END)
        self.file_src_def.insert(0, self.file_src_defs)
        self.file_dst_def.insert(0, self.file_dst_defs)
        self.file_type_def.insert(0, self.file_type_defs) 

GUI = Window()
file_mover = Program()
GUI.defaults(False)
GUI.create()
