# Shared Fail2Ban

This is a variation of [GitHub - bulgemonkey/Shared-Fail2Ban](https://github.com/bulgemonkey/Shared-Fail2Ban)

### The notes for their original project are

This project aims to enable [Fail2Ban](https://www.fail2ban.org/) instances on individual systems to push the ban information of each 
jail to a central database allowing other systems to pull the bans to 
their own system.

**Example:** This would then mean if Alice and Bob both share their bans and Charlie 
was locked out from Alice's system for too many incorrect details, 
Charlie would then be banned from Bob's system.

Fail2Ban Filters can still be applied meaning the sharing method is as robust as a standard Fail2Ban deployment.

We welcome any Issues and PRs.

## Project Credits

The authors of this project are currently **[Adam Boutcher](https://www.aboutcher.co.uk)** and **Paul Clark**.

This has been developed at the Durham [GridPP](https://gridpp.ac.uk) Site (*UKI-SCOTGRID-DURHAM*) and the [Institute for Particle Physics Phenomenology](https://www.ippp.dur.ac.uk), [Durham University](https://dur.ac.uk).

The work and partial works have been presented too the [WLCG](https://wlcg.web.cern.ch/) Security Operations Centre at [Cern](https://home.cern/)



----

## Guide

This is a very brief installation method/guide; please read the Warnings and Notices below

### Fail2Ban Host/Client

1. Install Fail2Ban
2. Create the f2b database
3. Choose and setup deployment type (Direct MySQL/MariaDB or API)
4. Deploy the Fail2Ban actions and scripts
5. Configure deployment type
6. Setup the Jails
7. Setup the Cron
8. Start Fail2Ban

### Database (MySQL/MariaDB) Only

1. Run the database scripts
2. Create a db user for each Fail2Ban Host/Client with CREATE and INSERT permissions.
3. Start mysql/mariadb

### API with Database (MySQL/MariaDB)

1. Run the database scripts
2. Create a db user for the API to use with CREATE and INSERT permissions.
3. Run the API insatllation script
4. Make the db changes required
5. Start mysql/mariadb
6. Start httpd/apache

----

## Warnings and Notices

### Warning - Not for Production

The files contained in this repository are currently primarily to use and develop from. They should be READ and UNDERSTOOD rather than blindly copied and deployed.

In no way do we endorse the current scripts as production ready (although they are currently deployed in some producation environments), we cannot gurantee their safety, especially as these are aimed for Cyber Security deployments.

### Notice - CentOS

The development for this project has been on CentOS Linux 7 although some efforts have been made to enable them to run on CentOS Linux 8. Other distros may have unexpected results.

#### SELinux

SELinux may break this, we wrote some modules for our environment but they have not been include in this project yet.

- Fail2Ban Client - setsebool -P nis_enabled 1
- Fail2Ban API - setsebool -P httpd_can_network_connect_db

### Warning - IPv6

Fail2Ban didn't support IPv6 at the time of initial development. The current state of this project is that IPv6 is completely untested and will probably not work correctly.

### Notice - Python Support

The version of Fail2Ban we targeted was written in Python2 and shipped with its own python binary, some scripts will run with Python2 and Python3, some are only Python2. Your experences may vary.

(end of original readme)

# The differances in this fork

I am using the project more or less as supplied by Durham but with a few local changes mainly code changes/different install mechanism/file name changes.

Ive added additional jails, the project , as was, handled a jail specifically for ssh. Ive added an extra jail for apache-no-script to show how to add extra jails.

Modified the 'get.py' mechanism and name of the produced filter.log file which is now
filter-NAMEOFJAIL.log

get.py called with no arguments will query ssh, or pass it an argument --jail thing and it will ask for jail called 'thing' and produce logfile filter-thing.log

The original installer mechanism used shell scripts and some of the config files were embedded within those scripts. I have chosen to have separate files and do the installation configuration using ansible.

Added web page to show current bans.

Durhams original code is in here and the customised variation is in

```
/Shared-Fail2Ban/jtf2binstallers
```

There are two installer scripts..one for client, one for the database server.

These are minimal and just copy files to the relevant destinations. Ansible could have done this but I wanted to keep code files and installer config mechanism separate.

An Ansible script does overwrite some of the content,
The associated Ansible scripts are at

[GitHub - ninelocks/ansible-shared-fail2ban](https://github.com/ninelocks/ansible-shared-fail2ban)

Here is what is in the installer folder Shared-Fail2Ban/jtinstallers

Shared-Fail2Ban/jtinstallers

├── client\

│ ├── get.py\

│ ├── input.py\

│ ├── shared_cfg.py\

│ ├── shared-f2b-filter.conf\

│ ├── shared-f2b-input.conf\

│ └── testsending.sh\

├── extras

│ ├── base-server.sql\

│ └── fail2ban-shared\

├── f2bweb\

│ └── index.php\

├── gu_sf2b_client_installer.sh\

├── gu_sf2b_server_installer.sh\

├── server\

│ ├── api_cfg.py\

│ ├── api.py\

│ ├── api.wsgi\

│ ├── api.wsgi.tpl\

│ └── forwebserver\

│ └── api.conf\

└── WhatFilesGoWhere\

 
