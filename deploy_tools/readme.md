Provisioning a new site
=======================

## Required packages:
	* nginx
	* Python 3.6
	* virtualenv + pip
	* Git

eg, on Ubuntu:
	sudo add-apt-repository ppa:fkrull/deadsnakes
	sudo apt-get install nginx git python36 python3.6-venv

## Nginx Virtual Host config
	* see nginx.template.conf
	* replace SITENAME with, e.g., staging.my-domain.com

## Systemd service
	* see gunicorn-systemd.template.service
	* replace SITENAME with, e.g., staging.my-domain.com

## Folder structure:

/var/www
&emsp;&emsp;&emsp;└── SITENAME
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; ├── database
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; ├── source
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; ├── static
&emsp;&emsp;&emsp;&emsp;&emsp;&emsp;&emsp; └── virtualenv
/var/www
├── SITENAME
│   ├── database
│   ├── source
│   ├── static
│   └── virtualenv

