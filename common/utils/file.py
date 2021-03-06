import os
from os import listdir, remove, rmdir
from os.path import isdir, islink
import ftplib

DIR_EXCLUDES = ('.', '..')

def deltree(topdir):
    """
    force to delete whole directory tree.
    """
    try:
        dirs = listdir(topdir)
    except OSError:
        return
    
    for dir in dirs:
        if dir in DIR_EXCLUDES:
            continue
        fpath = os.path.join(topdir, dir)
        if islink(fpath) or not isdir(fpath):
            try:
                if not os.access(fpath, os.W_OK):
                    os.chmod(fpath, 0777)
                remove(fpath)
            except OSError:
                pass
        else:
            deltree(fpath)
    try:
        rmdir(topdir)
    except OSError:
        pass

def getfile(name):
    if name.startswith("ftp://"):
        return getftpfile(name)
    return open(name)

def getftpfile(url):
    from ftplib import FTP
    import re
    import tempfile
    import os
    
    patterns = ['^ftp://(?P<user>[\w]+):(?P<password>[\w]+)@(?P<host>[\w\-\.]+):(?P<port>[\d]+)/(?P<path>.+)$',
                '^ftp://(?P<user>[\w]+):(?P<password>[\w]+)@(?P<host>[\w\-\.]+)/(?P<path>.+)$',
                '^ftp://(?P<host>[\w\-\.]+):(?P<port>[\d]+)/(?P<path>.+)$',
                '^ftp://(?P<host>[\w\-\.]+)/(?P<path>.+)$']
    for expr in patterns:
        m = re.match(expr, url, re.IGNORECASE)
        if m:
            d = m.groupdict()
            host = d.get('host')
            path = d.get('path')
            user = d.get('user')
            passwd = d.get('password')
            port = d.get('port')
            break
    if m:
        try:
            if port and port != 21:
                ftp = FTP()
                ftp.connect(host, int(port))
                if user:
                    ftp.login(user, passwd)
                else:
                    ftp.login()
            else:
                ftp = FTP(host, user, passwd)
            file = tempfile.TemporaryFile(suffix=os.path.basename(path))
            ftp.cwd(os.path.dirname(path))
            ftp.retrbinary('RETR ' + os.path.basename(path), file.write)
            file.flush()
            file.seek(0)
            ftp.close()
            return file
        except ftplib.all_errors, e:
            raise Exception("FTP: %s" % str(e))
            
    raise None
