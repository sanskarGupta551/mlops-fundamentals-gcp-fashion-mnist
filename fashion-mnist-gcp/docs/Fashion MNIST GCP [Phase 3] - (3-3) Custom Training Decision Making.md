# Fashion MNIST GCP [Phase 3]: (3/3) Custom Training Decision Making

### Overview
This document outlines the critical architectural decisions, implementation details, and technical considerations made during the development of the custom CNN model for Fashion MNIST classification. It complements the previous implementation documentation by focusing on the rationale behind key technical choices, the structured approach to model registry management, and lessons learned throughout the process. These insights demonstrate professional ML engineering practices that balance model performance with production deployment considerations.

## 1. Model Architecture Design

### CNN Architecture Selection

The custom model implements a carefully designed convolutional neural network with the following architecture:

```
Input (28×28×1)
↓
Conv2D (32 filters, 3×3 kernel, ReLU) → BatchNorm → MaxPooling (2×2) → Dropout (0.25)
↓
Conv2D (64 filters, 3×3 kernel, ReLU) → BatchNorm → MaxPooling (2×2) → Dropout (0.25)
↓
Conv2D (128 filters, 3×3 kernel, ReLU) → BatchNorm → MaxPooling (2×2) → Dropout (0.25)
↓
Flatten
↓
Dense (128 units, ReLU) → BatchNorm → Dropout (0.5)
↓
Dense (10 units, Softmax)
```

### Architecture Decision Rationale

1. **Progressive Filter Expansion (32→64→128)**
   - Enables hierarchical feature learning
   - Initial layers capture basic edges and textures
   - Middle layers detect pattern combinations
   - Final convolutional layer captures complex features and class-specific attributes
   - Balances expressivity with model size

2. **Regularization Strategy**
   - BatchNormalization after each convolutional and dense layer stabilizes training
   - Dropout rates strategically implemented:
     - 25% dropout after convolutional blocks prevents co-adaptation of feature detectors
     - Higher 50% dropout before output prevents overfitting in dense layers
   - MaxPooling reduces spatial dimensions and provides translation invariance

3. **Small Kernel Size (3×3)**
   - Optimal for capturing localized patterns in small 28×28 images
   - Reduces parameter count while maintaining representational power
   - Follows proven CNN architectural patterns from VGG and similar networks

4. **Activation Functions**
   - ReLU activations in hidden layers for non-linearity without vanishing gradient issues
   - Softmax in output layer for proper probability distribution across 10 classes

5. **Network Depth Considerations**
   - Three convolutional blocks provide sufficient depth for Fashion MNIST complexity
   - Additional layers would risk overfitting on this dataset size
   - Final architecture balances expressivity with generalization

## 2. Hyperparameter Selection

### Training Hyperparameters

| Parameter | Value | Rationale |
|-----------|-------|-----------|
| Batch Size | 32 | Provides stable gradient estimates while fitting in memory constraints |
| Learning Rate | 0.001 | Standard starting point for Adam optimizer |
| Epochs | 50 (max) | Sufficient for convergence with early stopping |
| Optimizer | Adam | Adaptive learning rates handle varying gradient magnitudes |
| Loss Function | Categorical Cross-Entropy | Appropriate for multi-class classification |

### Learning Rate Strategy

- **Initial Rate**: 0.001 (standard for Adam)
- **Reduction Strategy**: ReduceLROnPlateau
  - Factor: 0.2 (reduces by 80% when triggered)
  - Patience: 3 epochs
  - Monitoring: validation_loss
  - Min learning rate: 1e-6
- **Rationale**: Allows aggressive initial learning with adaptive reduction when progress plateaus

### Early Stopping Configuration

- **Patience**: 10 epochs
- **Monitor**: validation_loss
- **Restore Best Weights**: True
- **Rationale**: Prevents overfitting while ensuring sufficient opportunity for convergence

### Data Augmentation Parameters

Augmentation parameters were carefully calibrated for fashion item recognition:

| Transformation | Parameters | Rationale |
|----------------|------------|-----------|
| Rotation | ±15° | Accommodates natural image capture variance without distorting key features |
| Width/Height Shift | 15% | Simulates positioning variance while preserving garment structure |
| Shear Range | 15% | Adds realistic perspective distortion |
| Zoom Range | 15% | Simulates minor distance variations |
| Horizontal Flip | True | Valid for symmetric clothing items |
| Fill Mode | Nearest | Preserves edge characteristics important for classification |

## 3. Model Registry Implementation

### Registry Structure

The model registry implementation follows a hierarchical organization strategy:

```
Vertex AI Model Registry
└── fashion-mnist-models (Registry)
    ├── automl-baseline
    │   └── v1 (Initial AutoML model)
    └── custom-cnn
        └── v1 (Initial custom CNN implementation)
```

### Versioning Strategy

- **Semantic Versioning**: Major.Minor.Patch format
  - Major: Significant architecture changes
  - Minor: Hyperparameter modifications
  - Patch: Bug fixes or minor optimizations
- **Immutable Versions**: Each version represents a specific model state
- **Latest Tag**: Dynamically points to most recent production-ready version

### Metadata and Tagging

Custom metadata attached to models:

1. **Performance Metrics**:
   - Accuracy (training, validation, test)
   - F1-score (weighted, per class)
   - Confusion matrix reference
   - Inference latency

2. **Training Context**:
   - Dataset version used
   - Training environment (local vs. cloud)
   - Creation timestamp
   - Training duration

3. **Implementation Details**:
   - Framework version
   - Container reference
   - Data preprocessing steps
   - Resource requirements

4. **Environment Tags**:
   - `stage:dev` or `stage:prod`
   - `approved:yes` or `approved:no`
   - `deployment:eligible` or `deployment:ineligible`

### Model Artifact Organization

```
gs://fashion-mnist-model/
├── automl/
│   └── [AutoML model artifacts]
└── custom_model/
    ├── v1/
    │   ├── saved_model.pb
    │   ├── variables/
    │   ├── assets/
    │   └── metadata/
    │       ├── model_card.md
    │       ├── metrics.json
    │       ├── params.json
    │       └── confusion_matrix.png
    └── [future versions]
```

### Registry Access Patterns

- **Service Account Integration**:
   - Model serving uses dedicated `model-serving` service account
   - Training pipeline uses `model-training` service account
   - Each has appropriate IAM permissions for their function

- **Cross-Project Access**:
   - Models shareable across GCP projects via IAM
   - Enables separation of development and production environments

## 4. Lessons Learned & Best Practices

### Technical Insights

1. **AutoML vs. Custom Tradeoffs**:
   - AutoML provided stronger out-of-box performance (97.2% vs 91.3%)
   - Custom model offers greater architectural control and interpretability
   - AutoML development time was 80% less than custom implementation
   - Custom approach provided valuable learning opportunities and flexibility

2. **Development Workflow Optimization**:
   - Notebook-to-production pathway crucial for maintaining quality
   - Modular code structure with clear separation of concerns enables easier maintenance
   - Proper version control of training scripts is as important as model versioning
   - Docker containerization eliminates environment inconsistencies

3. **Infrastructure Challenges**:
   - Quota limitations common in new GCP projects
   - Service account management requires careful planning
   - GCS path conventions need standardization for consistency
   - Container optimization significantly impacts training performance

### Best Practices Identified

1. **Model Training**:
   - Validate data pipeline before extensive model training
   - Start with simpler architectures before adding complexity
   - Maintain consistent evaluation metrics across model types
   - Log hyperparameters and configurations for reproducibility

2. **Container Optimization**:
   - Use Google's pre-built ML containers when possible
   - Create multi-stage Docker builds for smaller production images
   - Include only necessary dependencies
   - Implement effective caching strategies

3. **Vertex AI Integration**:
   - Standardize artifact paths for consistent access
   - Create dedicated service accounts with least privilege
   - Implement cloud-agnostic fallback strategies
   - Design for both local and cloud execution

4. **Resource Management**:
   - Request quota increases before starting significant development
   - Implement cost controls and budgeting early
   - Use preemptible instances for development and experimentation
   - Match instance type to workload characteristics

### Recommendations for Future Implementation

1. **Architecture Improvements**:
   - Consider residual connections for deeper networks
   - Evaluate attention mechanisms for challenging class pairs
   - Test alternative normalization strategies (GroupNorm vs. BatchNorm)
   - Explore knowledge distillation from AutoML to custom model

2. **Pipeline Optimization**:
   - Implement more sophisticated augmentation techniques
   - Create dedicated preprocessing service for improved inference
   - Develop comprehensive integration testing for data pipeline
   - Establish automated data quality monitoring

3. **Hyperparameter Tuning**:
   - Priority parameters for tuning:
     - Learning rate schedule
     - Dropout rates
     - Filter counts
     - Data augmentation intensity
   - Consider Bayesian optimization approaches for efficient tuning
   - Implement warm-starting for accelerated tuning

## Conclusion

The Phase 3 implementation successfully established both AutoML and custom model approaches for Fashion MNIST classification. The architectural decisions, hyperparameter selections, and implementation strategies demonstrate professional ML engineering practices that balance model performance with production considerations. While quota limitations presented challenges, the flexible implementation approach showcased problem-solving skills essential for real-world ML projects. The established model registry and documented learnings provide a solid foundation for subsequent phases of the project, including evaluation, deployment, and monitoring.

This custom training implementation completes the model development phase of the project, setting the stage for comprehensive model evaluation and deployment in the following phases. The infrastructure and registry patterns established here will enable effective MLOps practices throughout the model lifecycle.