## GPIO Control
**GPIO Control** - tool designed to provide control on Raspberry pi's GPIO module by simple and elegant android app. This library gives possibility to build smart switching solutions by connection cheap electronic relays to GPIO modules. 

## Content
- [Requirements](#requirements)
- [Features](#features)
- [Installation and Usage](#installation-and-usage)
- [Dependencies](#dependencies)
- [Author](#author)
- [License](#license)

## Requirements
### Server
* Python 3.6+
* Raspbian 4.0+

### Client
* Android 5.0+

## Features
- [x] Quick, secure and reliable TCP communication
- [x] Readable and flexible interface to control Raspberry Pi
- [x] Simple configuration of connected devices

## Installation and Usage
### Server
To deploy server you need Raspian 4.0+ or any Unix system supporting Raspberry Pi hardware. Specify GPIO pins which you want to control and fill all device names in 'server_main.py' file. To start program run it with command line "python3 server_main,py". When program starts the 'android_config.txt' file will be created. Copy content of this file to your clipboard (it will be useful in client installation). In long term usage of that library, you can add bash script to crontab.It automatically starts server when device is booting.

### Client
Client installation can be completed in two ways: you can build app from the repository or just download apk file on target device. After the installation start the application. When main screen is shown click pencil icon at left bottom corner. The last thing you should do is paste content of 'android_config.txt' file and click save button. Now you should have full control on connected devices.

## Dependencies
### Server
* Internet connection
* https://pypi.org/project/RPi.GPIO/ - For GPIO module support

### Client
* Internet connection
* Allow android app to use internet connection
## Authors
* https://github.com/kkuuba

## License
GPIO Control is released under the MIT license. See LICENSE for details.