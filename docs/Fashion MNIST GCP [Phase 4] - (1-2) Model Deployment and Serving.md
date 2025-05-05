# Fashion MNIST [Phase 4]: (1/2) Model Deployment & Serving

## Overview
This document details the implementation of the deployment and serving infrastructure for the Fashion MNIST classification project on Google Cloud Platform. This phase focuses on operationalizing the trained models through appropriate deployment strategies, creating stable prediction interfaces, and establishing the foundation for continuous delivery. The implementation showcases professional ML engineering practices in model deployment, prediction API development, and infrastructure management.

## Completed Tasks

### 1. Vertex AI Model Endpoint Deployment

#### Implementation Details
- Successfully deployed AutoML baseline model to a dedicated Vertex AI endpoint
- Endpoint name: `fashion-mnist-automl`
- Endpoint ID: `3671617870330068992`
- Region: us-central1 (Iowa)
- Created on: May 5, 2025
- Model: AutoML baseline model (97.2% average precision)
- Configured with 1 minimum compute node for cost efficiency
- Auto-scaling enabled for handling variable traffic
- Implemented standard authentication for secure access
- Enabled access logging for comprehensive request tracking

#### Technical Considerations
- Selected optimal machine type balancing performance and cost
- Configured appropriate model runtime (TensorFlow Serving)
- Implemented Google-managed encryption for data security
- Established regional deployment for reduced latency
- Configured standard REST API access for broad compatibility

### 2. Cloud Run Prediction Service Implementation

#### Implementation Architecture
- Created containerized prediction service in Cloud Run
- Implemented with Flask web framework for API routing
- Container image built with Python 3.9 slim base image
- Deployed using Google Container Registry (GCR)
- Image tag: `gcr.io/fashion-mnist-gcp/prediction-service:v1.1`
- Developed RESTful API with health check and prediction endpoints
- Implemented production-ready web server (Gunicorn)

#### Core Functionality
- **Image Processing Pipeline**:
  - Dynamic image resizing to 28×28 pixels
  - Grayscale conversion for consistent input format
  - Min-Max [0,1] normalization matching training preprocessing
  - Vector flattening for compatibility with model expectations

- **Vertex AI Endpoint Integration**:
  - Secure authentication using environment variables
  - Properly formatted prediction requests
  - Structured JSON response formatting
  - Class label mapping for human-readable results
  - Confidence score interpretation

- **Production Considerations**:
  - Comprehensive error handling and logging
  - Multi-threaded request processing
  - Environment-based configuration
  - Clear API documentation through endpoint responses
  - Health monitoring endpoint

### 3. Testing and Validation

- Successfully tested service with fashion images from test dataset
- Verified proper image preprocessing pipeline
- Confirmed accurate classification results matching expected categories
- Validated error handling for invalid inputs
- Measured response timing for performance benchmarking
- Tested container locally before cloud deployment

### 4. Container Registry Integration

- Successfully built and pushed container image to GCR
- Implemented proper version tagging strategy
- Container size optimized for quick deployment
- Established foundation for version control and rollback capability
- Created pipeline for future CI/CD integration

### 5. Cloud Run Service Deployment

- Successfully deployed to Cloud Run service
- Service name: `serverless-prediction-service`
- URL: `https://serverless-prediction-service-1043645672756.us-central1.run.app`
- Configured with appropriate resource allocation (512 MiB memory, 1 CPU)
- Implemented authenticated access for security compliance
- Configured health checks for reliability monitoring:
  - HTTP health check to root endpoint (/)
  - 7-second initial delay for proper initialization
  - 5-second timeout for response
  - 3 failure threshold before marking unhealthy
  - 10-second check interval
- Set up environment variables:
  - PROJECT_ID: fashion-mnist-gcp
  - LOCATION: us-central1
  - ENDPOINT_ID: 3671617870330068992
- Enabled Cloud Run auto-scaling capabilities
- Configured request timeout (300 seconds) and concurrency (80 requests per instance)
- Added IAM policy binding for secure access during testing and development

### 6. Production Security Configuration

- Adapted to organization policy constraints for Cloud Run security
- Implemented authentication-required access pattern for the service
- Configured IAM policy binding for specific user access
- Established token-based authentication pattern for testing
- Successfully validated authenticated access using gcloud identity tokens
- Implemented appropriate security practices for ML model access
- Maintained separation between model serving and API layers for security boundary

## Key Technical Decisions

### 1. Architecture Selection

- **Multi-Tier Approach**: Separated model serving (Vertex AI) from API management (Cloud Run)
- **Benefits**:
  - Cleaner separation of concerns
  - Independent scaling of model and API layers
  - Improved resource utilization
  - Enhanced operational flexibility
  - Greater fault isolation

### 2. Container Strategy

- **Lightweight Base Image**: Used Python 3.9 slim to minimize container size
- **Dependency Management**: Pinned specific versions for reproducibility
- **Production Web Server**: Implemented Gunicorn with appropriate worker configuration
- **Environment Configuration**: Used environment variables for deployment flexibility

### 3. Preprocessing Pipeline

- **Consistent Normalization**: Applied identical preprocessing to training and inference
- **Image Format Standardization**: Converted all inputs to grayscale 28×28 format
- **Data Type Management**: Proper handling of numeric precision
- **Error Handling**: Robust validation of input formats

### 4. Authentication and Security

- **IAM Integration**: Secured Vertex AI endpoint access
- **Environment Separation**: Kept credentials out of container images
- **Proper Secret Management**: Used environment variables for sensitive configuration
- **Authenticated Access**: Implemented token-based authentication for Cloud Run service
- **IAM Policy Binding**: Configured specific user access for testing and development
- **Organization Policy Compliance**: Adapted deployment to work within organizational security constraints

## Status Summary
| Task | Status |
|------|--------|
| AutoML Model Endpoint Creation | ✅ |
| Cloud Run Service Development | ✅ |
| Local Testing and Validation | ✅ |
| Container Registry Integration | ✅ |
| Cloud Run Deployment | ✅ |
| Authentication Configuration | ✅ |
| Health Check Implementation | ✅ |
| Service Testing | ✅ |
| Documentation | ✅ |
| CI/CD Pipeline Integration | ⬜ |

Phase 4 part 1 is now complete with the successful implementation of the Vertex AI endpoint, Cloud Run prediction service, and authenticated access configuration, providing a solid foundation for the prediction capabilities of the Fashion MNIST project.