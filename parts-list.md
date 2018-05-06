The hardware for the DeskBot *will not* be the main focus of the project. But it's always fun picking robot parts. Everything was chosen with the following in mind:
* Price - The robot should be <£100. Mainly because I'm a poor uni student.
* Simplicity - It's supposed to be a Computer Science, not a robotics final year project! Plus my electronics A-level was a while ago, and it'd be nice if othere's could recreate DeskBot without vast technical knowledge.
* Low power - Originally the plan was to recharge DeskBot with an inductive charging station, so it had to have low enough power consumption to be able to keep the processor (1GHz ARM11 on the Raspberry Pi) running while recharging. To keep the project simple, wireless charging was abandoned, but it maintained the low power consumption specification.


Most of these pictures are ripped from https://pimoroni.com/ - where the majority of the components were purchased from. All images in this parts-list document have been uploaded to [Imgur](https://imgur.com/a/uAWCW) are used under ["fair use" guidelines](https://fairuse.stanford.edu/overview/fair-use/four-factors/) for certain limited educational purposes.



# Parts list


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

This is one of the few small power banks with *pass through* charging, which is required to keep DeskBot awake while he's recharging. Because of the very low power consumption, and comparitvely large battery size, pass-through is rarely needed, but it's nice to have.


### [Camera Module for Raspberry Pi Zero](https://shop.pimoroni.com/products/raspberry-pi-zero-camera-module)
![](https://i.imgur.com/kA7bhwb.jpg)

This camera was chosen for its tiny size, low cost, and simple interface with the Raspberry Pi Zero.


### [Adafruit Mini Pan-Tilt Kit](https://shop.pimoroni.com/products/adafruit-mini-pan-tilt-kit-assembled-with-micro-servos)
![](https://i.imgur.com/0jOfc0U.jpg)

The pan-tilt kit (*with* Micro Servos, *without* the Pan-Tilt HAT) holds all of the "sensor array", as well as the Picon Zero and Raspberry Pi at the top of the robot. Those electronic parts were mounted on the moving platform to reduce the number of wires between the static body and moving sensors.


### HC-SR04 Ultrasonic Sensor
![](https://i.imgur.com/ohhPbAU.jpg)

This sensor was originally planned to be the only one required besides the camera. However, due to it's limited range of reliable surface detection, it was later repurposed to only be used for distance-to-wall sensing, and the infrared distance sensor was added to be used for desk-edge detection.


### [Sharp GP2YA21YK0F Infrared Distance Sensor](http://www.sharp-world.com/products/device/lineup/data/pdf/datasheet/gp2y0a21yk_e.pdf)
![](https://i.imgur.com/o66f2kl.png)

As previously mentioned, the ultrasonic sensor had issues sensing the desk edge, so this distance measuring sensor unit was added. Ideally, this sensor would be used to measure distance directly, however due to the nature of the non-linear (and relatively undocumented) analog output, along with the varying reflectivity of the surfaces and angles measured to, some mathematical code had to be added to determine distance not from the voltage, but instead from the angles between this sensor sending a low output (no desk in view), to a higher output (sensor pointing downwards at desk).


### [Miscellaneous]

Additional minor components were used, like solid core wires, [jumper jerky](https://shop.pimoroni.com/products/jumper-jerky), a memory card for the Pi, and copious amounts of Blu Tack (to keep wires in place and angle the camera down).
