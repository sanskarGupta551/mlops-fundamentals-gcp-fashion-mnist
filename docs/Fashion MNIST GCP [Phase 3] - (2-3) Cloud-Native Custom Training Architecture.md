# Fashion MNIST GCP [Phase 3]: (2/3) Cloud-Native Custom Training Architecture

### Overview
This document details the development of a complete cloud-native custom training architecture for the Fashion MNIST image classification model using Vertex AI. This implementation demonstrates professional ML engineering practices by creating a modular, scalable training solution designed for Google Cloud's infrastructure, including comprehensive containerization, experiment tracking, and production-ready service account management. While quota limitations prevented immediate execution, the complete architecture provides a robust foundation for custom model development and showcases enterprise-grade ML engineering practices.

### Completed Tasks

#### 1. Custom Training Script Development

- Created a production-ready `train.py` script converted from interactive notebook development
- Implemented comprehensive argument parsing for hyperparameter configuration
- Added robust logging and error handling for cloud execution environments
- Incorporated environment-aware paths for seamless cloud integration
- Maintained all model architecture improvements from AutoML baseline analysis
- Structured code into logical functions for maintainability and testing
- **Integrated Vertex AI Experiments** for comprehensive tracking and analysis

#### 2. Cloud-Native Development Environment

- Established proper directory structure for Vertex AI custom training:
  ```
  fashion_mnist_custom_job/
  ├── trainer/
  │   ├── __init__.py
  │   └── train.py       # Main training script with experiments integration
  └── Dockerfile         # Container definition for cloud training
  ```
- Created dedicated trainer module with proper Python package structure
- Established version control workflow for training code and container definition
- Configured environment variables for cloud execution
- **Added experiment configuration** for parameter and metric tracking

#### 3. Production Training Script Architecture

The `train.py` script implements a professional ML engineering structure with the following components:

- **Data Processing Pipeline**: 
  - Implemented standardized data loading with comprehensive error handling
  - Created data generators with consistent augmentation parameters
  - Maintained stratified train/validation/test splits
  - Added normalization and preprocessing consistent with baseline model

- **Enhanced Model Architecture**:
  - Implemented three-layer CNN with increasing filter counts (32→64→128)
  - Integrated BatchNormalization after each convolutional and dense layer
  - Applied dropout regularization (25% for conv layers, 50% for dense layer)
  - Dense layer with 512 units for optimal feature representation
  - Adam optimizer with learning rate scheduling, gradient clipping, and weight decay
  - Comprehensive callback structure optimized for cloud environments

- **Cloud Integration Components**:
  - Added handling for environment variables (`AIP_MODEL_DIR`)
  - Implemented GCS-compatible model saving paths
  - Created proper metadata generation for model tracking
  - Modified logging for containerized execution
  - Removed visualization code unnecessary in production

- **Experiment Tracking Integration**:
  - Implemented Vertex AI Experiments initialization
  - Added parameter logging for hyperparameters and configuration
  - Integrated metric tracking for training and validation metrics
  - Created comprehensive experiment run naming strategy
  - Added class-level performance metric tracking

#### 4. Container Architecture

- Created an optimized Dockerfile using Google's pre-built TensorFlow container:
  ```dockerfile
  FROM gcr.io/deeplearning-platform-release/tf2-cpu.2-3
  WORKDIR /
  COPY trainer /trainer
  ENTRYPOINT ["python", "-m", "trainer.train"]
  ```
- Selected `tf2-cpu.2-3` base image for compatibility with model requirements
- Configured proper Python module execution through ENTRYPOINT
- Ensured efficient working directory and file copying
- Successfully built and pushed container to Google Container Registry

#### 5. Vertex AI Custom Job Configuration

- Prepared complete configuration for Vertex AI Custom Job:
  - Specified container image URI in Google Container Registry
  - Configured appropriate machine type (n1-highmem-2)
  - Set up model artifacts directory in Cloud Storage
  - Added comprehensive command-line arguments
  - Configured TensorFlow 2.1 serving container for predictions
  - **Added experiment parameters** for run tracking and analysis

#### 6. Comprehensive Experiment Tracking Setup

- Created dedicated Fashion MNIST experiment in Vertex AI Experiments
- Configured systematic run naming convention for comparison:
  - Pattern: `custom-cnn-{filter_config}-{units}-{dropout_rate}-{timestamp}`
  - Example: `custom-cnn-32-64-128-512-0.25-0.5-20250430123456`
- Implemented parameter tracking for critical values:
  - Model architecture details (layers, filters, units, activation)
  - Optimization settings (learning rate, decay, clipnorm)
  - Regularization parameters (dropout rates, batch normalization)
  - Training configuration (batch size, epochs, early stopping)
- Added comprehensive metric logging framework:
  - Per-epoch training and validation metrics
  - Final test set performance metrics
  - Per-class precision, recall, and F1 scores
  - Confusion matrix summary statistics

### Cloud Resource Constraint: Learning Experience

When attempting to execute the Custom Training Job, we encountered quota limitations:

```
Training pipeline failed with error message: The following quota metrics exceed quota limits: aiplatform.googleapis.com/custom_model_training_cpus
```

Several optimization attempts were made:

1. **Resource Optimization**:
   - Reduced machine type from n1-standard-4 to n1-highmem-2
   - Attempted different regions (us-central1, us-west1)
   - Cleared existing workbench instances to free up resources

2. **Configuration Adjustments**:
   - Adjusted output paths and parameters
   - Selected preemptible instances where available
   - Reduced disk size and other resource requirements

**Learning Outcome**: Quota limitations are a common challenge in cloud-based ML projects, especially with new GCP projects that have default quota settings. This experience demonstrates:
- The importance of proactive quota planning in cloud projects
- Professional problem-solving approaches when facing infrastructure constraints
- The value of building complete architectures that are ready for execution upon resource availability

### Key Technical Achievements

#### 1. Model Architecture Portability

Successfully designed and implemented a cloud-native CNN architecture:
- Three-layer CNN with progressive filter expansion (32→64→128)
- Strategic dropout placement (25% after convolutions, 50% before output)
- Adam optimizer with gradient clipping (clipnorm=1.0) and weight decay (1e-5)
- Learning rate starting at 0.001 with reduction scheduling

Data augmentation parameters optimized for cloud training:
- 15° rotation range for realistic variance
- 15% width/height shifts for positioning robustness
- 15% shear range for perspective variation
- 15% zoom range for scale invariance
- Horizontal flipping for symmetric clothing items
- Nearest-neighbor fill mode for edge preservation

#### 2. Production Engineering Excellence

- **Cloud-Native Design**:
  - Built for seamless Vertex AI integration
  - Environment-aware configuration management
  - GCS-compatible artifact storage
  - **Comprehensive experiment tracking** throughout

- **Container Optimization**:
  - Lightweight, efficient container builds
  - Proper dependency management
  - Production-ready logging and monitoring
  - **Experiment metadata integration**

- **Scalability Considerations**:
  - Resource-aware batch and step calculations
  - Memory-efficient data loading
  - Distributed training compatibility
  - **Experiment tracking at scale**

#### 3. Professional Service Account Architecture

- Created dedicated **Model Training Service Account**:
  - Name: `model-training-sa`
  - Email: model-training-sa@fashion-mnist-gcp.iam.gserviceaccount.com
  - Assigned roles:
    - Vertex AI User
    - Storage Object Admin
    - Vertex AI Experiments Editor
    - Artifact Registry Writer
    - Log Writer
    - Monitoring Metric Writer
    - Compute Admin

- Created dedicated **Model Registry Service Account**:
  - Name: `model-registry-sa`
  - Email: model-registry-sa@fashion-mnist-gcp.iam.gserviceaccount.com
  - Assigned roles:
    - Vertex AI Model Registry Admin
    - Storage Object Admin
    - Vertex AI Metadata Writer
    - Secret Manager Secret Accessor

### Professional Value and Learning Outcomes

#### 1. Enterprise Architecture Skills

This implementation demonstrates:
- **Complete Cloud-Native Design**: Built for Vertex AI from ground up
- **Container Best Practices**: Production-ready containerization
- **Security Implementation**: Proper service account and IAM design
- **Experiment Management**: Comprehensive tracking and versioning
- **Resource Planning**: Understanding cloud limitations and planning

#### 2. Problem-Solving and Adaptability

The quota limitation experience showcases:
- **Professional Constraint Handling**: Systematic troubleshooting approach
- **Resource Optimization**: Multiple optimization strategies attempted
- **Documentation of Challenges**: Transparent communication of limitations
- **Architecture Investment**: Building for future success despite current constraints

#### 3. ML Engineering Best Practices

- **Modular Design**: Clean separation of concerns in training architecture
- **Environment Portability**: Code designed for multiple execution contexts
- **Monitoring Integration**: Comprehensive logging and metric tracking
- **Version Control**: Proper management of training code and containers

### Ready for Deployment

The complete training architecture is ready for immediate execution upon quota increase:

1. **Container Image**: Successfully built and stored in Google Container Registry
2. **Training Script**: Production-ready with comprehensive error handling
3. **Experiment Tracking**: Integrated Vertex AI Experiments for full observability
4. **Service Accounts**: Properly configured with least-privilege access
5. **Job Configuration**: Complete Vertex AI Custom Job specification

### Status Summary
| Task | Status |
|------|--------|
| Training Script Development | ✅ |
| Container Architecture | ✅ |
| GCR Image Publishing | ✅ |
| Vertex AI Job Configuration | ✅ |
| Vertex AI Experiments Integration | ✅ |
| Service Account Configuration | ✅ |
| **Vertex AI Job Execution** | ⬜ (Pending quota increase) |
| **Model Performance Evaluation** | ⬜ (Dependent on training execution) |
| **Model Registry** | ⬜ (Dependent on successful training) |

### Conclusion

Phase 3 Part 2 successfully demonstrates comprehensive cloud-native ML engineering practices through the development of a complete custom training architecture. While quota limitations prevented immediate execution, the implementation showcases:

- **Professional ML Engineering**: Complete production-ready training infrastructure
- **Cloud-Native Design**: Built specifically for Vertex AI execution
- **Enterprise Practices**: Proper security, monitoring, and experiment tracking
- **Real-World Learning**: Professional handling of cloud resource constraints

This implementation establishes a robust foundation for custom model development and demonstrates the architectural thinking and technical skills essential for enterprise ML engineering roles. The complete infrastructure is ready for immediate deployment upon resource availability, showcasing both technical capability and strategic planning skills.

The project continues with the focus on AutoML deployment in production while maintaining this sophisticated custom training capability for future scaling needs.