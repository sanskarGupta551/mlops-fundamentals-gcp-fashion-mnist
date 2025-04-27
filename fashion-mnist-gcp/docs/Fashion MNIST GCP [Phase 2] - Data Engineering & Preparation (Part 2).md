# Fashion MNIST GCP [Phase 2]: Data Engineering & Preparation (Part 2)

## Phase 2: Data Engineering & Preparation

### Overview
Part 2 of Phase 2 completes the data engineering and preparation tasks, focusing on comprehensive dataset analysis, ingestion, and organization in Cloud Storage buckets.

### Completed Tasks

#### 1. Raw Data Analysis
- Conducted comprehensive analysis using Jupyter notebook in Vertex AI Workbench
- Generated analysis results including:
  - Dataset overview and class distribution
    - 60,000 training samples, 10,000 test samples
    - Perfectly balanced classes (6,000 training, 1,000 test per class)
  - Statistical analysis
    - Global mean: 72.94, standard deviation: 90.02
    - Class-specific statistics showing varying brightness patterns
    - Coat and Pullover have highest mean brightness (98.26, 96.06)
    - Sandal and Sneaker have lowest mean brightness (34.87, 42.76)
  - Visual pattern analysis
    - Generated average images per class
    - Edge detection analysis revealing structural differences
    - Created 10x10 grid of sample images per class
  - Dimensionality analysis
    - PCA: First component explains 29.04% variance
    - Only 1 component needed to explain 95% variance (error in calculation)
    - t-SNE visualization showing clear class clusters
  - Class relationship analysis
    - Similarity matrix using cosine similarity
    - Most similar pairs: Coat-Shirt (98.7%), Pullover-Coat (98.4%)
    - Least similar pairs: Trouser-Sneaker (44.0%), Trouser-Sandal (47.1%)
  - Data quality assessment
    - Only 37 outliers detected (0.06% of dataset)
    - Data range: 0-255
    - No null values
    - Data type: uint8
  - Preprocessing insights
    - Recommended: Min-Max [0,1] normalization
    - Suggested augmentations: rotation (±10°), horizontal flip, brightness (±10%), zoom (0.9-1.1x)
  - Performance predictions
    - Class difficulty ranking: Bag (most difficult) to Sneaker (least difficult)
    - Expected accuracy ranges: 85-90% (simple), 92-95% (complex), 94-97% (ensemble)
  - Comparative analysis with original MNIST
    - Fashion MNIST is 1.06x more complex
    - 1.48x higher edge density
    - Requires deeper CNNs and attention mechanisms

#### 2. Dataset Ingestion and Preparation
- Downloaded Fashion MNIST dataset from TensorFlow
- Prepared data in multiple formats:
  - NumPy arrays for custom training jobs (`.npz` format)
    - Contains X_train, y_train, X_test, y_test arrays
    - Compressed format for efficient storage and loading
  - Individual images with CSV for Vertex AI Datasets
    - JPEG format with 95% quality for optimal storage
    - Train/test images organized by class folders
    - CSV files with GCS paths and labels
    - Separate CSVs for train, test, and combined data
- Created organized directory structure for different use cases
- Generated metadata files:
  - `class_names.json`: List of category names
  - `manifest.json`: Dataset metadata including creation timestamp
  - `README.md`: Comprehensive usage instructions

#### 3. Cloud Storage Organization
- Uploaded analysis results to `fashion-mnist-dev/analysis-results`
  - 26 files including PNG visualizations and JSON analysis outputs
  - Total size: Approximately 5MB
  - Files prefixed numerically for logical ordering
- Uploaded dataset to `fashion-mnist-datasets` with structure:
  ```
  fashion-mnist-datasets/
  ├── custom_jobs/
  │   ├── fashion_mnist.npz
  │   └── class_names.json
  ├── vertex_datasets/
  │   ├── train/
  │   │   ├── T-shirt_top/
  │   │   ├── Trouser/
  │   │   └── ... (all 10 classes)
  │   ├── test/
  │   │   └── ... (all 10 classes)
  │   ├── train.csv
  │   ├── test.csv
  │   └── all_data.csv
  ├── manifest.json
  └── README.md
  ```

#### 4. Documentation and Metadata
- Created comprehensive README for dataset usage
- Generated manifest file with dataset metadata
- Documented file formats and usage instructions
- Included code examples for loading data
- Provided GCS path conventions for Vertex AI import

#### 5. Vertex AI Managed Dataset Creation
- Created managed dataset: `fashion-mnist-managed-dataset`
- Selected dataset type: Single-label classification
- Imported data from Cloud Storage using CSV files
- Used default data split configuration:
  - Random assignment to training, validation, and test sets
  - Preserves the ability for ml_use labels to override random assignments
- Successfully imported 70,000 images across 10 balanced classes
- Dataset ready for AutoML training or custom model development

### Key Findings from Analysis

1. **Dataset Characteristics**:
   - 70,000 total samples (60,000 training, 10,000 test)
   - 28x28 grayscale images (784 dimensions)
   - 10 balanced classes (6,000 samples per class in training)
   - Only 0.06% potential outliers detected
   - High-quality data with consistent formatting

2. **Class Relationships**:
   - Most similar classes: Coat and Shirt (98.7% similarity)
   - Upper body garments cluster together (Coat, Shirt, Pullover, T-shirt/top)
   - Footwear cluster (Sneaker, Sandal, Ankle boot)
   - Most difficult to classify: Bag, Shirt, Pullover
   - Easiest to classify: Sneaker, Trouser

3. **Complexity Analysis**:
   - Fashion MNIST is 1.06x more complex than original MNIST
   - 1.48x higher edge density
   - Requires more sophisticated feature extraction
   - Higher intra-class variability compared to digit recognition

4. **Preprocessing Recommendations**:
   - Use Min-Max [0,1] normalization
   - Apply data augmentation (rotation, flip, brightness, zoom)
   - Expected accuracy: 92-95% with complex models
   - Use deeper CNNs due to complex patterns and textures

5. **Model Architecture Insights**:
   - Recommend deeper CNN architectures
   - Consider attention mechanisms for better feature focus
   - Implement ensemble methods for optimal performance
   - Use data augmentation to improve generalization

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
| Data Preprocessing Pipeline | ⬜ |
| Vertex AI Feature Store Setup | ⬜ |
| Preprocessing Validation | ⬜ |

Phase 2 is in progress, with key infrastructure and initial data preparation completed. The next steps will focus on creating scalable, reproducible data transformation processes and feature management.