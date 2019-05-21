# !/usr/local/bin/python
import os
import re
PATTERN = re.compile(r'(.*?)\s+\=\s+\((.*)?\)')


def matchandcreate(eachline, path_folder):
    """
      Parses each line and generates md file
    """
    matchedobj = re.match(PATTERN, eachline)
    group = matchedobj.group(2)
    err = group.split(',')
    errcode = err[0].strip("\''")
    errmsg = err[1].strip("\''")
    md_file = '{}/{}_metadata.md'.format(path_folder, errcode)
    with open(md_file, 'w') as mdf:
        mdf.write('{} {}'.format(errcode, errmsg.strip('\""')))


def main():
    """
      main function reads multiple lines as one line and
      checks for lines matching regex to parse error codes.
      Created a folder mdfiles to generate the md files.
    """
    path_folder = 'mdfiles'
    if not os.path.exists(path_folder):
        os.mkdir(path_folder)
        print('Directory ', path_folder, 'created')
    input_file = './storyscript/ErrorCodes.py'
    foundstartline = False
    compline = ''
    with open(input_file, 'r') as file:
        for line in file:
            if line == '\n':
                continue
            if ((line.find('=') > -1) and (line.find(')') > -1)):
                line = line.strip()
                line = line.replace(r'\t+|\s+', '')
                if re.match(PATTERN, line):
                    matchandcreate(line, path_folder)
            elif line.find('=') > -1:
                foundstartline = True
                compline = compline + line.strip()
            elif ((line.find(')') > -1) and foundstartline is True):
                compline = compline + line.strip()
                compline = compline.replace(r'\t+|\s+', '')
                savedline = compline
                compline = ''
                foundstartline = False
                if re.match(PATTERN, savedline):
                    matchandcreate(savedline, path_folder)
            elif foundstartline is True:
                compline += line.strip()
            else:
                continue


if __name__ == '__main__':
    main()
