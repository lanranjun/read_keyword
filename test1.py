import wave
import string
from pyaudio import PyAudio
from pynput.keyboard import Controller, Key, Listener
import threading

chars = list(string.ascii_lowercase)

cache = ""
zt_list = ["zhi", "chi", "shi", "ri", "zi", "ci", "si", "yi", "wu", "yu", "ye", "yue", "yuan", "yin", "yun", "ying"]
ym_list = ["ai", "ei", "ui", "ao", "ou", "iu", "ie", "ve", "er", "an", "en", "in", "un", "vn", "ang", "eng", "ing",
           "ong"]


# 监听按压
def on_press(key):
    global cache
    try:
        print("cache: ", cache)
        print("正在按压:", format(key.char))
        char = format(key.char)
        if char in chars:
            cache += char

    except AttributeError:
        print("正在按压:", format(key))


# 监听释放
def on_release(key):
    global cache
    print("已经释放:", format(key))
    if key == Key.esc:
        # 停止监听
        return False
    if key == Key.space:
        items = []
        for zt in zt_list:
            if zt in cache:
                items.append(zt)
                cache = cache.replace(zt, "")
        for ym in ym_list:
            if ym in cache:
                items.append(ym)
                cache = cache.replace(ym, "")
        for c in cache:
            if c in chars:
                items.append(c)
                cache = cache.replace(c, "")
        for item in items:
            file_path = f"sounds/{item}.wav"
            play(file_path)


# 开始监听
def start_listen():
    with Listener(on_press=on_press, on_release=on_release) as listener:
        listener.join()


# 播放音乐
def play(filename):
    chunk = 1024
    wf = wave.open(filename, 'rb')
    p = PyAudio()
    stream = p.open(format=p.get_format_from_width(wf.getsampwidth()), channels=wf.getnchannels(),
                    rate=wf.getframerate(), output=True)
    data = wf.readframes(chunk)
    while data != b'':
        data = wf.readframes(chunk)
        stream.write(data)
    stream.stop_stream()
    stream.close()
    p.terminate()


if __name__ == '__main__':
    sema = threading.Semaphore(value=5)
    # 实例化键盘
    kb = Controller()
    start_listen()