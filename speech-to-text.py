import requests
import httplib
import uuid
import json
from conf import base_url, VIDEOS_FOLDER, EDITED_VIDEOS_FOLDER

class Microsoft_ASR():
    def __init__(self):
        self.sub_key = 'e2221948fba34597bf3487240602ac7c'
        self.token = None
        pass

    def get_speech_token(self):
        FetchTokenURI = "/sts/v1.0/issueToken"
        header = {'Ocp-Apim-Subscription-Key': self.sub_key}
        conn = httplib.HTTPSConnection('api.cognitive.microsoft.com')
        body = ""
        conn.request("POST", FetchTokenURI, body, header)
        response = conn.getresponse()
        str_data = response.read()
        conn.close()
        self.token = str_data
        print "Got Token: ", self.token
        return True

    def transcribe(self,speech_file):

        # Grab the token if we need it
        if self.token is None:
            print "No Token... Getting one"
            self.get_speech_token()

        endpoint = 'https://speech.platform.bing.com/speech/recognition/conversation/cognitiveservices/v1'
        # Params form Microsoft Example
        params = {'locale': 'en-US',
                  'language': 'en-US',
                  'requestid': uuid.uuid4(),
                  'format': 'simple'}
        content_type = "audio/wav; codec=""audio/pcm""; samplerate=16000"

        def stream_audio_file(speech_file, chunk_size=1024):
            with open(speech_file, 'rb') as f:
                while 1:
                    data = f.read(chunk_size)
                    if not data:
                        break
                    yield data

        headers = {'Authorization': 'Bearer ' + self.token,
                   'Content-Type': content_type,
                   'Expected': '100-continue'}

        resp = requests.post(endpoint,
                            params=params,
                            data=stream_audio_file(speech_file),
                            headers=headers)

        val = json.loads(resp.text)
        return val["DisplayText"]

def chunkVideoFiles(audioFilename):
    from pydub import AudioSegment
    from pydub.utils import make_chunks

    myaudio = AudioSegment.from_file(EDITED_VIDEOS_FOLDER + audioFilename, "wav")

    chunk_length_ms = 10000  # pydub calculates in millisec
    chunks = make_chunks(myaudio, chunk_length_ms)  # Make chunks
    chunk_names = []

    # Export all of the individual chunks as wav files
    for i, chunk in enumerate(chunks):
        chunk_name = EDITED_VIDEOS_FOLDER + "{}{}.wav".format(audioFilename, i)
        chunk_names.append(chunk_name)

        print "exporting", chunk_name
        chunk.export(chunk_name, format="wav")

    return chunk_names

def transcribe(audioFilename):
    ms_asr = Microsoft_ASR()
    ms_asr.get_speech_token()

    chunk_names = chunkVideoFiles(audioFilename)

    texts = []
    for chunk_name in chunk_names:
        text = ms_asr.transcribe(chunk_name)
        texts.append(text)
        print "Text: ", text

    return texts