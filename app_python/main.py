import requests
import re
import json
import io
import subprocess
from flask import Flask, request
from google.cloud import storage
from google.cloud.storage.blob import Blob
from google.cloud import speech

app = Flask(__name__)

bucket_name = 'globalgame-assets'
speech_client = speech.SpeechClient()

def gcp_storage_upload_string(source_string, bucket_name, blob_name):
    try:
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_string(source_string)
        print(f'[ INFO ] Uploaded {blob_name} to GCS bucket {bucket_name}')
    except Exception as e:
        print(f'[ ERROR ] Failed to upload to GCS. {e}')

def gcp_storage_upload_filename(filename, bucket_name, blob_name):
    try:
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_filename(filename)
        print(f'[ INFO ] Uploaded {blob_name} to GCS bucket {bucket_name}')
    except Exception as e:
        print(f'[ ERROR ] Failed to upload to GCS. {e}')

def speech_to_text_short(gcs_uri):
    '''
    Google Cloud Speech-to-Text (short audio)
    '''
    audio = speech.RecognitionAudio(uri=gcs_uri)
    config = speech.RecognitionConfig(
        #encoding=speech.RecognitionConfig.AudioEncoding.FLAC,
        #sample_rate_hertz=16000,
        language_code="en-US",
        enable_automatic_punctuation=True,
    )
    
    response = speech_client.recognize(config=config, audio=audio)
    
    sentences = []
    for result in response.results:
        sentences.append(result.alternatives[0].transcript)
    
    return sentences

def download_online_file(response, saved_filename):
    '''
    "response" comes from requests.get or request.post response
    '''
    if response.status_code == 200:
        print(f'[ INFO ] Saving {response.url} as {saved_filename}')
        with open(saved_filename, 'wb') as f:
            #f.write(response.content)
            for chunk in response.iter_content(chunk_size=1024): 
                if chunk:
                    f.write(chunk)
    
    return None

@app.route("/audio", methods = ['GET','POST'])
def audio():
    
    if request.method == 'POST':
        try:
            payload   = request.get_json()
            audio_uri = payload['audio_uri']
            print(f'''[ INFO ] User-provided payload: {payload}''')
            
            response = requests.get(audio_uri)
            print(f'[ INFO ] Requested audio file. Status code: {response.status_code}')
            if response.status_code == 200:
                
                audio_filename = audio_uri.split('/')[-1]
                
                # Write audio to GCS so that STT can be ran against this file.
                if True: # re.search('\.mp3$',audio_filename):
                    # Save audio file
                    download_online_file(response=response, saved_filename=audio_filename)
                    # Upload raw (initial) audio file
                    gcp_storage_upload_string(response.content, bucket_name=bucket_name, blob_name=audio_filename)
                    # Convert mp3 to flac
                    audio_filename_flac = re.sub('\.[a-z0-9]+$','.flac',audio_filename.lower())
                    subprocess.call(['ffmpeg', '-i', audio_filename, '-ac', '1', audio_filename_flac])
                    gcp_storage_upload_filename(filename=audio_filename_flac, bucket_name=bucket_name, blob_name=audio_filename_flac)
                
                # GCS Path
                gcs_uri = f'gs://{bucket_name}/{audio_filename_flac}'
                
                # Write audio payload to GCS
                audio_payload_filename = re.sub('\.[a-z0-9]+$', '.json', audio_uri.lower().split('/')[-1])
                print(f'[ INFO ] Writing {audio_payload_filename} to GCS')
                gcp_storage_upload_string(json.dumps(payload), bucket_name=bucket_name, blob_name=audio_payload_filename)
                
                # Speech-to-Text
                print(f'[ INFO ] Performing Speech-to-Text against {gcs_uri}')
                sentences = speech_to_text_short(gcs_uri=gcs_uri)
                transcript = ' '.join(sentences)
                
                print(f'''[ INFO ] {audio_uri} has been processed''')
                return transcript, 200
            else:
                msg = f'Failed to get {audio_uri}. Status Code: {response.status_code}. {response.content}'
                print(f'''[ ERROR ] {msg}''')
                return msg, response.status_code
        except Exception as e:
            return f'{e}', 400

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
