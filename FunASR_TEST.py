from modelscope.pipelines import pipeline
from modelscope.utils.constant import Tasks
import pyaudio
import wave

def real_time_speech_recognition():
    # 创建语音识别的pipeline
    inference_pipeline = pipeline(
        device='cpu',
        task=Tasks.auto_speech_recognition,
        model='damo/speech_paraformer-large_asr_nat-zh-cn-16k-common-vocab8404-pytorch',
    )

    # 初始化音频输入流
    p = pyaudio.PyAudio()
    audio_stream = p.open(format=pyaudio.paInt16, channels=1, rate=16000, input=True, frames_per_buffer=1024)

    try:
        print("开始实时语音识别，按Ctrl+C停止...")
        while True:
            audio_data = audio_stream.read(1024)  # 从音频流中读取数据
            rec_result = inference_pipeline(audio_data)
            print("识别结果:", rec_result['text'])

    except KeyboardInterrupt:
        print("停止实时语音识别")
    finally:
        audio_stream.stop_stream()
        audio_stream.close()
        p.terminate()

if __name__ == "__main__":
    real_time_speech_recognition()
