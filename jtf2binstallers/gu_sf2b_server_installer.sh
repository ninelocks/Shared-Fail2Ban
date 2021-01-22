#!/bin/bash
#jon.trinder@glasgow.ac.uk
#jont@ninelocks.com
# 22/01/2021
#set -x #echo on
#installer for our variant of Durhams fail2ban project

#dest files assuming we going to /opt/f2bapi
# these need customisation and were original inside durhams install script
# here I will copy over raw files as placeholder but in reality will overwrite from ansible
# api.wsgi
# api-cfg.py

##################################
# this is for httpd/apache config
##################################
# /etc/httpd/conf.d/api.conf
# so will depend on being apache or httpd and I will do via ansible
#

# suss which webserver (durhams code)
# code from durham installer :-)
# if we cant find webserver may as well go home/pub

if [ -d "/etc/httpd" ]; then
  aloc="/etc/httpd"
elif [ -d "/etc/apache2" ]; then
  aloc="/etc/apache2"
else
  echo "Unknown Apache Location"
  exit 1
fi

# these need customisation and were original inside durhams install script
# here I will copy over raw files as placeholder but in reality will overwrite from ansible

  
if [ ! -d "/opt/f2bapi" ]; then
  echo "create folder /opt/f2bapi"
  mkdir /opt/f2bapi/
fi
if [ ! -d "/opt/f2bapi" ]; then
  echo "could not create folder"
  exit 1
fi

echo "copy files across"
cp ./server/api.wsgi /opt/f2bapi/api.wsgi
cp ./server/api-cfg.py /opt/f2bapi/api-cfg.py

#this just needs copied
# api.py
cp ./server/api.py /opt/f2bapi

#finally the web server conf
cp ./server/forwebserver/api.conf $aloc/conf.d/api.conf

echo "if we got here all good, go run your ansible script"