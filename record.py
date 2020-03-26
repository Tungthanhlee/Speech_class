"""
This script is mostly copy from https://stackoverflow.com/questions/50832181/how-to-record-audio-in-python-without-giving-the-duration-in-advance
Modified and edited by Tungthanhlee
"""

import sys
import queue
import tempfile
import numpy as np
import sounddevice as sd
import soundfile as sf
import os
q = queue.Queue()

folder = "Tamsu"
# link = "https://vnexpress.net/the-gioi/covid-19-goi-bong-ma-khung-hoang-toan-cau-4074600.html"
sentence = "Qua đây tôi cũng muốn khuyên các bạn, nếu quen nhau thì nên tìm hiểu kỹ về gia đình và thân nhân của họ, tránh tình trạng như tôi đã gặp. "

if os.path.exists(f"data/{folder}") == False:
    os.mkdir(f"data/{folder}")

f = open(f"data/{folder}/info.txt", "a")
# write link
# f.write(f"{link}\n")
# Unique file name for every recording
filename = tempfile.mktemp(prefix='record_', suffix='.wav', dir=f'data/{folder}/')
f.write(f"{filename}\n")
#write text
f.write(f"{sentence}\n")

f.close()

def callback(indata, frames, time, status):
    """
    This is called from a separate thread for each audio block
    """
    if status:
        print(status, file=sys.stderr)
    q.put(indata.copy())




# Make sure the file is open before recording anything
with sf.SoundFile(filename, mode='x', samplerate=22050, channels=1) as file:
    with sd.InputStream(samplerate=22050, channels=1, callback=callback):
        print('#' * 80)
        print('press Ctrl+C to stop the recording')
        print('#' * 80)
        while True:
            file.write(q.get())