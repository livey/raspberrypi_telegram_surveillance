## raspberrypi_telegram_surveillance
Use pi camera to detect the moition and sent the video to your telegram. 
The image resolution is maximized. When the video resolution is 1920*7972, it manages framerate 8. 

## dependencies
[sudo apt install gpac](https://gpac.wp.imt.fr/tag/mp4box/)  
[py telegram api](https://github.com/eternnoir/pyTelegramBotAPI)  
pi camera

## limitations & improvements
* The pi camera only output motion vector when you choose h264 format while the telegram bot support mp4 video. So, we need MP4Box to do format converting.
* Some in memory operations can reduce the disc reading, for example, capture a image and send it to telegram and capture video, convert to mp4 and send it to telegram.
* periodic operations such as taking a photo can be scheduled with more sophisticated schedular for example thread.Timer()
* when motion detected, we can send a thread signal to trigger sending it to telegram instead of always checking its status. 

## to do list
- [x] photo request
- [x] video request
- [x] motion detection
- [x] stop, start
- [ ] voice detection
- [ ] adjust exposure time according to your local time
