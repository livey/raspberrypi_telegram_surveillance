## raspberrypi_telegram_surveillance
Use pi camera to detect the moition and sent the video to your telegram. 
The image resolution is maximized. When the video resolution is 1920*792, it manages framerate 8. 

## dependencies
[sudo apt install gpac](https://gpac.wp.imt.fr/tag/mp4box/)  
[py telegram api](https://github.com/eternnoir/pyTelegramBotAPI)  
pi camera

## limitations & improvements
* The framerate is so low. Do not know how to improve it. It is weird video resolutions 640*480 and 1920*792 result in the same maximal framerate 8. 
* The pi camera only output motion vector when you choose h264 format while the telegram bot support mp4 video. So, we need MP4Box to do format converting.
* Some in memory operations can reduce the disc reading, for example, capture a image and send it to telegram and capture video, convert to mp4 and send it to telegram.
* Periodic operations such as taking a photo can be scheduled with more sophisticated schedular for example thread.Timer()
* When motion detected, we can send a thread signal to trigger sending it to telegram instead of always checking its status. 
* If you are recording video while capturing image is called, it will stop recording for about 2 seconds. The time also depends on the exposure setting. 

## to do list
- [x] photo request
- [x] video request
- [x] motion detection
- [x] stop, start
- [ ] voice detection
- [ ] adjust exposure time according to your local time
