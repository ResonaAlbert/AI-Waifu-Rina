import os
import logging
import onnxruntime
from transformers import BertTokenizer
import numpy as np


class SentimentEngine():
    def __init__(self, model_path):
        logging.info('Initializing Sentiment Engine...')
        onnx_model_path = model_path

        self.ort_session = onnxruntime.InferenceSession(onnx_model_path, providers=['CPUExecutionProvider'])

        self.tokenizer = BertTokenizer.from_pretrained('bert-base-chinese')

    def infer(self, text):
        tokens = self.tokenizer(text, return_tensors="np")
        input_dict = {
            "input_ids": tokens["input_ids"],
            "attention_mask": tokens["attention_mask"],
        }
        # Convert input_ids and attention_mask to int64
        input_dict["input_ids"] = input_dict["input_ids"].astype(np.int64)
        input_dict["attention_mask"] = input_dict["attention_mask"].astype(np.int64)
        logits = self.ort_session.run(["logits"], input_dict)[0]
        probabilities = np.exp(logits) / np.sum(np.exp(logits), axis=-1, keepdims=True)
        predicted = np.argmax(probabilities, axis=1)[0]
        logging.info(f'Sentiment Engine Infer: {predicted}')
        return predicted

# r=0 positio, if r higher, more negative

""" if __name__ == '__main__':
    t = '我爱你'
    dirname, filename = os.path.split(os.path.realpath(__file__))
    print(dirname)
    path = dirname + '\paimon_sentiment.onnx'
    s = SentimentEngine(path)
    r = s.infer(t)
    print(r)
    txt="今天天气真好！"
    r = s.infer(txt)
    print(txt, ":", r)
    txt="今天天气真糟糕！"
    r = s.infer(txt)
    print(txt, ":", r)
    txt="我和朋友一起度过了愉快的一天。"
    r = s.infer(txt)
    print(txt, ":", r)
    txt="我很生你的气"
    r = s.infer(txt)
    print(txt, ":", r)
    txt="我很感激你的帮助。"
    r = s.infer(txt)
    print(txt, ":", r) """
    
