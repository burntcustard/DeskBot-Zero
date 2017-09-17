Work in progress instructions for setting up and using the robot via an external PC, via a microSD card reader and then WiFi.

These should would work on any Unix based OS, or the general ideas would work with a Windows PC.

1. Download [Raspbian Lite](https://www.raspberrypi.org/downloads/raspbian/) and use [Etcher](https://etcher.io/) to burn it to microSD card.


2. Unplug SD card and shove it back in again to remount it.


3. Figure out where it's mounted (with a file manager, or the command df -h), and change directory to the boot folder in it.
   ```
   cd /run/media/{your-username}/{ad6203a1-ec50-4f44-a1c0-e6c3dd4c9202-or-something}/boot
   ```


4. Create a new empty file called "ssh", to allow us to connect via SSH to the Pi later. Note that there is no file extension.
   ```
   touch ssh
   ```


5. To get the Pi auto-magically connectied to WiFi, create a wpa_supplicant.conf file (I'm using nano).
   ```
   nano wpa_supplicant.conf
   ```
   In the file, put the following, edited to the appropriate country and WiFi details:
   ```
   ctrl_interface=DIR=/var/run/wpa_supplicant GROUP=netdev
   update_config=1
   country=GB
   
   network={
	   ssid="Your network SSID"
	   psk="Your WPA/WPA2 security key"
	   key_mgmt=WPA-PSK
   }
   ```


6. Remove the microSD from the PC, put it in the Pi, then plug the Pi into it's power supply.


7. Use Nmap to figure out the IP address of the Pi. Alternatively you could rummage around your router's settings page.
   ```
   sudo nmap -sn 192.168.1.0/24
   ```
   Note that this must be run as super user to show extra details about the addresses. [Here's an explanation of the "/24"](https://serverfault.com/questions/270005/what-is-the-slash-after-the-ip).


8. SSH into the PI - your Pi's IP address is probably different, and may change as we haven't set it to be static.
   ```
   ssh pi@192.168.0.4
   ```
   The default Raspberry Pi password is "raspberry".



#### TODO:
Instructions for setting up the PiCon Zero. For now [the instructions here](https://4tronix.co.uk/blog/?p=1224) could be used, but they may require some tweaking.
