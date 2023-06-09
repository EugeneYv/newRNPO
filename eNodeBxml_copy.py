import os
import shutil

''' код для xml файлов с eNodeB, копирование файлов из отдельных папок в общую папку'''

working_directory = 'C:/temp/try2/eNodeB/UH/'
destination_directory = 'C:/temp/try4/'
for r,d,f in os.walk(working_directory):
    print(f'root={r}, dirnames={d}, filenames={f}')
    for files in f:
        filepath = os.path.join(os.getcwd(),working_directory, r, files)
        shutil.copy(filepath,destination_directory)
#    shutil.rmtree(os.path.join(os.getcwd(),files_path,r))
# for r,d,f in os.walk(working_directory):
#     shutil.rmtree(os.path.join(os.getcwd(), working_directory, r))