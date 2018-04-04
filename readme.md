# SFUSat Houston

Named after the coloquial term for the Apollo missions' control centre, Houston is SFUSat's control centre. 

It is a serial monitor, command schedule creator, command uploader, and telemetry verifier. 

![screenshot](screenshot.png?raw=true "Screenshot of early version")

## Installation
1. run `sudo pip3 install virtualenvwrapper`
2. run `nano ~/.bashrc`
3. At the bottom of your .bashrc file, paste the following lines with ctrl + shift + v

`export WORKON_HOME=$HOME/.virtualenvs`

`export PROJECT_HOME=$HOME/Devel`

`source /usr/local/bin/virtualenvwrapper.sh`

4. exit nano with `ctrl + x`, `y` to save the file
5. cd houston
6. `mkvirtualenv sfusat-gcs` (you can name it whatever you want)
7. You should now be in the virtualenv, indicated by `(sfusat-gcs)` before your command prompt
7. `pip3 install -r reqs.txt`

## Installation Notes:

- These steps haven't been thouroughly tested. You might need to jump through some hoops to install Kivy on your system.

## Usage:
1. cd into the repo
2. `workon sfusat-gcs` to enter the virtualenv
3. `python houston.py` to start the app. Serial will automatically connect if the device path is right (see next section).

## Usage notes:

- You will likely need to change the path to the OBC's FTDI usbserial convertor. This is `serialPort` at the top of houston.py.