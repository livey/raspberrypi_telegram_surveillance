import threading
import telebot
import time 
from pi_camera import pi_camera
from audio import audio_input 
token = 'your telegram bot token'
bot = telebot.TeleBot(token = token)
recent_chat_id =  your-chat-id 

surveillance_enabled = True 
camera = pi_camera(video_res = (1296, 972), framerate= 8) #(1296, 730) (640, 480) (1920, 1080) (1296, 972)
audio = audio_input(rate = 44100, chunck = 8192, device_index=1, time_record = 10, save_dirc='./audio_clips')

@bot.message_handler(commands=['start'])
def start_surveillance(message):
    global surveillance_enabled 
    global recent_chat_id 
    print('surveillance enabled')
    recent_chat_id = message.chat.id
    surveillance_enabled = True
    bot.reply_to(message, 'start watching') 

@bot.message_handler(commands=['photo'])
def take_photo(message):
    global recent_chat_id
    print('executing taking photo')
    recent_chat_id = message.chat.id
    try:
        file_name = camera.cap_image()
        bot.send_photo(recent_chat_id, open(file_name, 'rb'))
    except:
        bot.send_message(recent_chat_id, 'wait for a while and try again')

@bot.message_handler(commands=['video'])
def send_video_clips(message):
    global recent_chat_id
    print('executing sending video')
    recent_chat_id = message.chat.id
    try:
        file_name = camera.cap_video()
        bot.send_message(recent_chat_id, 'here is the video')
        bot.send_video(recent_chat_id, open(file_name, 'rb'))
    except:
        print('wait for a while and try again')
    

@bot.message_handler(commands=['stop'])
def stop_surveillance(message):
    global surveillance_enabled
    global recent_chat_id 
    print('stopping the surveillance')
    recent_chat_id = message.chat.id
    surveillance_enabled = False
    bot.reply_to(message, 'stop watch')

@bot.message_handler(commands=['audio'])
def send_audio_clips(message):
    global recent_chat_id 
    recent_chat_id = message.chat.id 
    print('audio acquisition')
    try:
        file_name = audio.save_recording()
        bot.send_message(recent_chat_id, 'here is the audio')
        bot.send_audio(recent_chat_id, open(file_name, 'rb'))
    except:
        bot.send_message(recent_chat_id, 'bot is busy, wait for a while')

def send_audio_event():
    global surveillance_enabled 
    global recent_chat_id 
    while True:
        time.sleep(0.01)
        if audio.voice_detected() and surveillance_enabled:
            print('voice detected at time: ' +  time.strftime("%Y%m%d-%H%M%S"))
            file_name = audio.cap_voice_event()
            bot.send_message(recent_chat_id, 'voice detected')
            bot.send_audio(recent_chat_id, open(file_name, 'rb'))


def periodic_cap_image():
    while True:
        try:
            camera.cap_image()
            print('image captured')
        except:
            print('camera is in use')
        time.sleep(600)

def send_motion_event():
    global surveillance_enabled
    global recent_chat_id 
    while True:
        time.sleep(0.01)
        if camera.motion_detected() and surveillance_enabled:
            print('motion detected at time ' + time.strftime("%Y%m%d-%H%M%S"))
            file_name = camera.cap_motion_event()
            bot.send_message(recent_chat_id, 'motion detected')
            bot.send_video(recent_chat_id, open(file_name, 'rb'))
            # time.sleep(10) 

t1 = threading.Thread(target = bot.polling)
t2 = threading.Thread(target = periodic_cap_image)
t3 = threading.Thread(target = send_motion_event)
t4 = threading.Thread(target = send_audio_event)
threads = [t1,t2,t3,t4]

for th in threads:
    th.start() 

for th in threads:
    th.join() 


