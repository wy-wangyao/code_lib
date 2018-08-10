"""
网站重定向,将原站点所有页面替换为转向转向链接文件
"""

import os
import configparser

config = configparser.ConfigParser()
config.read('redirect_web.conf')

servername = config.get('web', 'servername')
homedir = config.get('web', 'homedir')
sitefiledir = config.get('web', 'sitefiledir')
uploaddir = config.get('web', 'uploaddir')
templatename = config.get('web', 'templatename')

try:
    os.mkdir(uploaddir)
except OSError:
    pass

template = open(templatename).read()
sitefiles = os.listdir(sitefiledir)
count = 0

for filename in sitefiles:
    if filename.endswith('.html') or filename.endswith('.htm'):
        fwdname = os.path.join(uploaddir, filename)
        print('creating', filename, 'as', fwdname)
        filetext = template.replace('$server$', servername)
        filetext = filetext.replace('$home$', homedir)
        filetext = filetext.replace('$file$', filename)
        with open(fwdname, 'w') as f:
            f.write(filetext)
        count += 1

print('last file =>\n', filetext, sep='')
print('Done:', count, 'forword files created.')
