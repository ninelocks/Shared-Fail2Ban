#!/usr/bin/fail2ban-python
# Shared Fail2Ban
<<<<<<< HEAD
# This is the script that pulls Banned IPs in a given JailName and output it to a file.
=======
# modified Feb 2021 Jon Trinder to add command line arg
# as of 01/02/2021 I hadnt tested the 'mysql' route through here so may have broken the query
# Paul Clark, Adam Boutcher
>>>>>>> moondawn
# github.com/bulgemonkey/Shared-Fail2Ban/
#
# Paul Clark    - 2018, IPPP, Durham University
#  Initial Database work
# Adam Boutcher - 2020, IPPP, Durham University
#  Inital API work
# Jon Trinder   - 2021, Glasgow University
#  Added arguments to support multiple jailnames (MySQL Untested), default to ssh to keep compatability.


import sys
import json
import argparse
<<<<<<< HEAD
import shared_cfg as cfg

=======

import shared_cfg as cfg


>>>>>>> moondawn
def getjails(jailname):

    if 'mysql' in cfg.source:
        import mysql.connector
        import socket
        db = mysql.connector.connect(
            host=cfg.mysql["host"], user=cfg.mysql["user"], passwd=cfg.mysql["passwd"], db=cfg.mysql["db"])
        cur = db.cursor(dictionary=True)
        host = socket.gethostname()
        sql = "SELECT UNIX_TIMESTAMP(created) as created, ip, port, protocol FROM f2b WHERE created>=DATE_ADD(NOW(), INTERVAL -1 HOUR) AND jail = '%s' AND hostname != '%s'" % (jailname, host)
        cur.execute(sql)
        data = cur.fetchall()
    else:
<<<<<<< HEAD
        if (sys.version_info > (3, 0)):
            # Python 3 code in this block
            import urllib.request
            response = urllib.request.urlopen(cfg.apiurl+"/time/"+jailname+"/1")
        else:
            # Python 2 code in this block
            import urllib
            response = urllib.urlopen(cfg.apiurl+"/time/"+jailname+"/1")
        data = json.loads(response.read())
    logfilename = "/etc/fail2ban/action.d/shared-f2b/filter-"+jailname+".log"
=======
        queryline = cfg.apiurl + "/time/" + jailname + "/1"
        if (sys.version_info > (3, 0)):
            # Python 3 code in this block
            import urllib.request
            #response = urllib.request.urlopen(cfg.apiurl+"/time/ssh/1")
            response = urllib.request.urlopen(queryline)
        else:
            # Python 2 code in this block
            import urllib
            #response = urllib.urlopen(cfg.apiurl+"/time/ssh/1")
            response = urllib.urlopen(queryline)
        data = json.loads(response.read())
    logfilename = "/etc/fail2ban/action.d/shared-f2b/filter-" + jailname + ".log"
>>>>>>> moondawn

    open(logfilename, "w").close()
    file = open(logfilename, "w")
    for result in data:
        file.write(str(result['created'])+" ["+str(result['ip'])+"] " +
                   str(result['port'])+" "+str(result['protocol'])+"\n")
    file.close()


if __name__ == '__main__':

<<<<<<< HEAD
    parser = argparse.ArgumentParser()
    parser.add_argument('--jail', required=False, help='Enter jailname', dest='jail_name', default="ssh")
    results = parser.parse_args()
    getjails(results.jail_name)
=======
    """
    jjt added args parse so I can pass in jailname    
    """
    parser = argparse.ArgumentParser()
    parser.add_argument('--jail', required=False,
                        help='Enter jailname', dest='jail_name', default="ssh")

    results = parser.parse_args()
    getjails(results.jail_name)
    #print(results.jail_name)   #left around for debugging to save me eretyping
>>>>>>> moondawn
