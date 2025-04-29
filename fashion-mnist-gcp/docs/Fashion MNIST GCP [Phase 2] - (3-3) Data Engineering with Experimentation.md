# Fashion MNIST GCP [Phase 2]: (3/3) Data Engineering with Experimentation

### Overview
This document details the enterprise-grade data engineering implementation that bridges experimental exploration and production deployment. It demonstrates a methodical approach that begins with interactive experimentation in Jupyter notebooks to validate preprocessing strategies, followed by transformation into robust, production-ready Python modules with comprehensive error handling and optimizations. The implementation incorporates Vertex AI Feature Store to provide consistent feature access across training and serving environments while establishing a sophisticated data augmentation system that enhances model generalization capabilities. This experimental-to-production pathway creates a solid foundation that ensures reproducibility, performance, and maintainability throughout the model development lifecycle.

### Completed Tasks

#### 1. Detailed Data Preprocessing Strategy in Notebooks

The notebook-based processing validation included:

- **Dataset Loading and Initial Exploration**:
  - Leveraged TensorFlow's built-in `fashion_mnist.load_data()` to access the dataset
  - Examined shape characteristics (60,000 training samples, 10,000 test samples)
  - Analyzed data type (uint8) and value range [0-255]
  - Visualized sample images to understand dataset quality and characteristics

- **Data Splitting Implementation**:
  - Utilized `sklearn.model_selection.train_test_split` for reproducible splits
  - Applied stratified sampling to maintain class distribution
  - Created 80/20 train/validation split from the original training data
  - Verified class balance across all splits with distribution counts
  - Preserved the original test set for final evaluation

- **Normalization Process**:
  - Applied Min-Max [0,1] normalization by converting to float32 and dividing by 255
  - Verified normalization effectiveness by examining value ranges
  - Confirmed visual quality of normalized images through side-by-side comparisons
  - Selected normalization approach based on performance with neural networks

- **Augmentation Strategy Development**:
  - Implemented a comprehensive `augment_image` function with multiple transformations:
    - Horizontal flipping (50% probability)
    - Random rotation (±15° with 60% probability)
    - Brightness adjustments (0.8-1.2× factor with 70% probability)
    - Contrast modifications (0.7-1.3× factor with 60% probability)
    - Pixel shifting (±2-3 pixels with 50% probability)
    - Zoom transformations (0.9-1.1× with 40% probability)
  - Calibrated probabilities to ensure diverse yet recognizable augmentations
  - Visualized augmented outputs across multiple image classes
  - Fine-tuned transformation parameters based on visual inspection

- **Mini-Batch Generation Validation**:
  - Created an efficient batch generator with optional augmentation
  - Implemented shuffle mechanism for training data randomization
  - Compared augmented vs. non-augmented batches visually
  - Verified consistent label association after augmentation
  - Tested batch generator performance with different batch sizes

- **End-to-End Pipeline Validation**:
  - Created a complete workflow from raw data to augmented batches
  - Verified data shape consistency throughout the pipeline
  - Conducted systematic visual inspections at each processing stage
  - Confirmed batch generator functionality with both training and validation data
  - Established time and memory benchmarks for pipeline operations

#### 2. Production-Ready Python Module Development

The notebook-validated processes were transformed into a robust, modular Python script with:

- **Object-Oriented Architecture**:
  - `FashionMNISTDataset` class encapsulating dataset management:
    - Constructor parameters for validation split ratio, random seed, and normalization toggle
    - Internal methods for dataset loading and normalization
    - Properties providing access to processed data splits
    - NPZ serialization capability for storing processed data
  
  - `ImageAugmenter` class for configurable image transformations:
    - Fully parameterized initialization for all augmentation parameters
    - Optimized augmentation pipeline with probabilistic transformation application
    - Efficient implementation of geometric and pixel-value transformations
    - Random seed support for reproducible augmentation

  - `DataGenerator` class implementing Python's iterator protocol:
    - Support for both training (with augmentation) and validation (without augmentation) workflows
    - Memory-efficient batch generation
    - Shuffle capability with reproducible random states
    - Support for both finite iteration and infinite generation

- **Production Optimizations**:
  - Removed visualization and analytics code from production module
  - Added comprehensive error handling and logging
  - Streamlined data loading process for efficiency
  - Optimized memory usage during batch generation
  - Improved numerical stability in transformation calculations
  - Fixed edge cases in zoom transformation implementation

- **Integration-Friendly Design**:
  - Utility functions `load_fashion_mnist_dataset`, `create_train_generator`, and `create_val_generator` for simplified usage
  - Clear documentation for integration with training scripts
  - Consistent parameter naming conventions
  - Flexible configuration options for different training scenarios
  - Self-contained implementation requiring minimal dependencies

#### 3. Feature Store Implementation Details

The Vertex AI Feature Store implementation included:

- **Feature Extraction Pipeline**:
  - Created statistical features capturing pixel intensity distributions
  - Implemented edge detection algorithms to extract structural information
  - Applied Principal Component Analysis (PCA) for dimensionality reduction
  - Generated histogram features representing brightness distributions
  - Created metadata features for class information and split designation

- **BigQuery Infrastructure Setup**:
  - Established `fashion_mnist_features` dataset in BigQuery
  - Created two main tables with appropriate schemas:
    - `image_features`: Numerical features extracted from images
    - `metadata_features`: Class labels and identifiers
  - Implemented timestamp-based versioning columns
  - Established entity ID as the primary join key

- **Feature Group Configuration**:
  - Registered feature definitions in Vertex AI Feature Registry
  - Created two feature groups with appropriate schemas:
    - `exp_image_features`: Image-derived numerical features
    - `exp_metadata_features`: Class information and metadata
  - Established entity definitions with image_id as primary key
  - Configured online serving options for inference access

- **Feature Quality Validation**:
  - Verified feature values against source images
  - Confirmed entity ID consistency across feature groups
  - Validated feature retrieval through API calls
  - Tested batch and online serving capabilities

#### 4. Data Normalization Process for Training

To support subsequent model training phases, an additional data preparation task was implemented:

- **Cloud-Based Normalized Dataset Generation**:
  - Created a dedicated normalizer script to process raw dataset files
  - Implemented a systematic workflow to convert uint8 [0-255] images to float32 [0-1] range
  - Preserved original training/validation/test splits during normalization
  - Generated normalized dataset in NPZ format for efficient loading in training jobs
  - Implemented comprehensive logging for process transparency
  - Created detailed documentation of normalized dataset structure and usage patterns
  - Successfully processed and saved normalized dataset to `custom_jobs_normalized` directory
  - Verified data integrity and normalization consistency across all splits

### Technical Implementation Details

#### Data Processing Workflow

The data processing implementation follows a systematic workflow:

1. **Raw Data Acquisition**:
   - Import Fashion MNIST through TensorFlow's datasets API
   - Original 28×28 pixel grayscale images with values [0-255]
   - Training (60,000 samples) and test (10,000 samples) splits
   - Ten balanced classes with 6,000 training samples per class

2. **Preprocessing Pipeline**:
   - Stratified train/validation split (80/20) from original training data
   - Type conversion from uint8 to float32 for numerical stability
   - Min-Max normalization to scale pixel values to [0,1] range
   - Verification of data shapes and value ranges

3. **Augmentation System**:
   - Multiple transformation types with configurable parameters
   - Probabilistic application to ensure diverse outputs
   - Geometric transformations: rotation, flipping, shifting, zooming
   - Pixel-value transformations: brightness, contrast adjustments
   - Preservation of image dimensions after transformations

4. **Batch Generation Process**:
   - Configurable batch size for different hardware capabilities
   - Random shuffling of training data with reproducible seeds
   - Just-in-time augmentation applied only to training data
   - Memory-efficient iterator implementation
   - Support for both epoch-based and infinite generation

5. **Feature Management**:
   - Extraction of statistical, structural, and distribution features
   - Storage in BigQuery with appropriate schema design
   - Registration in Vertex AI Feature Registry with entity definitions
   - Version control through timestamp-based tracking
   - Flexible access mechanisms for both training and serving

### Integration with Training Workflow

The production module enables seamless integration with model training through:

```python
# Example workflow (not included in production module)
from data import FashionMNISTDataset, create_train_generator, create_val_generator

# Load dataset with preprocessing
dataset = FashionMNISTDataset(val_split=0.2, random_state=42, normalize=True)

# Create training generator with augmentation
train_generator = create_train_generator(
    dataset.X_train, dataset.y_train, 
    batch_size=32, 
    augment=True, 
    random_state=42
)

# Create validation generator without augmentation
val_generator = create_val_generator(
    dataset.X_val, dataset.y_val, 
    batch_size=32, 
    random_state=42
)

# Example of integration with TensorFlow/Keras training
model.fit(
    train_generator.generate(),
    steps_per_epoch=len(train_generator),
    validation_data=val_generator.generate(),
    validation_steps=len(val_generator),
    epochs=10
)
```

### Status Summary
| Task | Status |
|------|--------|
| Vertex AI Workbench Setup | ✅ |
| Service Account Creation | ✅ |
| Storage Buckets Creation | ✅ |
| Bucket Configuration | ✅ |
| Network Configuration | ✅ |
| Security Settings | ✅ |
| Monitoring & Health Setup | ✅ |
| Dataset Download | ✅ |
| Data Upload | ✅ |
| Folder Structure | ✅ |
| Raw Data Analysis | ✅ |
| Dataset Ingestion | ✅ |
| Dataset Preparation | ✅ |
| Cloud Storage Organization | ✅ |
| Documentation | ✅ |
| Data Preprocessing Pipeline | ✅ |
| Data Augmentation Strategy | ✅ |
| Notebook-Based Preprocessing Validation | ✅ |
| Feature Engineering | ✅ |
| BigQuery Feature Tables | ✅ |
| Vertex AI Feature Store Implementation | ✅ |
| Production Module Development | ✅ |
| Training Integration Testing | ✅ |
| Normalized Dataset Generation | ✅ |

Phase 2 is now complete with the successful implementation of data processing strategies, feature engineering, Vertex AI Feature Store, and production-ready data processing modules. The project is ready to proceed to Phase 3: Model Development & Training with a solid data foundation that ensures consistency, reproducibility, and performance through both Feature Store capabilities and modular processing components.

### Key Benefits of Implemented Approach

1. **Notebook-to-Production Pathway**:
   - Interactive experimentation and validation in notebooks
   - Clear transition to production-grade code
   - Maintained consistency between development and production
   - Documented decisions and rationale through notebook annotations

2. **Feature Store Advantages**:
   - Centralized feature management reducing redundancy
   - Clear versioning enabling reproducible model development
   - Separation of concerns between feature engineering and model training
   - Consistent feature access across training and serving

3. **Modular Component Design**:
   - Separation of dataset handling, augmentation, and batch generation
   - Flexible configuration for different use cases
   - Clear interfaces enabling integration with various training frameworks
   - Maintainable codebase with well-defined responsibilities

4. **Production-Ready Data Assets**:
   - Multiple data formats supporting different training approaches
   - Normalized datasets ready for immediate model consumption
   - Comprehensive documentation for each data asset
   - Verified data quality across all preparation stages

This comprehensive data engineering foundation will enable efficient model development in the next phase while ensuring consistent evaluation and reproducible results.