import requests
import re
import json
from google.cloud import storage
from google.cloud.storage.blob import Blob
from flask import Flask, request

app = Flask(__name__)

def gcp_storage_upload_string(source_string, bucket_name, blob_name):
    try:
        storage_client = storage.Client()
        bucket = storage_client.get_bucket(bucket_name)
        blob = bucket.blob(blob_name)
        blob.upload_from_string(source_string)
        print(f'[ INFO ] Uploaded {blob_name} to GCS bucket {bucket_name}')
    except Exception as e:
        print(f'[ ERROR ] Failed to upload to GCS. {e}')

@app.route("/audio", methods = ['GET','POST'])
def audio():
    
    if request.method == 'POST':
        try:
            payload   = request.get_json()
            audio_uri = payload['audio_uri']
            print(f'''[ INFO ] Request payload: {payload}''')
            
            req = requests.get(audio_uri)
            print(f'[ INFO ] Reg status code: {req.status_code}')
            if req.status_code == 200:
                
                # Write audio to GCS so that STT can be ran against this file.
                audio_filename = audio_uri.split('/')[-1]
                gcp_storage_upload_string(req.content, bucket_name='globalgame-assets', blob_name=audio_filename)
                
                # Write audio payload to GCS
                audio_payload_filename = re.sub('\.[a-zA-Z0-9]{2,4}$','',audio_uri.split('/')[-1])+'.json'
                gcp_storage_upload_string(json.dumps(payload), bucket_name='globalgame-assets', blob_name=audio_payload_filename)
                
                return f'''{audio_uri} has been processed''', 200
            else:
                return f'Failed to get {audio_uri}', req.status_code
        except Exception as e:
            return f'{e}', 400

if __name__ == "__main__":
    app.run(debug=True, host="0.0.0.0", port=8080)
