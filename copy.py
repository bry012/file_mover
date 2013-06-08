import os, os.path, shutil

def copy_files(src,dst,files_list):
        """Copies files from source directory to destination directory"""
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
       the type_list or exclusion_list."""
    desired_files = []
    total_size = 0
    for root,dirs,files in os.walk(src):
        
        for filed in files:
            file_path = os.path.join(root, filed)
            total_size += os.path.getsize(file_path)
            (files,extension) = os.path.splitext(filed)
            
            if extension in type_list and not exclusion_list:
                desired_files.append(root+"/"+filed)
            
            elif extension not in exclusion_list and exclusion_list:
                desired_files.append(root+"/"+filed)
        
        for dire in dirs:
            directory_path = os.path.join(root, dire)
            total_size += os.path.getsize(directory_path)
            
    return [desired_files,total_size]

def remove_files(files_list):
        """removes files and empty directories in list of files passed to function"""
        for files in files_list:
            (directory_path,file_path) = os.path.split(files)
            os.remove(files)
            
            if not os.listdir(directory_path):
               os.removedirs(directory_path) 

def get_size(total_size):
    """Takes size as bytes and converts size into readable SI form and Gebibyte form"""
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
