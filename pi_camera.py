import numpy as np
import picamera
from picamera.array import PiMotionAnalysis
import time 
import io 
from PIL import Image 
from subprocess import call
import os 

class DetectMotion(PiMotionAnalysis):
    def __init__(self, picamera, size):
        super(DetectMotion, self).__init__(picamera, size)
        self.framerate = int(picamera.framerate)
        # print(self.framerate)
        # motion for each frame in the passed fourseconds 
        self.frame_motions = np.zeros(self.framerate//3)
        self.motion_detected = False
        self.size = size 
        self.TH = size[0]*size[1]*3.2e-5
        
    def analyze(self, a):
        # queue the current frame motions 
        self.frame_motions[1:] = self.frame_motions[:-1]
        a = np.sqrt(
            np.square(a['x'].astype(np.float)) +
            np.square(a['y'].astype(np.float))
            ).clip(0, 255).astype(np.uint8)
        # If there're more than TH vectors with a magnitude greater
        # than 60, then say we've detected motion
        # this two values can be changed according to your scenario (objective size, sensitivity, etc.)
        if (a > 60).sum() > self.TH:
            # print('Motion detected!')
            self.frame_motions[0] = 1

            if np.all(self.frame_motions):
                self.motion_detected = True
        else:
            self.frame_motions[0] = 0 
            
            self.motion_detected = False


class pi_camera():
    def __init__(self, video_res=(640,480), image_dir = './image_clips', video_dir = './video_clips', framerate=8):
        self.image_dir = image_dir
        self.video_dir = video_dir
        self.camera =  picamera.PiCamera()
        self.camera.resolution = self.camera.MAX_RESOLUTION
        self.camera.framerate = framerate
        self.framerate = framerate 
        self.video_res = video_res 
        self.circular_buff = picamera.PiCameraCircularIO(self.camera, seconds=20)
        self.motion_analysis_output = DetectMotion(self.camera, size = video_res)
        self.imageIO = io.BytesIO()
        self.start_recording()
        time.sleep(2)
        # take the first image 
        print('taking the first image')
        # self.cap_image()
        print('camera initialize done')

    def start_recording(self):
        self.camera.start_recording(
            self.circular_buff, format='h264', 
            resize = self.video_res, 
            motion_output=self.motion_analysis_output)

    def wait_recording(self,seconds):
        self.camera.wait_recording(seconds)
    
    def stop_recording(self):
        self.camera.stop_recording()

    def motion_detected(self):
        return self.motion_analysis_output.motion_detected

    def cap_image(self):
        file_name =time.strftime("%Y%m%d-%H%M%S") +'.jpg'
        image_path = os.path.join(self.image_dir, file_name)
        self.camera.capture(image_path, format = 'jpeg', use_video_port = True)
            # print('time cost to capture: {} seconds'.format(time.time() - stime))
        return image_path
    
    def cap_motion_event(self):
        self.camera.wait_recording(10)
        file_path = os.path.join(self.video_dir, time.strftime("%Y%m%d_%H%M%S"))
        self.circular_buff.copy_to(file_path + '.h264', seconds = 20)
            # bot.send_animation(chat_id = chat_id, animation = open('./video_clips/record.h264', 'rb'))
        command = "MP4Box -add " + file_path + '.h264' + " " + file_path + '.mp4'+ ' -fps ' +str(self.framerate)
            # print(command)
        call([command], shell=True, stdout=open(os.devnull, 'wb'))
        # bot.send_video(chat_id, video = open(filename + '.mp4', 'rb'))
        self.circular_buff.clear()
        return file_path + '.mp4'

    def cap_video(self):
        file_path = os.path.join(self.video_dir, time.strftime("%Y%m%d_%H%M%S"))
        self.circular_buff.copy_to(file_path + '.h264', seconds = 20)
        command = "MP4Box -add " + file_path + '.h264' + " " + file_path + '.mp4' + ' -fps ' +str(self.framerate)
        call([command], shell=True, stdout=open(os.devnull, 'wb'))
        self.circular_buff.clear()
        return file_path + '.mp4'

    
    def __del__(self):
        self.camera.close()
        self.imageIO.close()
        self.circular_buff.close()
        self.motion_analysis_output.close()
