#!/usr/local/Cellar/python3/3.5.1/Frameworks/Python.framework/Versions/3.5/bin/python3.5
# coding=<UTF-8>
import os
import codecs
import webbrowser

class FileSorter:
    def sort_files():
        file_list = []
        for item in os.listdir():
            if os.path.isdir(item):
                os.chdir(os.getcwd()+'/'+item+'/')
                next_line = (FileSorter.sort_files())
                next_line.insert(0,item)
                os.chdir('..')
            else:
                next_line = [item]
            file_list.append(next_line)
        return file_list

    def parse_txt(file_list,tabbing):
        content = ''
        for item in file_list:
            if len(item) > 1 and isinstance(item,list):
                if len(tabbing) > 0:
                    content += '\n' + tabbing[:-2] + '↳'
                else:
                    content += '\n' + tabbing
                content += item[0]
                tabbing += '  '
                in_item = []
                x = 0
                for things in item:
                    if x != 0: in_item.append(item[x])
                    x += 1
                content += FileSorter.parse_txt(in_item,tabbing)
                tabbing = tabbing[:-2]
            else:
                if len(tabbing) > 0:
                    content += '\n' + tabbing[:-2] + '↳'
                else:
                    content += '\n' + tabbing
                if isinstance(item,list): content += item[0]
                else: content += item
        return content


    def write(file_name,file_extension,content):
        file = file_name+file_extension
        with codecs.open('fileindex'+file,'w',encoding='utf8') as text_file:
            text_file.write(content)

'''def sort_files(tabbing):
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
'''
file_list = FileSorter.sort_files()
content = FileSorter.parse_txt(file_list,'')
FileSorter.write('fileindex','.txt',content)
