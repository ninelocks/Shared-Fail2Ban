#!/bin/bash
#jon.trinder@glasgow.ac.uk
#jont@ninelocks.com
# 22/01/2021
#set -x #echo on
#installer for our variant of Durhams fail2ban project
#this for the client side
#
# these just get copied as is
# /etc/fail2ban/filter.d/shared-f2b-filter.conf
# /etc/fail2ban/action.d/shared-f2b-input.conf
# /etc/fail2ban/action.d/fail2ban/shared-f2b/get.py
# /etc/fail2ban/action.d/fail2ban/shared-f2b/input.py
#
# this is the config file , in Glasgow will be overwrttien by ansible
# /etc/fail2ban/action.d/fail2ban/shared-f2b/shared_cfg.py



if [ ! -d "/etc/fail2ban" ]; then
    echo "You need to install fail2ban on this system first :-)"
    exit 1
fi


if [ ! -d "/etc/fail2ban/action.d/shared-f2b" ]; then
    mkdir /etc/fail2ban/action.d/shared-f2b
fi

echo "copying main files across to fail2ban"
cp ./client/shared-f2b-filter.conf /etc/fail2ban/filter.d/shared-f2b-filter.conf
cp ./client/shared-f2b-input.conf  /etc/fail2ban/action.d/shared-f2b-input.conf
cp ./client/get.py                 /etc/fail2ban/action.d/shared-f2b/get.py
cp ./client/input.py               /etc/fail2ban/action.d/shared-f2b/input.py


#touch /etc/fail2ban/action.d/shared-f2b/filter.log


#
echo "copying config files across to fail2ban"
cp ./client/shared_cfg.py /etc/fail2ban/action.d/shared-f2b/shared_cfg.py
echo "If we got here things looking good"
 
