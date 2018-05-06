Instructions for setting up and using the robot, and training the neural network, via an external PC (host machine) with a microSD card reader and WiFi.

These are written to work on any Unix based OS, but the general ideas would also work with Windows or macOS.

First, clone this repository to the main machine (not the Raspberry Pi), then...


### Prerequisites
1. This repository cloned onto the host machine (not the Raspberry Pi).
2. Python, pip and (optionally) virtualenv on the host machine.


### Headless Raspberry Pi Zero setup

1. Download [Raspbian Lite](https://www.raspberrypi.org/downloads/raspbian/) and use [Etcher](https://etcher.io/) to burn it to microSD card.


2. Unplug SD card and shove it back in again to remount it.


3. Figure out where it's mounted (with a file manager, or the command df -h), and change directory to the boot folder in it.
   ```
   $ cd /run/media/{your-username}/{ad6203a1-ec50-4f44-a1c0-e6c3dd4c9202-or-something}/boot
   ```

4. Create a new empty file called "ssh", to allow us to connect via SSH to the Pi later. Note that there is no file extension.
   ```
   $ touch ssh
   ```


5. To get the Pi auto-magically connectied to WiFi, create a wpa_supplicant.conf file (I'm using nano).
   ```
   $ nano wpa_supplicant.conf
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
   To allow connections to different networks, simply add more `network={}`s.


6. Remove the microSD from the PC, put it in the Pi, then plug the Pi into it's power supply.


7. Use Nmap to figure out the IP address of the Pi. Alternatively you could rummage around your router's settings page.
   ```
   $ sudo nmap -sn 192.168.1.0/24
   ```
   Note that this must be run as super user to show extra details about the addresses. [Here's an explanation of the "/24"](https://serverfault.com/questions/270005/what-is-the-slash-after-the-ip).


8. SSH into the Pi - your Pi's IP address is probably different, and may change as we haven't set it to be static.
   ```
   $ ssh pi@192.168.1.4
   ```
   The default Raspberry Pi password is "raspberry". It's recommended that you change this with the `passwd` command.


9. SFTP into the Pi by entering this into Thunar's address bar (or however with your SFTP client of choice).
   ```
   sftp://pi@192.168.1.4/
   ```



### Python Code on the Raspberry Pi

1. Follow the instruction on [the 4tronix instructions here](https://4tronix.co.uk/blog/?p=1224) to ensure the Raspberry Pi is setup correctly.


2. Download the the 4tronix piconzero library onto the host machine to end up with the folder structure:
   ```
   DeskBot-Zero -> lib -> PiconZero -> Python -> .py files
   ```


3. Via SFTP, copy over the lib and src files into a `DeskBot-Zero' (case insensitive) on the Raspberry Pi. These can now be deleted from the host machine, but it's easier to leave them so that if desired they can be edited more comfortably.
 


### Compiling & installing OpenCV on the Raspberry Pi
This takes a long time! Pre-built packages for the Pi Zero seem rare and/or outdated, but mine could be linked to from here rather than having this full tutorial. Mostly copied from this guide https://www.pyimagesearch.com/2015/12/14/installing-opencv-on-your-raspberry-pi-zero/


1. Install dev tools:
   ```
   $ sudo apt-get install build-essential cmake pkg-config
   ```


2. Install image I/O packages:
   ```
   $ sudo apt-get install libjpeg-dev libtiff5-dev libjasper-dev libpng12-dev
   ```


3. Install video I/O packages (~250MB):
   ```
   $ sudo apt-get install libavcodec-dev libavformat-dev libswscale-dev libv4l-dev
   $ sudo apt-get install libxvidcore-dev libx264-dev
   ```


4. Pull down a routine optimization packages leveraged by OpenCV:
   ```
   $ sudo apt-get install libatlas-base-dev gfortran
   ```


5. Install Python 2.7 headers so we can compile OpenCV + Python bindings:
   Note: Python 2 support is ending in 2020. Switching to Python 3 could be a good idea.
   ```
   $ sudo apt-get install python2.7-dev
   ```


6. Get recent OpenCV source (~80MB):
   ```
   $ wget -O opencv.zip https://github.com/Itseez/opencv/archive/3.3.0.zip
   $ unzip opencv.zip
   ```


7. Get opencv_contrib, which contains stuff no longer included in OpenCV 3 [due to licensing](https://www.pyimagesearch.com/2015/07/16/where-did-sift-and-surf-go-in-opencv-3/). (~50MB):
   ```
   $ wget -O opencv_contrib.zip https://github.com/Itseez/opencv_contrib/archive/3.3.0.zip
   $ unzip opencv_contrib.zip
   ```


8. Delete the two zip files to save space:
   ```
   $ rm opencv.zip opencv_contrib.zip
   ```


9. Install the Python package manager pip:
   ```
   $ wget https://bootstrap.pypa.io/get-pip.py
   $ sudo python get-pip.py
   ```


10. Install NumPy (could take a while) (sudo required?):
    ```
    $ sudo pip install numpy
    ```


11. Setup OpenCV build using CMake:
    ```
    $ cd ~/opencv-3.3.0/
    $ mkdir build
    $ cd build
    $ cmake -D CMAKE_BUILD_TYPE=RELEASE \
       -D CMAKE_INSTALL_PREFIX=/usr/local \
       -D INSTALL_C_EXAMPLES=ON \
       -D INSTALL_PYTHON_EXAMPLES=ON \
       -D OPENCV_EXTRA_MODULES_PATH=~/opencv_contrib-3.3.0/modules \
       -D BUILD_EXAMPLES=ON ..
    ```


12. Run make to start the compilation process. This will take MANY hours. Go sleep.
    ```
    make
    ```


13. Assuming compiling worked, install it:
    ```
    $ sudo make install
    $ sudo ldconfig
    ```


14. Check if install worked:
    ```
    $ python
    >>> import cv2
    >>> cv2.__version__

    ```   
The directories opencv-3.0.0 and opencv_contrib-3.0.0 could be removed to save space, but then if something breaks re-compilation might be necessary.



### Running the dataset collection routine

1. In the SSH connection to the Raspberry Pi in the DeskBot-Zero directory, run:
   ```
   $ python /src/Python/dataCollect.py
   ```


2. To stop the robot, press ctrl+c. Images with classification filenames are stored in the `/src/Python/TrainingImages` directory.



### Setting up and running the neural network training

There are two versions of the project's neural network. One with purely TensorFlow, and one with Keras (which uses TensorFlow). Currently only the Keras implementation is functioning due to image loading issues.

1. Install TensorFlow following the [guide on their website](https://www.tensorflow.org/install/) - including the Nvidia requirements if training on a GPU is desired, it's ~20x faster! The Virtualenv installation with Python3 is recommended as it's what the rest of these instructions will use, but and mechanism would work.


2. Install Keras following their [installation instructions](https://keras.io/#installation) or just with the following command:
   ```
   $ sudo pip install keras
   ```


3. Copy over images collected from the robot via SFTP (out of their individual data/time folders), or extract the test-dataset.zip, for the file structure:
   ```
   DeskBot-Zero -> neural-net -> img -> .pngs
   ```
  
  
4. Activate the virtual environment:
   ```
   $ source ~/Documents/tensorflow/bin/activate
   ```
   

5. Navigate to the neural-net implementation-specific directory (required for files to be found/saved in correct places):
   ```
   (tensorflow) $ cd Documents/DeskBot-Zero/neural-net/keras
   ```

6. Run:
   ```
   (tensorflow) $ python neural-net.py
   ```
   

### Final notes

If all has gone as planned, after some time setting up and training the neural network, loss and accuracy values should be printed (around 0.6 and 0.7 for the test dataset).


If issues are encountered during any stage of the process, feel free to ask me about it on [Twitter](http://twitter.com/burntcustard), via [email](mailto:burntcustard@gmail.com), or by submitting an issue on this repository (or even better a pull request with a fix)!
