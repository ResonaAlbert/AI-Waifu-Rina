import dlna
import time

def search_devices():
    devices = dlna.Discover()
    for device in devices:
        print(device.friendly_name)
    return devices

def play_audio(device, audio_file):
    device.play(audio_file)
    print("正在播放音频：{} 到设备：{}".format(audio_file, device.friendly_name))

def main():
    devices = search_devices()
    if devices:
        device = devices[0]
        play_audio(device, "/path/to/audio/file")
        time.sleep(10)
        device.stop()
        print("停止播放音频")
    else:
        print("没有找到可用的DLNA设备")

if __name__ == "__main__":
    main()
