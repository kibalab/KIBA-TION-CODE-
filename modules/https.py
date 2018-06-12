#import ftplib
#import time
#import threading
#import shutil
#import os
#server = 'alran.xyz'
#username = 'kibara'
#password = 'kys7song#'
#ftp_connection = ftplib.FTP(server, username, password)
#remote_path = "/"
#ftp_connection.cwd(remote_path)
#def srvhttp(htcode):
#
#    fh = open("./hitomi/"+htcode+".zip", 'rb')
#    ftp_connection.storbinary('STOR '+htcode+".zip", fh)
#    threading.Thread(target=delete, args=[ftp_connection, htcode]).start()
#    fh.close()
#def delete(ftp_connection,htcode):
#    time.sleep(900)#15분 = 900초
#    ftp_connection.delete(htcode+".zip")
#
#for ftpfile in ftp_connection.nlst():
#    if('.zip' in ftpfile ):
#        ftp_connection.delete(ftpfile)