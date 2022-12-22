from flask import Flask, request
from youtube_transcript_api import YouTubeTranscriptApi
from sklearn.feature_extraction.text import TfidfVectorizer
import pandas as pd
import regex as re
import string
import pickle

app = Flask(__name__)

@app.get('/prediction')
def prediction_api():
    url = request.args.get('url', '')
    video_id = url.split('=')[1]
    predictions = video_predict(get_transcript(video_id))
    print("api called")
    return predictions, 200


### return a string of YouTube video transcript
def get_transcript(video_id):
    transcript_list = YouTubeTranscriptApi.get_transcript(video_id)
    transcript = ' '.join(d['text'] for d in transcript_list)
    return transcript

### return a tuple with size of 4 containing model predictions in the form of 0 and 1.
### 0 = fake; 1 = real
def video_predict(transcript):
    ### load models
    LR = load_pickle('pickle_models/lr_model.pkl')
    GBC = load_pickle('pickle_models/gbc_model.pkl')
    DT = load_pickle('pickle_models/dt_model.pkl')
    RFC = load_pickle('pickle_models/rfc_model.pkl')
    vectorization = TfidfVectorizer()

    testing_news = {"text":[transcript]}
    new_def_test = pd.DataFrame(testing_news)
    new_def_test["text"] = new_def_test["text"].apply(wordopt) 
    new_x_test = new_def_test["text"]
    new_xv_test = vectorization.transform(new_x_test)

    ### model predictions
    pred_LR = LR.predict(new_xv_test)
    pred_GBC = GBC.predict(new_xv_test)
    pred_DT = DT.predict(new_xv_test)
    pred_RFC = RFC.predict(new_xv_test)
    print("executed")
    return str(pred_LR[0]) + str(pred_GBC[0]) + str(pred_DT[0]) + str(pred_RFC[0])
    # return (pred_LR[0], pred_GBC[0], pred_DT[0], pred_RFC[0])


### return a processed text
def wordopt(text):
    text = text.lower()
    text = re.sub('\[.*?\]', '', text)
    text = re.sub("\\W"," ",text) 
    text = re.sub('https?://\S+|www\.\S+', '', text)
    text = re.sub('<.*?>+', '', text)
    text = re.sub('[%s]' % re.escape(string.punctuation), '', text)
    text = re.sub('\n', '', text)
    text = re.sub('\w*\d\w*', '', text)    
    return text


def load_pickle(path):
    with open(path, 'rb') as f:
        obj = pickle.load(f)
    return obj


if __name__ == '__main__':
    app.run()