# Get GCP Identity Token 
# https://cloud.google.com/sdk/gcloud/reference/auth/print-identity-token
GCP_TOKEN="$(gcloud auth print-identity-token)"

# Call test script
python3 test.py \
--endpoint https://audio-input-cyj7y6zvsq-ue.a.run.app/audio \
--token $GCP_TOKEN \
--json_payload '{"audio_uri":"https://github.com/zaratsian/speech-to-text-container/raw/main/samples/otherguys_clip1.mp3"}'
