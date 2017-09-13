The hardware for the DeskBot *will not* be the main focus of the project. But it's always fun picking robot parts. Everything was chosen with the following in mind:
* Price - The robot should be <£100. Mainly because I'm a poor uni student.
* Simplicity - It's supposed to be a Computer Science, not a robotics final year project! Plus my electronics A-level was a while ago, and it'd be nice if othere's could recreate DeskBot without vast technical knowledge.
* Low power - The plan is to recharge DeskBot with a Qi inductive charging station. I.e. very slowly. Everything combined must have low enough energy consumption to stay on, while also being wirelessly charged.


Most of these pictures are ripped from https://pimoroni.com/. I imagine they won't mind, as it's where I got most of the components from... and this is free advertising :wink:


Here's the *work in progress* list of bits, and some reasoning as to why they've been chosen:


### [Raspberry Pi Zero W](https://www.raspberrypi.org/products/raspberry-pi-zero-w/)
![](http://i.imgur.com/wSj9Y1d.png)

The Pi Zero is "the brain" of the robot. It's a compact way to have some processing power, WiFi and Bluetooth connectivity, and more.


### [Picon Zero](http://4tronix.co.uk/blog/?p=1224)
![](http://i.imgur.com/GbMPGWN.png)

The Picon Zero is a nice add-on for (any) Raspberry Pi. It has a pair of H-Bridge motor drivers to get DeskBot moving, some useful inputs and outputs, and can be powered directly from the Pi.


### [Zumo Chassis](https://www.pololu.com/product/1418)
![](http://i.imgur.com/GKzTTEf.jpg)

Tank tracks are cool. The Zumo chassis was originally intended for Arduino based Mini Sumo robots, but it'll make a good base for DeskBot.

### 298:1 Micro Metal Gearmotor (x2)
![](http://i.imgur.com/1TTihxG.png)

A pair of these will slot inside the chassis and only draw ~120mA at full speed. DeskBot won't be super fast, but it'll have enough torque to get over small desk-based obstacles like mouse mats or drinks coasters.

### [CHJGD® Ultracompact 10,000mAh power bank](https://chargedpower.com/collections/chjgd-ultracompact-range/products/chjgdr-10k-lambo-credit-card-power-bank-1)
![](http://i.imgur.com/pqe64PW.png)

This is one of the few small power banks with *pass through* charging, which is required to keep DeskBot awake while he's recharging.


## To document still:
* Camera
* Microphone(?)
* Speaker(?)
* Ultrasonic distance sensor
* Memory card
* Qi charging pad & reciever
* Misc components (wires, pin headers, LEDs, etc.)
