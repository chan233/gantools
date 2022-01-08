#-*- coding:UTF-8 -*-

import os
import hashlib
import gloabl
#filedir = './'+gloabl.g_name
filedir = '/root/Desktop/git/gantools/alphacoders/space'
def filecount(DIR):
    filecount = len([name for name in os.listdir(DIR) if os.path.isfile(os.path.join(DIR, name))])
    return (filecount)
def md5sum(filename):
    f = open(filedir+'/'+filename, 'rb')
    md5 = hashlib.md5()
    while True:
        fb = f.read(8096)
        if not fb:
            break
        md5.update(fb)
    f.close()
    return (md5.hexdigest())


def delfile():
    all_md5 = {}
    dir =os.walk(filedir)
    for i in dir:
        for tlie in i[2]:
            if md5sum(tlie) in all_md5.values():
                os.remove(filedir+'/'+tlie)
                print(tlie)
            else:
                all_md5[tlie] = md5sum(tlie)


if __name__ == '__main__':
#def doprocess():
    oldf = filecount(filedir)
    print('before uniq', oldf, 'files\nplease wait for deleting...')
    delfile()
    print('\n\nafter uniq', filecount(filedir), 'files')
    print('\n\ndelete', oldf - filecount(filedir), 'files\n\n')

