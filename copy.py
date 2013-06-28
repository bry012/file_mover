import os, os.path, shutil

def copy_files(src,dst,files_list):
        """Copies files from source directory to destination directory. Returns number of files moved"""
        files_moved = len(files_list)
        for files in files_list:
            dst_path = files.replace(src,dst)
            (dst_root,dst_file) = os.path.split(dst_path)
            
            if not os.path.exists(dst_root): 
                os.makedirs(dst_root)

            shutil.copyfile(files,dst_root+"/"+dst_file)
        return files_moved

def walk_dir(src,type_list=[],exclusion_list=[]):
    """walks source directory and filters files based on whether they are included in 
       the type_list or exclusion_list. Returns list of desired files"""
    desired_files = []

    for root,dirs,files in os.walk(src):
        
        for filed in files:
            file_path = os.path.join(root, filed)
            (files,extension) = os.path.splitext(filed)
            
            if extension in type_list and not exclusion_list:
                desired_files.append(root+"/"+filed)
            
            elif extension not in exclusion_list and exclusion_list:
                desired_files.append(root+"/"+filed)
            
    return desired_files

def remove_files(files_list):
        """removes files and empty directories in list of files passed to function"""
        for files in files_list:
            (directory_path,file_path) = os.path.split(files)
            os.remove(files)
            
            if not os.listdir(directory_path):
               os.removedirs(directory_path) 

def get_size(files_list):
    """Iterates through file list and converts size into readable SI form and Gebibyte form. Returns string."""

    total_size = 0
    dirs_list = []
    for file_path in files_list:
        (root,files) = os.path.split(file_path)
        total_size += os.path.getsize(file_path)
        
        #adds size of directories themselves into total size
        if root not in dirs_list:
            total_size += os.path.getsize(root)
            dirs_list.append(root)
    
    #beginning of conversion process
    in_si = [[1,'b'],[1000,'Kb'],[1000**2,'Mb'],[1000**3,'Gb'],[1000**4,"Tb"]]
    in_byt = [[1,'ib'],[1024,'Kib'],[1024**2,'Mib'],[1024**3,'Gib'],[1024**4,"Tib"]]
    B = 0
    iB = 0
    ending = ""
    ending2 = ""
    total_size += 0.1
    for x in range(len(in_si)):
    
        if total_size/in_si[x][0] >= 1:
            B = (total_size/in_si[x][0])
            ending = in_si[x][1]
        
        if total_size/in_byt[x][0] >= 1:
            iB = (total_size/in_byt[x][0])
            ending2 = in_byt[x][1]
    
    return  "%0.2f %s and %0.2f %s" % (B, ending, iB, ending2)

def check_for_duplicates(src_list,dst_list,guiObject,END):
    """Sorts through two lists of files and creates new list without duplicates"""
    src_files = list(src_list)
    #naming is confussing 
    for files in src_list:
        (srcRoot,srcFile_name) = os.path.split(files)
        for files_in_dst in dst_list:
            (dstRoot,dstFile_name) = os.path.split(files_in_dst)
            if dstFile_name == srcFile_name:
                #informs user of duplicate file 
                guiObject.insert(END,'%s exists'%srcFile_name)
                print files in src_files
                try:
                    src_files.remove(files)
                except:
                    print files
    return src_files
