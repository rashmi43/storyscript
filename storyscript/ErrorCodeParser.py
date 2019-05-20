#!/usr/local/bin/python
import re
import sys
pattern = re.compile('(.*?)\s+\=\s+\((.*)?\)')
def matchandcreate(l, path_folder):
    matchedobj = re.match(pattern, l)
    group = matchedobj.group(2)
    err = group.split(',')
    errcode = err[0].strip("\''")
    errmsg = err[1].strip("\''")
    md_file = "{}/{}_metadata.md".format(path_folder, errcode)
    with open(md_file, 'w') as mdf:
        mdf.write('{} {}'.format(errcode, errmsg.strip('\""')))
                      
def main():
    if not len(sys.argv) == 3:
        print('Please specify the output and input file')
        sys.exit(0)
        
    path_folder = sys.argv[1]
    input_file = sys.argv[2]
    foundstartline = False
    #pattern = re.compile('(.*?)\s+\=\s+\((.*)?\)')
    compline= ''
    with open(input_file, 'r') as f :
        for line in f :
            if line == '\n':
                continue
            if ((line.find('=') > -1) and (line.find(')') > -1)):
                line = line.strip()
                line = line.replace('\t+|\s+','')
                if re.match(pattern, line):
                    matchandcreate(line, path_folder)
                else:
                    print('full line not matches')
            elif (line.find("=")>-1):
                foundstartline = True
                compline = compline + line.strip()
            elif ( (line.find(')') > -1) and (foundstartline == True )):
                compline = compline + line.strip()
                compline = compline.replace('\t+|\s+','')
                savedline = compline
                compline = ''
                foundstartline = False
                if re.match(pattern, savedline):
                    matchandcreate(savedline, path_folder)
                else:
                    print('not matches')
            elif ( foundstartline == True):
                compline += line.strip()
            else:
                continue
        

if __name__ == "__main__":
    main()


