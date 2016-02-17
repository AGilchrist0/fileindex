#!/usr/local/Cellar/python3/3.5.1/Frameworks/Python.framework/Versions/3.5/bin/python3.5
import os
import codecs
import argparse
import logging as log

parser = argparse.ArgumentParser()
parser.add_argument('filename', nargs='?', help='Chooses file name to output to.', default='fileindex')
parser.add_argument('fileformat', help='Chooses file type to output to.', nargs='?', choices=('txt', 'rtf', 'md'), default='txt')
parser.add_argument('location', help='Chooses file location to index.', nargs='?', default='./')
parser.add_argument('-v', '--verbose', help='Makes program more verbose.', action='store_true')
parser.add_argument('-a', '--allfiles', help='Index all files, including dotfiles.', action='store_true')
args = parser.parse_args()

def sort_files_hyperlink(location):
    include_dotfiles = args.allfiles
    hyperlink_list = []
    for item in os.listdir(os.getcwd()):
        # Exclude dotfiles by removing all files that begin with '.'
        if not include_dotfiles:
            if item[0] == '.':
                continue
        if os.path.isdir(item):
            os.chdir(os.getcwd()+'/'+item+'/')
            next_line = sort_files_hyperlink(os.getcwd())
            next_line.insert(0,'file://'+os.getcwd()+'/'+item)
            os.chdir('..')
        else:
            next_line = ['file://'+os.getcwd()+'/'+item]
        hyperlink_list.append(next_line)
        log.info(str(next_line) + ' sorted.')
    return hyperlink_list

def sort_files_name(location):
    os.chdir(location)
    include_dotfiles = args.allfiles
    file_list = []
    for item in os.listdir(os.getcwd()):
        # Exclude dotfiles by removing all files that begin with '.'
        if not include_dotfiles:
            if item[0] == '.':
                continue
        if os.path.isdir(item):
            os.chdir(os.getcwd()+'/'+item+'/')
            next_line = sort_files_name(os.getcwd())
            next_line.insert(0,item)
            os.chdir('..')
        else:
            next_line = [item]
        file_list.append(next_line)
        log.info(str(next_line) + ' sorted.')
    return file_list

def write_txt(file_name, location):
    file_list = sort_files_name(location)
    log.info('*** Files sorted ***')
    content = '*** SORTED FILES ***'
    content += parse_txt(file_list,'')
    log.info('*** txt parsed ***')
    write(file_name,'.txt',content)

def parse_txt(file_list,tabbing):
    content = ''
    for item in file_list:
        if len(item) > 1 and isinstance(item,list):
            if len(tabbing) > 0:
                content += '\n' + tabbing[:-4] + '- '
            else:
                content += '\n' + tabbing
            content += item[0]
            tabbing += '    '
            in_item = []
            x = 0
            for things in item:
                if x != 0: in_item.append(item[x])
                x += 1
            content += parse_txt(in_item,tabbing)
            tabbing = tabbing[:-4]
        else:
            if len(tabbing) > 0:
                content += '\n' + tabbing[:-4] + '- '
            else:
                content += '\n' + tabbing
            if isinstance(item,list): content += item[0]
            else: content += item
    return content

def write_rtf(file_name,location):
    file_list = sort_files_name(location)
    log.info('*** Files sorted ***')
    file_list_hyperlink = sort_files_hyperlink(location)
    content = '{\\rtf1\\ansi\\deff0\n***SORTED FILES***'
    content += parse_rtf(file_list,file_list_hyperlink,'')
    content += '}'
    log.info('*** rtf parsed ***')
    write(file_name,'.rtf',content)

def parse_rtf(file_list,file_list_hyperlink,tabbing):
    content = ''
    file_list_hyperlink = file_list_hyperlink
    y = 0
    for item in file_list:
        if len(item) > 1 and isinstance(item,list):
            if len(tabbing) > 0:
                content += '\\line\n' + tabbing#[:-4] + '- '
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
            content += parse_rtf(in_item,in_item_hyperlink,tabbing)
            tabbing = tabbing[:-4]
        else:
            if len(tabbing) > 0:
                content += '\\line\n' + tabbing#[:-4] + '- '
            else:
                content += '\\line\n' + tabbing
            if isinstance(item,list):
                content += '{\\field{\*\\fldinst HYPERLINK "'+file_list_hyperlink[y][0]+ '"}{\\fldrslt{\\ul\\cf1'+item[0]+'}}}'
            else:
                content += '{\\field{\*\\fldinst HYPERLINK "'+file_list_hyperlink[y]+ '"}{\\fldrslt{\\ul\\cf1'+item+'}}}'
        y += 1
    return content

def write_md(file_name,location):
    file_list = sort_files_name(location)
    content = ('# Files Sorted #')
    file_list_hyperlink = sort_files_hyperlink(location)
    content += parse_md(file_list,file_list_hyperlink,' * ')
    log.info('*** Markdown parsed ***')
    write(file_name,'.md',content)

def parse_md(file_list,file_list_hyperlink,tabbing):
    content = ''
    file_list_hyperlink = file_list_hyperlink
    y = 0
    for item in file_list:
        if len(item) > 1 and isinstance(item,list):
            if len(tabbing) > 0:
                content += '\n' + tabbing
            else:
                content += '\n' + tabbing
            content += '['+item[0]+']('+file_list_hyperlink[y][0]+')'
            tabbing += ' * '
            in_item = []
            in_item_hyperlink = []
            x = 0
            for things in item:
                if x != 0:
                    in_item.append(item[x])
                    in_item_hyperlink.append(file_list_hyperlink[y][x])
                x += 1
            content += parse_md(in_item,in_item_hyperlink,tabbing)
            tabbing = tabbing[:-3]
        else:
            if len(tabbing) > 0:
                content += '\n' + tabbing
            else:
                content += '\n' + tabbing
            if isinstance(item,list):
                content += '['+item[0]+']('+file_list_hyperlink[y][0]+')'
            else:
                content += '['+item+']('+file_list_hyperlink[y]+')'
        y += 1
    return content

def write(file_name,file_extension,content):
    file = file_name+file_extension
    with codecs.open(file,'w',encoding='utf8') as text_file:
        text_file.write(content)
    log.info(file + ' created.')

if args.verbose:
    log.basicConfig(format="%(levelname)s: %(message)s", level=log.DEBUG)
    log.info("Verbose output.")
else:
    log.basicConfig(format="%(levelname)s: %(message)s")

try:
    if args.location != '' and os.path.isdir(args.location):
        log.info('File Location ' + args.location + 'exists.')
    else: args.location = './'
except OSError:
    log.error('File Location doesn\'t exist.')
    raise SystemExit

if args.fileformat == 'txt':
    write_txt(args.filename, args.location)
elif args.fileformat == 'rtf':
    write_rtf(args.filename, args.location)
elif args.fileformat == 'md':
    write_md(args.filename, args.location)
