GCP_PROJECT_ID="globalgame"
API_REGION="us-east1"
APP_ID=google-toxicity
CONFIG_ID=${APP_ID}-config
GATEWAY_ID=${APP_ID}-gateway
#BACKEND_SERVICE_ACCOUNT=service-826671308632@serverless-robot-prod.iam.gserviceaccount.com

# Enable GCP APIs
gcloud services enable apigateway.googleapis.com
gcloud services enable servicemanagement.googleapis.com
gcloud services enable servicecontrol.googleapis.com

# Create an API Config
gcloud api-gateway api-configs create ${CONFIG_ID} \
  --api=${APP_ID} --openapi-spec=openapi2-run.yaml \
  --project=${GCP_PROJECT_ID} #--backend-auth-service-account=${BACKEND_SERVICE_ACCOUNT}

# Deploy API Gateway
gcloud api-gateway gateways create ${GATEWAY_ID} \
  --api=${APP_ID} --api-config=${CONFIG_ID} \
  --location=${API_REGION} --project=${GCP_PROJECT_ID}



