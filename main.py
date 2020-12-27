import threading
import telebot
import time 
from pi_camera import pi_camera

token = '***'
bot = telebot.TeleBot(token = token)

recent_chat_id = ****

motion_detect_enabled = True 
camera = pi_camera(framerate=8)

@bot.message_handler(commands=['start'])
def start_surveillance(message):
    global motion_detect_enabled 
    global recent_chat_id 
    print('surveillance enabled')
    recent_chat_id = message.chat.id
    motion_detect_enabled = True
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
    global motion_detect_enabled
    global recent_chat_id 
    print('stopping the surveillance')
    recent_chat_id = message.chat.id
    motion_detect_enabled = False
    bot.reply_to(message, 'stop watch')


def periodic_cap_image():
    while True:
        try:
            camera.cap_image()
            print('image captured')
        except:
            print('camera is in use')
        time.sleep(600)

def send_motion_event():
    global motion_detect_enabled
    global recent_chat_id 
    while True:
        if camera.motion_detected() and motion_detect_enabled:
            print('motion detected at time ' + time.strftime("%Y%m%d-%H%M%S"))
            file_name = camera.cap_motion_event()
            bot.send_message(recent_chat_id, 'motion detected')
            bot.send_video(recent_chat_id, open(file_name, 'rb'))

t1 = threading.Thread(target = bot.polling)
t2 = threading.Thread(target = periodic_cap_image)
t3 = threading.Thread(target = send_motion_event)
t1.start()
t2.start()
t3.start()
t1.join()
t2.join()
t3.join()

