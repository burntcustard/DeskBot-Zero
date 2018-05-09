The hardware for DeskBot *is not* the main focus of the project. But picking robot parts is fun. Everything was chosen with the following in mind:
* Price - The robot is <£100.
* Simplicity - It's supposed to be a Computer Science, not a robotics final year project! Plus my electronics A-level was a while ago, and it's nice that others can recreate DeskBot without vast technical knowledge.
* Low power - Originally the plan was to charge DeskBot with an inductive charger, and it had to have low enough power consumption to be able to keep the main processor (1GHz ARM11 on the Raspberry Pi) running while recharging. To simplify the project, wireless charging was abandoned, but it maintained its low power consumption.


Most of these pictures are ripped from [Pimoroni](https://pimoroni.com/) - where the majority of the components were purchased from. All images in this parts-list document have been uploaded to [Imgur](https://imgur.com/a/uAWCW) are used under "[fair use](https://fairuse.stanford.edu/overview/fair-use/four-factors/)" for limited educational purposes.



# Parts list


### [Raspberry Pi Zero W](https://www.raspberrypi.org/products/raspberry-pi-zero-w/)
![](http://i.imgur.com/wSj9Y1d.png)

The Pi Zero is "the brain" of the robot. It's a compact way to have some processing power, WiFi and more.


### [Picon Zero](http://4tronix.co.uk/blog/?p=1224)
![](http://i.imgur.com/GbMPGWN.png)

The Picon Zero is a nice add-on for (any) Raspberry Pi. It has a pair of H-Bridge motor drivers to get DeskBot moving, some useful inputs and outputs, and can be powered directly from the Pi.


### [Zumo Chassis](https://www.pololu.com/product/1418)
![](http://i.imgur.com/GKzTTEf.jpg)

Tank tracks are cool. This chassis was originally intended for Arduino-based Mini Sumo robots, but it's a great platform for DeskBot.


### [298:1 Micro Metal Gearmotor (x2)](https://shop.pimoroni.com/products/micro-metal-gearmotor-extended-back-shaft)
![](http://i.imgur.com/1TTihxG.png)

A pair of these slot inside the chassis and only draw ~120mA at full speed. DeskBot isn't super fast, but it has enough torque to get over small desk-based obstacles like mouse mats or drinks coasters.


### [CHJGD® Ultracompact 10,000mAh power bank](https://chargedpower.com/collections/chjgd-ultracompact-range/products/chjgdr-10k-lambo-credit-card-power-bank-1)
![](http://i.imgur.com/pqe64PW.png)

This is one of the few small power banks with *pass through* charging, which is required to keep DeskBot awake while he's recharging. Because of the very low power consumption, and comparitvely large battery size, pass-through is rarely needed, but it's nice to have.


### [Camera Module for Raspberry Pi Zero](https://shop.pimoroni.com/products/raspberry-pi-zero-camera-module)
![](https://i.imgur.com/kA7bhwb.jpg)

This camera was chosen for its tiny size, low cost, and simple interface with the Raspberry Pi Zero.


### [Adafruit Mini Pan-Tilt Kit](https://shop.pimoroni.com/products/adafruit-mini-pan-tilt-kit-assembled-with-micro-servos)
![](https://i.imgur.com/0jOfc0U.jpg)

The pan-tilt kit (*with* Micro Servos, *without* the Pan-Tilt HAT) holds the "sensor array", as well as the Picon Zero and Raspberry Pi at the top of the robot. Those electronic parts were mounted on the moving platform to reduce the number of wires between the static body and moving sensors.


### [HC-SR04 Ultrasonic Sensor](https://www.electroschematics.com/8902/hc-sr04-datasheet/)
![](https://i.imgur.com/ohhPbAU.jpg)

This sensor was originally planned to be the only one required besides the camera. However, due to it's limited range of reliable surface detection, it was later repurposed to only be used for distance-to-wall sensing, and the infrared distance sensor was added for desk-edge detection.


### [Sharp GP2YA21YK0F Infrared Distance Sensor](http://www.sharp-world.com/products/device/lineup/data/pdf/datasheet/gp2y0a21yk_e.pdf)
![](https://i.imgur.com/o66f2kl.png)

As previously mentioned, the ultrasonic sensor had issues sensing the desk edge, so this distance measuring sensor unit was added. Ideally, this sensor would be used to measure distance directly, however due to the nature of the non-linear (and relatively undocumented) analog output, along with the varying reflectivity of the surfaces and angles measured to, some mathematical code had to be added to determine distance not from the output voltage, but instead from the angles between this sensor sending a low output (no desk in view), to a higher output (sensor pointing downwards at desk).


### Miscellaneous

Additional minor components were used, like solid core wires, [jumper jerky](https://shop.pimoroni.com/products/jumper-jerky), a memory card for the Pi, and copious amounts of Blu Tack to keep wires in place and angle the camera downwards.
