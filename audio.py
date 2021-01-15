import pyaudio 
import time 
import numpy as np 
import wave 
import os 


class numpy_data_buffer:
    """
    A fast, circular FIFO buffer in numpy with minimal memory interactions by using an array of index pointers
    from https://github.com/tr1pzz/Realtime_PyAudio_FFT 
    """

    def __init__(self, n_windows, samples_per_window, dtype = np.float32, start_value = 0, data_dimensions = 1):
        self.n_windows = n_windows
        self.data_dimensions = data_dimensions
        self.samples_per_window = samples_per_window
        self.data = start_value * np.ones((self.n_windows, self.samples_per_window), dtype = dtype)

        if self.data_dimensions == 1:
            self.total_samples = self.n_windows * self.samples_per_window
        else:
            self.total_samples = self.n_windows

        self.elements_in_buffer = 0
        self.overwrite_index = 0

        self.indices = np.arange(self.n_windows, dtype=np.int32)
        self.last_window_id = np.max(self.indices)
        self.index_order = np.argsort(self.indices)

    def append_data(self, data_window):
        self.data[self.overwrite_index, :] = data_window

        self.last_window_id += 1
        self.indices[self.overwrite_index] = self.last_window_id
        self.index_order = np.argsort(self.indices)

        self.overwrite_index += 1
        self.overwrite_index = self.overwrite_index % self.n_windows

        self.elements_in_buffer += 1
        self.elements_in_buffer = min(self.n_windows, self.elements_in_buffer)

    def get_most_recent(self, window_size):
        ordered_dataframe = self.data[self.index_order]
        if self.data_dimensions == 1:
            ordered_dataframe = np.hstack(ordered_dataframe)
        return ordered_dataframe[self.total_samples - window_size:]

    def get_buffer_data(self):
        return self.data[:self.elements_in_buffer]



class audio_input():
    def __init__(self, rate = 44100, chunck = 8192, device_index=1, time_record = 10, save_dirc='./'):
        self.format = pyaudio.paInt16
        self.rate = rate
        self.chunck = chunck 
        self.device_index = device_index
        self.channels = 1
        self.pa = pyaudio.PyAudio()
        self.num_chuncks = 0 
        self.stream = self.pa.open(format = self.format, \
                                rate = self.rate,\
                                channels = self.channels,\
                                input = True,\
                                input_device_index = self.device_index,\
                                frames_per_buffer = self.chunck,\
                                start = True,\
                                stream_callback = self.analyze)

        self.num_windows = time_record*rate//chunck 
        self.ringbuffer = numpy_data_buffer(self.num_windows, self.chunck, dtype=np.int16)
        self.energy_th = np.zeros((rate//chunck))
        self.event_detected = False 
        self.save_dirc = save_dirc 
    
    def cap_voice_event(self):
        self.wait_recording(5)
        file_name = self.save_recording()
        return file_name 

    def voice_detected(self):
        return self.event_detected

    def analyze(self, in_data, frame_count, time_info, status):
        self.num_chuncks +=1 
        # print('received message num of chunks: {}'.format(self.num_chuncks))
        # print('in data len: {}, frame_count: {}'.format(len(in_data), frame_count))
        data = np.frombuffer(in_data, dtype=np.int16)
        self.ringbuffer.append_data(data)
        energy = np.mean(np.square(data))
        self.energy_th[:-1] = self.energy_th[1:]
        if energy >200:
            self.energy_th[-1]=1
        else:
            self.energy_th[-1]=0
        if np.sum(self.energy_th)>0.5*self.rate/self.chunck:
            # print('voice detected')
            self.event_detected = True 
        else:
            self.event_detected = False 
        # print('energy in the chunk: {}'.format(np.mean(np.square(data))))
        return in_data, pyaudio.paContinue
        

    def stop_recording(self):
        self.stream.stop_stream()

    def start_recording(self):
        self.stream.start_stream()

    def is_active(self):
        return self.stream.is_active()
    
    def is_stopped(self):
        return self.stream.is_stopped()
    
    def wait_recording(self, seconds):
        time.sleep(seconds)

    def save_recording(self):
        file_name = os.path.join(self.save_dirc, time.strftime("%Y%m%d_%H%M%S") + '.wav')
        frames = self.ringbuffer.get_buffer_data()
        print('saving audio files: {}'.format(file_name))
        # print('number of frames:{}'.format(len(frames)))
        # print(frames.shape)
        # print(frames)
        with wave.open(file_name, 'wb') as wavefile:
            wavefile.setnchannels(self.channels)
            wavefile.setsampwidth(self.pa.get_sample_size(pyaudio.paInt16))
            wavefile.setframerate(self.rate)
            wavefile.writeframes(frames.flatten())
        return file_name 

    def __del__(self):
        self.stream.stop_stream()
        self.stream.close()
        self.pa.terminate()


    
if __name__ == '__main__':
    print('init...')
    audio = audio()
    audio.start_recording()
    audio.wait_recording(20)
    audio.stop_recording()
    print('end')
    audio.save_recording()
    print('num of windows: {}'.format(audio.num_chuncks))


