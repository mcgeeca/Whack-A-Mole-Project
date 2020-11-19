# Updates system
sudo apt-get update
# Installs python 3 and pip
sudo apt-get install build-essential python3-dev python3-pip -y
# Installs Adafruit_BBIO if you don't already have it
sudo pip3 install Adafruit_BBIO
# Install both of these for blynk app 
sudo npm install -g onoff blynk-library
sudo pip3 install blynklib
