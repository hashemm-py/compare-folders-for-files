# Imports required for the functions
import sys
import os
from filecmp import dircmp


# All Functions
# Function to compare the folders and files
def print_diff_files(comp_files):
    try:
        for name in comp_files.diff_files:
            print("Different file %s found in %s and %s" % (name, comp_files.left, comp_files.right))
        for sub_comp_files in comp_files.subdirs.values():
            print(print_diff_files(sub_comp_files))
    except Exception as e:
        return 'Error in function print_diff_files : ' + str(e)


# Function to show the mis-match data in output file
def find(substr, infile, outfile):
    try:
        with open(infile) as a, open(outfile, 'w') as b:
            for line in a:
                if substr in line:
                    b.write(line) #  + '\n'
        a.close()
        b.close()
    except Exception as e:
        return 'Error in function find : ' + str(e)


# Function to find the folder size
def folder_size(start_path, folder_name):
    try:
        total_size_bytes = 0
        total_size_mb = 0
        for path, dirs, files in os.walk(start_path):
            for f in files:
                fp = os.path.join(path, f)
                total_size_bytes += os.path.getsize(fp)
                total_size_mb = (total_size_bytes / 1024) / 1024
        print("Size: " + folder_name + ": "+ str(round(total_size_mb, 2)) + " MB")
    except Exception as e:
        return 'Error in function folder_size : ' + str(e)


# Function for the full run - All Running Functions into text files
# This part will put the compare report in a text file
def full_run():
    try:
        file = open('FullResult.txt', 'w') # , encoding='utf-8')
        sys.stdout = file

        print_diff_files(comp_files)
        # comp_files.report_partial_closure()  # Partial report is good. But for this one we need complete report.
        comp_files.report_full_closure()  # Generates full report
        # comp_files.report()  # Shows a small report with no data on sub-directory related data. So not really useful.
        print('\n')
        folder_size(comp_from_path, folder_name_from)
        folder_size(comp_to_path, folder_name_to)

        file.close()
    except Exception as e:
        return 'Error in function full_run : ' + str(e)


# All Variables
# Variable for comparing the folders and file
comp_from_path = 'E:\\'
folder_name_from = 'Internal Folder'
comp_to_path = 'H:\\Back-Up'
folder_name_to = 'External Backup'
comp_files = dircmp(comp_from_path, comp_to_path, ignore=['BIN'])


# All Function Runs
# Puts compare report in a text file
full_run()


# Generates result for Mis-Match Folder and Files
find('Only in', 'FullResult.txt', 'MissingFolderAndFiles.txt')


# Generates result for Mis-Match Files
find('Different file', 'FullResult.txt', 'MissingFiles.txt')


# Generates result for sizes
find('Size: ', 'FullResult.txt', 'SizeFiles.txt')
