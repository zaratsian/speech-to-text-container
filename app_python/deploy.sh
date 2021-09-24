# Load Config
. ./default.config

# Enable necessary GCP services
gcloud services enable run.googleapis.com

REGISTRY="${GCP_ARTIFACT_REGISTRY_REGION}-docker.pkg.dev/${GCP_PROJECT_ID}/${GCP_ARTIFACT_REGISTRY_NAME}"

gcloud run deploy audio-input \
    --image $REGISTRY/audio-input:latest \
    --allow-unauthenticated \
    --region us-east1 \
    --concurrency 80 \
    --cpu 1 \
    --memory 256M \
    --max-instances 5 \
    --min-instances 0 \
    --timeout 120

#Testing from Cloud Shell - load random audio file
#curl -X POST -H "Authorization: Bearer $(gcloud auth print-identity-token)" "https://audio-input-cyj7y6zvsq-ue.a.run.app/audio" \
#   -H "Content-Type: application/json" \
#   -d '{"audio_uri":"https://github.com/prof3ssorSt3v3/media-sample-files/blob/master/fight-club.mp3","name":"test name"}'