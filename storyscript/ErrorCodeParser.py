#!/usr/local/bin/python
#import markdown
import re
import sys
pattern = re.compile('(.*?)\s+\=\s+\((.*)?\)')
def matchAndCreate(l, path_folder):
    matchedObj = re.match(pattern, l)
    group = matchedObj.group(2)
    err = group.split(',')
    errCode = err[0].strip("\''")
    errMsg = err[1].strip("\''")
    md_file = "{}/{}_metadata.md".format(path_folder, errCode)
    with open(md_file, 'w') as mdf:
        #text = markdown.markdown("# "+errCode+errMsg)
        mdf.write('{} {}'.format(errCode, errMsg.strip('\""')))
                                 
def main():
    if not len(sys.argv) == 3:
        print('Please specify the output and input file')
        sys.exit(0)
        
    path_folder = sys.argv[1]
    input_file = sys.argv[2]
    lines = []
    foundStartLine = False
    #pattern = re.compile('(.*?)\s+\=\s+\((.*)?\)')
    compline= ''
    with open(input_file, 'r') as f:
        for line in f:
            if line == '\n':
                continue
            if (( line.find("=")> -1) and (line.find(")") > -1) ):
                line = line.strip()
                line = line.replace("\t+|\s+","")
                #print('line is: '+line)
                if re.match(pattern, line):
                    matchAndCreate(line, path_folder)
                else:
                    print('full line not matches')
            elif (line.find("=")>-1):
                #till you find end brace
                foundStartLine = True
                compline = compline + line.strip()
            elif ( (line.find(')') > -1) and (foundStartLine == True )):
                compline = compline + line.strip()
                compline = compline.replace("\t+|\s+","")
                savedLine = compline
                compline =''
                foundStartLine = False
                if re.match(pattern, savedLine):
                    matchAndCreate(savedLine, path_folder)
                else:
                    print('not matches')
            elif ( foundStartLine == True):
                compline += line.strip()
            else:
                continue
        

if __name__ == "__main__":
    main()


