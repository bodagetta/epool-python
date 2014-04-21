epool-python
============

Python script to interface with the <a href="http://www.game-group.com/products/epool/">e-pool wireless pool monitor</a> base station.

I run this script on a <a href="http://www.raspberrypi.org/product/model-b/">Raspberry Pi Model B Board</a> running Raspian OS and the <a href="http://www.newark.com/element14/wipi/module-wifi-usb-for-raspberry/dp/07W8938?CMP=KNC-GPLA">WiPi Dongle</a>

Clone the script to your Raspberry Pi, then edit the port number to match your e-pool reciever (line 122) and server address to match your server (line 112). Then run the script:

```
python epool.py
```


It will show output from the sensor as it is recieved. Note that the local node sends data every few seconds but it might take a few minutes to get data from the pool sensor. Only the pool sensor data is uploaded.

To run in the background, I use screen

Start screen with 

```
screen
```

Then start the script

```
python epool.py
```

Press control + a, then d to detach the screen.

screen -r will resume the session.