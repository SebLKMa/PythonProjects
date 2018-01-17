https://github.com/certsocietegenerale/FIR/wiki/Installation-on-a-production-environment

01. Install the prerequisites for running FIR with MySQL and nginx:
$ sudo apt-get update
$ sudo apt-get install mysql-server libmysqlclient-dev gettext python-dev python-pip python-lxml git libxml2-dev libxslt1-dev libz-dev nginx

mysql root password "sebtno"

02. Configure MySQL database
Create users:
$ mysql -uroot -p
> CREATE DATABASE fir;
> CREATE USER 'fir'@'localhost' IDENTIFIED BY 'firtno';
> GRANT USAGE ON *.* TO 'fir'@'localhost';
> GRANT ALL PRIVILEGES ON `fir`.* TO 'fir'@'localhost';
> exit
and test mysql login
$ mysql -ufir -pfirtno


03. Install FIR
If you want to use a virtual environment, follow these steps:

04.Switch to virtualenv if you wish.
Since this VM is strictly for FOR PROD, we do not need to have virtualenv.
#$ sudo pip install virtualenv
#$ virtualenv env-FIR
#$ source env-FIR/bin/activate

05. Clone the GitHub repo:
$ git clone https://github.com/certsocietegenerale/FIR.git
cd into the FIR directory and install Python dependencies:

$ cd FIR
$ sudo pip install -r requirements.txt       # Install dependencies
$ sudo pip install mysql-python

06. Create a production configuration file by copying the fir/config/production.py.sample to fir/config/production.py
$ cp fir/config/production.py.sample fir/config/production.py

07. Change the settings in the production.py file according to your setup. 
This includes the ALLOWED_HOSTS directive - change it to whatever vhost you're planning to use in your deployment. 
Also, remember to change the timezone(http://en.wikipedia.org/wiki/List_of_tz_zones_by_name) in base.py (Asia/Singapore)

A virtual host will provide its customers with domain name registration, 
file storage and directory services for the files that Web page is built from, 
e-mail services and even Web site design and creation services if the customers 
want someone else to build their Web sites.

#ALLOWED_HOSTS = ['FIR.DOMAIN.COM'] to be from web hosting one.com later
#For local VM using NAT, just use the IP from ifconfig
ALLOWED_HOSTS = ['127.0.0.1','localhost', '192.168.9.132']

DATABASES = {
    'default': {
        'ENGINE': 'django.db.backends.mysql',
        'NAME': 'fir',
        'USER': 'fir',
        'PASSWORD': 'firtno',
        'HOST': '',
        'PORT': '',
    }
}

# SECRET KEY
SECRET_KEY = 'sebtno'

08. Enable the plugins, copy the fir/config/installed_apps.txt.sample file to fir/config/installed_apps.txt:
$ cp fir/config/installed_apps.txt.sample fir/config/installed_apps.txt

09. Create the tables in the database:
./manage.py migrate --settings fir.config.production

10. Create a superuser:
$ ./manage.py createsuperuser --settings fir.config.production
Username (leave blank to use 'sebtno'):       
Email address: sebastian.ma@tno.nl 
Password: 
Password (again): 
Superuser created successfully.

11. Import initial data (you can change these later from the Django backend):
$ ./manage.py loaddata incidents/fixtures/seed_data.json --settings fir.config.production

12. Collect static files (these will be cached for better performance)
$ ./manage.py collectstatic --settings fir.config.production 

13. Change some permissions in order for the www-data to be able to access log files and write to the uploads directory:
$ sudo chown www-data logs/errors.log uploads
$ sudo chmod 750 logs/errors.log uploads

14. We need to install uWSGI in order to serve our application:
$ sudo pip install uwsgi

15. Change www-data's shell to /bin/sh:
$ sudo chsh www-data
Changing the login shell for www-data
Enter the new value, or press ENTER for the default
	Login Shell [/usr/sbin/nologin]: /bin/sh

16. Create a file in /etc/init/fir.conf with the following contents 
(Note your FIR install directory /home/sebtno/app/FIR)
(If using virtualenv, the "exec" line must be adjusted if you're using a Python virtual environment.):

description "FIR - Django uWSGI"

start on runlevel [2345]
stop on runlevel [!2345]

setuid www-data
setgid www-data

respawn

exec uwsgi --socket /home/sebtno/app/FIR/run/fir.sock --chdir /home/sebtno/app/FIR/ --module fir.wsgi

17. This section does NOT work!
To start the daemon, run 
sudo start fir 
To restart it, run 
sudo restart fir 
To stop it, 
sudo stop fir 

18. If you're using systemd, the following script in /etc/systemd/system/fir_uwsgi.service should work:

[Unit]
Description=uWSGI instance for FIR
After=syslog.target

[Service]
User=www-data
Group=www-data
WorkingDirectory=/home/sebtno/app/FIR/
ExecStart=/usr/local/bin/uwsgi --socket /home/sebtno/app/FIR/run/fir.sock --chdir /home/sebtno/app/FIR/ --module fir.wsgi
Restart=always
KillSignal=SIGQUIT
Type=Debug
StandardError=syslog
NotifyAccess=All

[Install]
WantedBy=multi-user.target

18a. Then run:
$ sudo service fir_uwsgi start
tno
19. nginx for load balancing

Download uwsgi params:
$ wget https://raw.githubusercontent.com/nginx/nginx/master/conf/uwsgi_params -P run
Remove the default configuration file:

$ sudo rm /etc/nginx/sites-enabled/default
Create a /etc/nginx/sites-available/fir file with the following contents:

upstream fir {
	server unix:///home/sebtno/app/FIR/run/fir.sock;
}

server {
	server_name 192.168.9.132;

	location / {
		uwsgi_pass fir;
		include /home/sebtno/app/FIR/run/uwsgi_params;
	}

	location /static/ {
		alias /home/sebtno/app/FIR/static/;
	}
}

Make sure you replace FIR.DOMAIN.COM with the host you will be using to host your FIR install. This should match what you specified in the ALLOWED_HOSTS directive in production.py. (This solves error 400 problems as described in https://github.com/certsocietegenerale/FIR/issues/46)
See also:
https://github.com/certsocietegenerale/FIR/issues/188

20. Enable the configuration:

$ sudo ln -s /etc/nginx/sites-available/fir /etc/nginx/sites-enabled/fir
$ sudo service nginx reload

open http://127.0.0.1/admin
admin login: sebtno/sebtno

tail -f /var/log/syslog

sebtno@ubuntu:~/app/FIR$ sudo service fir_uwsgi status
? fir_uwsgi.service - uWSGI instance for FIR
   Loaded: loaded (/etc/systemd/system/fir_uwsgi.service; disabled; vendor preset: enabled)
   Active: active (running) since Tue 2018-01-16 01:23:50 PST; 5min ago
 Main PID: 11110 (uwsgi)
   CGroup: /system.slice/fir_uwsgi.service
           +-11110 /usr/local/bin/uwsgi --socket /home/sebtno/app/FIR/run/fir.sock --chdir /home/sebtno/app/FIR/ --plugins python --module fir.wsgi

Jan 16 01:23:50 ubuntu uwsgi[11110]: Python main interpreter initialized at 0x15adcb0
Jan 16 01:23:50 ubuntu uwsgi[11110]: your server socket listen backlog is limited to 100 connections
Jan 16 01:23:50 ubuntu uwsgi[11110]: your mercy for graceful operations on workers is 60 seconds
Jan 16 01:23:50 ubuntu uwsgi[11110]: mapped 72760 bytes (71 KB) for 1 cores
Jan 16 01:23:50 ubuntu uwsgi[11110]: *** Operational MODE: single process ***
Jan 16 01:23:51 ubuntu uwsgi[11110]: WSGI app 0 (mountpoint='') ready in 1 seconds on interpreter 0x15adcb0 pid: 11110 (default app)
Jan 16 01:23:51 ubuntu uwsgi[11110]: *** uWSGI is running in multiple interpreter mode ***
Jan 16 01:23:51 ubuntu uwsgi[11110]: spawned uWSGI worker 1 (and the only) (pid: 11110, cores: 1)
Jan 16 01:24:05 ubuntu systemd[1]: [/etc/systemd/system/fir_uwsgi.service:12] Failed to parse service type, ignoring: Debug
Jan 16 01:24:05 ubuntu systemd[1]: [/etc/systemd/system/fir_uwsgi.service:14] Failed to parse notify access specifier, ignoring: All
sebtno@ubuntu:~/app/FIR$ sudo service fir_uwsgi stop
sebtno@ubuntu:~/app/FIR$ sudo service fir_uwsgi start
sebtno@ubuntu:~/app/FIR$ sudo service fir_uwsgi status
? fir_uwsgi.service - uWSGI instance for FIR
   Loaded: loaded (/etc/systemd/system/fir_uwsgi.service; disabled; vendor preset: enabled)
   Active: active (running) since Tue 2018-01-16 01:30:15 PST; 1min 54s ago
 Main PID: 11275 (uwsgi)
   CGroup: /system.slice/fir_uwsgi.service
           +-11275 /usr/local/bin/uwsgi --socket /home/sebtno/app/FIR/run/fir.sock --chdir /home/sebtno/app/FIR/ --module fir.wsgi

Jan 16 01:30:15 ubuntu uwsgi[11275]: Python main interpreter initialized at 0x10bcba0
Jan 16 01:30:15 ubuntu uwsgi[11275]: your server socket listen backlog is limited to 100 connections
Jan 16 01:30:15 ubuntu uwsgi[11275]: your mercy for graceful operations on workers is 60 seconds
Jan 16 01:30:15 ubuntu uwsgi[11275]: mapped 72760 bytes (71 KB) for 1 cores
Jan 16 01:30:15 ubuntu uwsgi[11275]: *** Operational MODE: single process ***
Jan 16 01:30:15 ubuntu uwsgi[11275]: WSGI app 0 (mountpoint='') ready in 0 seconds on interpreter 0x10bcba0 pid: 11275 (default app)
Jan 16 01:30:15 ubuntu uwsgi[11275]: *** uWSGI is running in multiple interpreter mode ***
Jan 16 01:30:15 ubuntu uwsgi[11275]: spawned uWSGI worker 1 (and the only) (pid: 11275, cores: 1)
Jan 16 01:31:41 ubuntu uwsgi[11275]: [pid: 11275|app: 0|req: 1/1] 192.168.9.132 () {40 vars in 625 bytes} [Tue Jan 16 17:31:41 2018] GET /admin => generate
Jan 16 01:31:53 ubuntu uwsgi[11275]: [pid: 11275|app: 0|req: 2/2] 127.0.0.1 () {40 vars in 617 bytes} [Tue Jan 16 17:31:53 2018] GET /admin => generate


WHEN YOUR VM STARTS WITH BLANK SCREEN
1. Ctrl+Alt+F1 to enter console mode
2. Login
3. sudo apt-get upgrade
4. sudo restart now or sudo shutdown now






