import requests
import json
from speech_to_text import transcribe

ANALYTICS_URL = 'https://westcentralus.api.cognitive.microsoft.com/text/analytics/v2.0/keyPhrases'
headers = {
    'Content-Type': 'application/json',
    'Ocp-Apim-Subscription-Key': '538a04378d34481e9735503f87a05586',
    'Accept': 'application/json'
}

def analyze_audio(audioFile):

    chunk_times, corpus = transcribe(audioFile)

    data = {'documents': []}
    key_phrases = {"documents": []}
    time_ranges = []
    step = 7

    for i in range(0, len(corpus), step):

        time_ranges.append(chunk_times[i])

        excerpt = " ".join(corpus[i:i+step])
        id = i/step
        data['documents'].append({
            'id': id,
            'language': 'en',
            'text': excerpt
        })

        if(len(data['documents']) == 1000):
            json_dump = json.dumps(data)
            r = requests.post(ANALYTICS_URL, headers=headers, data=json_dump)
            key_phrases["documents"].extend(json.loads(r.text)["documents"])
            data['documents'] = []

    data = json.dumps(data)
    r = requests.post(ANALYTICS_URL, headers=headers, data=data)
    key_phrases["documents"].extend(json.loads(r.text)["documents"])

    #sync up
    return zip(time_ranges, key_phrases["documents"])
