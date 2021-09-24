# Load Config
. ./default.config

# Enable necessary GCP services
gcloud services enable artifactregistry.googleapis.com

# Setup Google Artifact Registry
gcloud artifacts repositories create ${GCP_ARTIFACT_REGISTRY_NAME} \
--repository-format=docker \
--location=${GCP_ARTIFACT_REGISTRY_REGION} \
--description="Audio processing artifacts"

# Verify that repo has been created
#gcloud artifacts repositories list

# Set up authentication to Docker repositories in the region
gcloud auth configure-docker "${GCP_ARTIFACT_REGISTRY_REGION}-docker.pkg.dev"

# Build Container
REGISTRY="${GCP_ARTIFACT_REGISTRY_REGION}-docker.pkg.dev/${GCP_PROJECT_ID}/${GCP_ARTIFACT_REGISTRY_NAME}"
echo "Artifact Registry Path: ${REGISTRY}"
docker build -t $REGISTRY/audio-input -f ./Dockerfile .

# Push image to Artifact Registry
docker push $REGISTRY/audio-input