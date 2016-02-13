#!/usr/local/Cellar/python3/3.5.1/Frameworks/Python.framework/Versions/3.5/bin/python3.5
import os
print('*** File Contents ***')
def sort_files(tabbing):
    list = ''
    for item in os.listdir():
        next_line = '\n'+tabbing+(item)
        print(next_line)
        list += next_line
        if os.path.isdir(item):
            tabbing+='    '
            os.chdir(os.getcwd()+'/'+item+'/')
            list += sort_files(tabbing)
            tabbing = tabbing[:-4]
            os.chdir('..')
    return list


with open('fileindex.txt','w') as text_file:
    text_file.write('*** File Contents ***')
    text_file.write(sort_files(''))
