"""
Fashion MNIST Dataset Normalizer Cloud Function

This script provides a Cloud Function that normalizes the Fashion MNIST dataset
stored in a GCS bucket and saves the normalized version to another location
in the same bucket.

Trigger: Cloud Storage (finalize/create) or HTTP trigger
"""

import numpy as np
import os
import logging
import tempfile
from google.cloud import storage
import functions_framework
import json
import datetime

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

def download_from_gcs(gcs_path, local_path):
    """Download a file from Google Cloud Storage to local filesystem."""
    # Parse the GCS path
    if not gcs_path.startswith('gs://'):
        raise ValueError(f"Invalid GCS path: {gcs_path}. Must start with 'gs://'")
    
    path_parts = gcs_path[5:].split('/', 1)
    if len(path_parts) < 2:
        raise ValueError(f"Invalid GCS path: {gcs_path}. Must be in format 'gs://bucket/path'")
    
    bucket_name = path_parts[0]
    blob_name = path_parts[1]
    
    # Create a storage client
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    
    # Ensure directory exists
    os.makedirs(os.path.dirname(local_path), exist_ok=True)
    
    # Download the blob
    logger.info(f"Downloading {gcs_path} to {local_path}")
    blob.download_to_filename(local_path)
    logger.info(f"Download complete")

def upload_to_gcs(local_path, gcs_path):
    """Upload a file from local filesystem to Google Cloud Storage."""
    # Parse the GCS path
    if not gcs_path.startswith('gs://'):
        raise ValueError(f"Invalid GCS path: {gcs_path}. Must start with 'gs://'")
    
    path_parts = gcs_path[5:].split('/', 1)
    if len(path_parts) < 2:
        raise ValueError(f"Invalid GCS path: {gcs_path}. Must be in format 'gs://bucket/path'")
    
    bucket_name = path_parts[0]
    blob_name = path_parts[1]
    
    # Create a storage client
    storage_client = storage.Client()
    bucket = storage_client.bucket(bucket_name)
    blob = bucket.blob(blob_name)
    
    # Upload the blob
    logger.info(f"Uploading {local_path} to {gcs_path}")
    blob.upload_from_filename(local_path)
    logger.info(f"Upload complete")

def normalize_dataset(dataset):
    """Normalize dataset by converting to float32 and scaling to [0,1]."""
    logger.info("Normalizing dataset")
    normalized = {}
    
    # Normalize image data (X arrays)
    for key in dataset.keys():
        if key.startswith('X_'):
            # Convert to float32 and normalize to [0,1]
            normalized[key] = dataset[key].astype('float32') / 255.0
            logger.info(f"Normalized {key}: shape={normalized[key].shape}, dtype={normalized[key].dtype}")
        else:
            # Keep labels as they are
            normalized[key] = dataset[key]
            logger.info(f"Kept {key} unchanged: shape={normalized[key].shape}, dtype={normalized[key].dtype}")
    
    return normalized

def normalize_fashion_mnist(input_path, output_path):
    """Main function to normalize Fashion MNIST dataset."""
    # Create temporary directory
    with tempfile.TemporaryDirectory() as temp_dir:
        # Define local paths
        local_input_file = os.path.join(temp_dir, "fashion_mnist.npz")
        local_output_file = os.path.join(temp_dir, "fashion_mnist_normalized.npz")
        
        # Download the dataset
        download_from_gcs(input_path, local_input_file)
        
        # Load the dataset
        logger.info(f"Loading dataset from {local_input_file}")
        dataset = dict(np.load(local_input_file))
        logger.info(f"Dataset loaded with keys: {dataset.keys()}")
        
        # Normalize the dataset
        normalized_dataset = normalize_dataset(dataset)
        
        # Save the normalized dataset locally
        logger.info(f"Saving normalized dataset to {local_output_file}")
        np.savez_compressed(local_output_file, **normalized_dataset)
        
        # Upload to GCS
        gcs_output_file = os.path.join(output_path, "fashion_mnist_normalized.npz")
        upload_to_gcs(local_output_file, gcs_output_file)
        
        # Create and upload class names file if it exists
        class_names_input = input_path.rsplit('/', 1)[0] + "/class_names.json"
        class_names_local = os.path.join(temp_dir, "class_names.json")
        class_names_output = os.path.join(output_path, "class_names.json")
        
        try:
            download_from_gcs(class_names_input, class_names_local)
            upload_to_gcs(class_names_local, class_names_output)
            logger.info(f"Copied class_names.json to {class_names_output}")
        except Exception as e:
            logger.warning(f"Could not copy class_names.json: {e}")
        
        # Create a README file
        readme_local = os.path.join(temp_dir, "README.md")
        readme_content = f"""# Normalized Fashion MNIST Dataset

This directory contains the normalized version of the Fashion MNIST dataset.

## Files
- `fashion_mnist_normalized.npz`: Contains the following arrays:
  - X_train: Training images, normalized to [0,1] range, dtype=float32
  - y_train: Training labels
  - X_val: Validation images, normalized to [0,1] range, dtype=float32
  - y_val: Validation labels
  - X_test: Test images, normalized to [0,1] range, dtype=float32
  - y_test: Test labels

## Usage
```python
import numpy as np

# Load the dataset
data = np.load('fashion_mnist_normalized.npz')

# Access the arrays
X_train = data['X_train']  # Already normalized to [0,1]
y_train = data['y_train']
X_val = data['X_val']      # Already normalized to [0,1]
y_val = data['y_val']
X_test = data['X_test']    # Already normalized to [0,1]
y_test = data['y_test']
```

## Preprocessing
- Data type: float32
- Normalization: Pixel values divided by 255 to scale from [0,255] to [0,1]
- Shape: 28x28 pixels (original dimensions preserved)

Created: {datetime.datetime.now().isoformat()}
"""
        
        with open(readme_local, 'w') as f:
            f.write(readme_content)
        
        # Upload README
        readme_output = os.path.join(output_path, "README.md")
        upload_to_gcs(readme_local, readme_output)
        logger.info(f"Created and uploaded README.md to {readme_output}")
        
        return {
            "status": "success",
            "input_path": input_path,
            "output_path": output_path,
            "normalized_file": gcs_output_file,
            "timestamp": datetime.datetime.now().isoformat()
        }

# HTTP Trigger version
@functions_framework.http
def normalize_http(request):
    """HTTP-triggered function that normalizes Fashion MNIST dataset.
    
    Args:
        request (flask.Request): The request object with JSON payload containing:
            - input_path: GCS path to input .npz file
            - output_path: GCS path for output directory
    
    Returns:
        JSON response with normalization status
    """
    # Parse request
    request_json = request.get_json(silent=True)
    
    if not request_json or 'input_path' not in request_json or 'output_path' not in request_json:
        return json.dumps({
            "status": "error",
            "message": "Request must include input_path and output_path"
        }), 400
    
    input_path = request_json['input_path']
    output_path = request_json['output_path']
    
    try:
        result = normalize_fashion_mnist(input_path, output_path)
        return json.dumps(result), 200
    except Exception as e:
        logger.error(f"Error in normalization: {e}")
        return json.dumps({
            "status": "error",
            "message": str(e)
        }), 500

# GCS Trigger version
@functions_framework.cloud_event
def normalize_gcs(cloud_event):
    """Cloud Storage-triggered function that normalizes Fashion MNIST dataset.
    
    This function is triggered when a file matching the trigger configuration
    is created/finalized in Cloud Storage.
    
    Args:
        cloud_event (CloudEvent): The Cloud Event containing Storage data
    """
    data = cloud_event.data
    
    bucket = data["bucket"]
    name = data["name"]
    
    # Only process NPZ files named fashion_mnist.npz
    if not name.endswith("/fashion_mnist.npz"):
        logger.info(f"Skipping file {name} as it's not fashion_mnist.npz")
        return
    
    # Define input and output paths
    input_path = f"gs://{bucket}/{name}"
    
    # The output path will be the same bucket, but in the _normalized subfolder
    # For example: custom_jobs/fashion_mnist.npz -> custom_jobs_normalized/
    parent_folder = os.path.dirname(name)
    output_folder = f"{parent_folder}_normalized"
    output_path = f"gs://{bucket}/{output_folder}"
    
    logger.info(f"Processing triggered by upload of {input_path}")
    logger.info(f"Output will be saved to {output_path}")
    
    try:
        result = normalize_fashion_mnist(input_path, output_path)
        logger.info(f"Normalization result: {json.dumps(result)}")
    except Exception as e:
        logger.error(f"Error in normalization: {e}")
        raise

# This allows testing the function locally
if __name__ == "__main__":
    # Example paths for testing
    input_path = "gs://fashion-mnist-datasets/custom_jobs/fashion_mnist.npz"
    output_path = "gs://fashion-mnist-datasets/custom_jobs_normalized/"
    
    result = normalize_fashion_mnist(input_path, output_path)
    print(f"Normalization result: {json.dumps(result, indent=2)}")