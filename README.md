**What is this?**

This is the versatile robot platform.


**1. The first usecase is a surveillence robot that is controlled using an android interface:**

The robot will stream the video using [UV4l](http://www.linux-projects.org/uv4l/)

The python server will receive commands using mqtt from the android application, and will transmit battery level and 
distance around the robot.

To access the frontend (android app) access this [repository](https://github.com/danionescu0/android-robot-camera)



**Manual Installation**

You can skip this if you'll run it with docker-compose

* uv4l streamming: https://www.instructables.com/id/Raspberry-Pi-Video-Streaming/?ALLSTEPS
* python packages: ````pip install.sh -r requirements.txt````
* mosquitto 3.1: ````sudo apt-get install.sh mosquitto````


**Configuration**

Clone the project in the home folder:
````
git clone https://github.com/danionescu0/robot-camera-platform
````

Uv4l configuration:

* by editing uv4l/start.sh you can configure the following aspects of the video streaming: password,
port, framerate, with, height, rotation and some other minor aspects

* edit config.py
* replace password with your own password that you've set on the mosquitto server
* optional you can change the baud rate (default 9600) and don't forget to edit that on the arduino-sketch too

**Running project:**
- install docker and docker-compose

````
cd ./docker-container
docker-compose build # once to install
docker-compose up
````


**Uv4l streamming:**

Start image streaming: 
````
chmod +x uv4l/install.sh
sh /uv4l/install.sh # once to install
chmod +x uv4l/start.sh
sh uv4l/start.sh
````
Stop streaming
````
sudo pkill uv4l
````

**Auto starting services on reboot/startup**

1. Copy the files in systemctl folder to /etc/systemd/system/

2. Enable services:
````
sudo systemctl enable robot-camera.service
sudo systemctl enable robot-camera-video.service
````

3. Reboot

4. Optional, check status:
````
sudo systemctl status robot-camera.service
sudo systemctl status robot-camera-video.service
````

**How does it work**

The server listens to movement and light commands from mqtt (android app) and 
forwards them to serial where will be picked up by the listening arduino to 
command the robot.

Also the script listens to serial port for distance updates (front and back) from the 
sensors.

**Why does an intermediary arduino layer has to exist and not directly the Pi ?**

* it's more modular, you can reuse the arduino robot in another project without the PI
* for safety, it's cheaper to replace a 3$ arduino pro mini than to replace a Pi (35$)
* an arduino it's not intrerupted by the operating system like the pi is, so it's more 
efficient to implement PWM controlls for the mottors, polling the front and back sensors
a few times per second
* if an error might occur in the python script the robot might run forever draining the
batteries and probably damaging it or catching fire if not supervised, in an arduino sketch
a safeguard it's more reliable because it does not depends on an operating system

**ToDo**

* Implement a battery status updater, maby my monitoring the power consumption for the py and arduino.
By knowing the full power of the battery pack an power estimation would be possible.
Email alerts and system shutdown should be in place when power is critical.
* Full tutorial on the project with both hardware and software
* Single configuration file for senstive settings like passwords, usernames hosts
* Movement detection with email notification




**2. The second usecase is a object following robot (still in development)**
The robot will follow an object of a specific color (must be unique from background).

In config_navigation.py you'll find:
````
hsv_bounds = (
    (24, 86, 6),
    (77, 255, 255)
)
object_size_threshold = (10, 100)
````

HSV means hue saturation value, and for our color object detection to work it has a lower and
an upper bound, our object color will have to be in this range to be detected.
[Here](https://github.com/jrosebr1/imutils/blob/master/bin/range-detector) you can find a 
visual HSV object threshold detector.

Object size threshold means the smallest and the highest object radius size 
(in percents from width) which will be considered a detection.

Running the object tracking script in vnc graphical interface in a terminal:

```` python3 object_tracking.py --show-video ````

This will enable you to view the video, with a circle drawn over it. The cirle means 
that the object has been detected.

Running the object tracking script with no video output:

```` python3 object_tracking.py ````



** Arduino pro mini pinout **

Led flashlight: D3
Left motor: PWM (D5), EN1, EN2(A4, A5)
Right motor: PWM (D6), EN1, EN2(A3, A2)
Infrared sensors: Front (A0), Back(A1)
Tx: D11, Rx: D10