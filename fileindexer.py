#!/usr/local/Cellar/python3/3.5.1/Frameworks/Python.framework/Versions/3.5/bin/python3.5
# coding=<UTF-8>
import os
import codecs

class FileSorter:
    def sort_files_hyperlink(location):
        hyperlink_list = []
        for item in os.listdir():
            if os.path.isdir(item):
                os.chdir(os.getcwd()+'/'+item+'/')
                next_line = FileSorter.sort_files_hyperlink(os.getcwd())
                next_line.insert(0,'file://'+os.getcwd()+'/'+item)
                os.chdir('..')
            else:
                next_line = ['file://'+os.getcwd()+'/'+item]
            hyperlink_list.append(next_line)
        return hyperlink_list

    def sort_files_name(location):
        os.chdir(location)
        file_list = []
        for item in os.listdir():
            if os.path.isdir(item):
                os.chdir(os.getcwd()+'/'+item+'/')
                next_line = FileSorter.sort_files_name(os.getcwd())
                next_line.insert(0,item)
                os.chdir('..')
            else:
                next_line = [item]
            file_list.append(next_line)
        return file_list

    def write_txt(file_list):
        content = '*** SORTED FILES ***'
        content += FileSorter.parse_txt(file_list,'')
        FileSorter.write('fileindex','.txt',content)

    def parse_txt(file_list,tabbing):
        content = ''
        for item in file_list:
            if len(item) > 1 and isinstance(item,list):
                if len(tabbing) > 0:
                    content += '\n' + tabbing[:-4] + '↳ '
                else:
                    content += '\n' + tabbing
                content += item[0]
                tabbing += '    '
                in_item = []
                x = 0
                for things in item:
                    if x != 0: in_item.append(item[x])
                    x += 1
                content += FileSorter.parse_txt(in_item,tabbing)
                tabbing = tabbing[:-4]
            else:
                if len(tabbing) > 0:
                    content += '\n' + tabbing[:-4] + '↳ '
                else:
                    content += '\n' + tabbing
                if isinstance(item,list): content += item[0]
                else: content += item
        return content

    def write_rtf(file_list,file_list_hyperlink):
        content = '{\\rtf1\\ansi\\deff0\n***SORTED FILES***'
        content += FileSorter.parse_rtf(file_list,file_list_hyperlink,'')
        content += '}'
        FileSorter.write('fileindex','.rtf',content)

    def parse_rtf(file_list,file_list_hyperlink,tabbing):
        content = ''
        file_list_hyperlink = file_list_hyperlink
        y = 0
        for item in file_list:
            if len(item) > 1 and isinstance(item,list):
                if len(tabbing) > 0:
                    content += '\\line\n' + tabbing[:-4] + '- '
                else:
                    content += '\\line\n' + tabbing
                content += '{\\field{\*\\fldinst HYPERLINK "'+file_list_hyperlink[y][0]+ '"}{\\fldrslt{\\ul\\cf1'+item[0]+'}}}'
                tabbing += '\\tab'
                in_item = []
                in_item_hyperlink = []
                x = 0
                for things in item:
                    if x != 0:
                        in_item.append(item[x])
                        in_item_hyperlink.append(file_list_hyperlink[y][x])
                    x += 1
                content += FileSorter.parse_rtf(in_item,in_item_hyperlink,tabbing)
                tabbing = tabbing[:-4]
            else:
                if len(tabbing) > 0:
                    content += '\\line\n' + tabbing[:-4] + '- '
                else:
                    content += '\\line\n' + tabbing
                if isinstance(item,list):
                    content += '{\\field{\*\\fldinst HYPERLINK "'+file_list_hyperlink[y][0]+ '"}{\\fldrslt{\\ul\\cf1'+item[0]+'}}}'
                else:
                    content += '{\\field{\*\\fldinst HYPERLINK "'+file_list_hyperlink[y]+ '"}{\\fldrslt{\\ul\\cf1'+item+'}}}'
            y += 1
        return content

    def write(file_name,file_extension,content):
        file = file_name+file_extension
        with codecs.open(file,'w',encoding='utf8') as text_file:
            text_file.write(content)

location = './'
FileSorter.write_txt(FileSorter.sort_files_name(location))
FileSorter.write_rtf(FileSorter.sort_files_name(location),FileSorter.sort_files_hyperlink(location))
