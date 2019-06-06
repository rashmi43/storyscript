# !/usr/local/env python3
"""
Parse the error code to generate mdfiles
"""
import os
import argparse


def matchandcreate(eachline, path_folder):
    """
      Parses each line and generates md file
    """
    splitline = eachline.split('=')
    #err = splitline[0]
    errorline = splitline[1].split(',')
    errcode = errorline[0][2:].strip("\''")
    errmsg = errorline[1][:len(errorline[1])-1]
    md_file = '{}/{}_metadata.md'.format(path_folder, errcode)
    with open(md_file, 'w') as mdf:
        mdf.write('{} {}'.format(errcode, errmsg.strip('\""')))


def main():
    """
      main function reads multiple lines as one line and
      checks for lines matching regex to parse error codes.
      Created a folder mdfiles to generate the md files.
    """
    parser = argparse.ArgumentParser()
    parser.add_argument("error_file", help="Specify the path to the error file")
    args = parser.parse_args()
    path_folder = 'mdfiles'
    if not os.path.exists(path_folder):
        os.mkdir(path_folder)
        print('Directory', path_folder, 'created')
    input_file = args.error_file
    foundstartline = False
    compline = ''
    with open(input_file, 'r') as infile:
        for line in infile:
            if line == '\n':
                continue
            if (line.find('=') > -1) and (line.find(')') > -1):
                line = line.strip()
                line = line.replace(r'\t+|\s+', '')
                matchandcreate(line, path_folder)
            elif line.find('=') > -1:
                foundstartline = True
                compline = compline + line.strip()
            elif (line.find(')') > -1) and foundstartline is True:
                compline = compline + line.strip()
                compline = compline.replace(r'\t+|\s+', '')
                savedline = compline
                compline = ''
                foundstartline = False
                matchandcreate(savedline, path_folder)
            elif foundstartline is True:
                compline += line.strip()
            else:
                continue


if __name__ == '__main__':
    main()
