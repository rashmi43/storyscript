# !/usr/local/env python3
"""
Parse the error code to generate mdfiles
"""
import os
from storyscript.ErrorCodes import ErrorCodes


def main():
    """
      main function reads multiple lines as one line and
      checks for lines matching regex to parse error codes.
      Created a folder mdfiles to generate the md files.
    """
    path_folder = 'mdfiles'
    if not os.path.exists(path_folder):
        os.mkdir(path_folder)
        print('Directory', path_folder, 'created')
    ec = ErrorCodes()
    members = [attr for attr in dir(ec) if not
               callable(getattr(ec, attr)) and not attr.startswith("__")]
    for error in members:
        err = ec.get_error(error)
        errcode = err[0]
        errmsg = err[1]
        md_file = '{}/{}_metadata.md'.format(path_folder, errcode)
        with open(md_file, 'w') as mdf:
            mdf.write('{} - {}'.format(errcode, errmsg))

if __name__ == '__main__':
    main()
