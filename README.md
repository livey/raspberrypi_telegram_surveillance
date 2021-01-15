## raspberrypi_telegram_surveillance
Use pi camera to detect the moition and sent the video to your telegram. 
The image resolution is maximized. When the video resolution is 1920*792, it manages framerate 8. 

## dependencies
[sudo apt install gpac](https://gpac.wp.imt.fr/tag/mp4box/)  
[py telegram api](https://github.com/eternnoir/pyTelegramBotAPI)  
pi camera  
follow [this](https://raspberrypi.stackexchange.com/questions/75031/cannot-install-pyaudio) to install pyaudio

## limitations & improvements
* The framerate is so low. Do not know how to improve it. It is weird video resolutions 640x480 and 1920x792 result in the same maximal framerate 8. 
* The pi camera only output motion vector when you choose h264 format while the telegram bot support mp4 video. So, we need MP4Box to do format converting.
* Some in memory operations can reduce the disc reading, for example, capture a image and send it to telegram and capture video, convert to mp4 and send it to telegram.
* Periodic operations such as taking a photo can be scheduled with more sophisticated schedular for example thread.Timer()
* When motion detected, we can send a thread signal to trigger sending it to telegram instead of always checking its status. 
* If you are recording video, capturing image will stop the recording for about 2 seconds. The time also depends on the exposure setting. 
* Pay attention to the chunk size. Small chunk size will result in two frequent call backs and lead to lose of chunks. On my Raspberry Pi 4B. I set chunk-size=8192.  

## to do list
- [x] photo request
- [x] video request
- [x] motion detection
- [x] stop, start
- [x] voice detection
- [ ] adjust exposure time according to your local time
- [ ] more sophisticated voice detection and motion detection algorithms.
