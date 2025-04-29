# Fashion MNIST GCP [Phase 3]: (1/3) AutoML Baseline Model Development

### Overview
This document details the implementation of a baseline image classification model for the Fashion MNIST dataset using Vertex AI AutoML. It demonstrates a systematic approach to leveraging Google Cloud's managed ML services for establishing robust model benchmarks with minimal engineering overhead. The implementation focuses on effective model training configuration, comprehensive performance evaluation, and insightful analysis of classification patterns. This baseline model provides a strong reference point for subsequent custom model development while validating the data analysis and preprocessing performed in Phase 2.

### Completed Tasks

#### 1. AutoML Training Configuration
- Successfully configured and initiated AutoML Vision training:
  - Model name: `fashion-mnist-automl-baseline-model`
  - Dataset: `fashion-mnist-managed-dataset` (70,000 images, 10 classes)
  - Training objective: Image classification (single-label)
  - Model optimization: Higher accuracy option (200-300ms latency)
  - Node hours budget: 8 hours maximum
  - Training completed on: April 29, 2025 3:30:58 AM
  - Total training time: ~1 hour

- Data split configuration:
  - Training: 80% (56,121 images)
  - Validation: 10% (7,097 images)
  - Test: 10% (6,782 images)
  - Method: Random split with stratification
  - No additional data augmentation applied (using AutoML defaults)

- Storage and encryption:
  - Google-managed encryption key
  - No CMEK implementation required for baseline
  - Model artifacts stored in us-central1 region

#### 2. Model Performance Evaluation
- Overall performance metrics:
  - Average precision: 0.972 (97.2%)
  - Global precision: 93.9% 
  - Global recall: 89.1%

- Per-class performance analysis:
  | Class | Precision | Correct Predictions | Confusion Areas |
  |-------|-----------|---------------------|-----------------|
  | Sandal | 0.999 | 98% | Ankle_boot (1%) |
  | Trouser | 0.998 | 98% | Dress (1%) |
  | Bag | 0.997 | 100% | None significant |
  | Ankle_boot | 0.993 | 96% | Sneaker (3%) |
  | Sneaker | 0.991 | 97% | Ankle_boot (2%) |
  | Dress | 0.968 | 91% | Coat (4%), Bag (3%) |
  | Pullover | 0.948 | 92% | Coat (2%), Dress (2%) |
  | T-shirt_top | 0.940 | 92% | Bag (4%), Shirt (1%) |
  | Coat | 0.934 | 86% | Shirt (5%), Pullover (6%) |
  | Shirt | 0.864 | 66% | Coat (17%), T-shirt_top (1%), Pullover (6%) |

- Precision-recall characteristics:
  - Precision-recall curve shows consistently high performance across most threshold values
  - Slight precision drop observed only at very high recall requirements (>95%)
  - Current confidence threshold set at 0.5 (default)
  - F1-score optimal near default threshold

- Confusion matrix insights:
  - Primary confusion clusters:
    - Upper body garments: Shirt-Coat-Pullover-T-shirt_top exhibit highest inter-class confusion
    - Footwear: Minimal confusion between Ankle_boot-Sneaker-Sandal
    - Dress occasionally confused with Coat and T-shirt_top
  - Shirt class represents the most challenging classification with only 66% correct predictions
  - Most confident classifications: Bag (100%), Trouser (98%), Sandal (98%)

#### 3. Analysis and Key Findings
- Validation of data engineering insights:
  - The confusion patterns directly correlate with similarity analysis from Phase 2
  - Predicted challenging classes (Shirt, Coat, Pullover) confirmed by model performance
  - Edge and texture features indeed crucial for discriminating upper body garments
  - Class separability matches PCA and t-SNE visualizations from Phase 2

- Performance exceeds expectations:
  - Average precision (97.2%) surpasses projected range for simple models (85-90%)
  - Results approach upper bound of complex model projections (92-95%)
  - AutoML optimization demonstrates higher ceiling than initially anticipated

- Error pattern analysis:
  - Misclassifications primarily structural rather than random
  - Visual similarity directly correlates with confusion probability
  - Confusion occurs primarily within semantically related categories
  - No significant anomalies or unexpected classification patterns detected

- Architecture insights (from AutoML metrics):
  - Model shows greater focus on local texture features over global shape
  - Decision boundaries most robust for categories with distinctive texture patterns
  - Possible evidence of attention mechanisms in AutoML architecture

#### 4. Model Artifacts and Documentation
- Model registration:
  - Successfully registered in Vertex AI Model Registry
  - Model ID: `automl-97239`
  - Region: us-central1 (Iowa)
  - Model type: AutoML Image Classification
  - Creation timestamp: April 29, 2025, 3:31:23 AM
  - Versioning: Initial version (1.0)

- Artifact storage:
  - Evaluation metrics stored in GCS bucket: `fashion-mnist-model`
  - Confusion matrices exported in both percentage and count formats
  - Precision-recall curves saved as vector graphics
  - Complete evaluation report archived with timestamp

- Documentation:
  - Model card created with:
    - Training configuration details
    - Performance metrics
    - Known limitations
    - Intended use guidelines
    - Fairness considerations

### Key Decisions Made

1. **AutoML vs. Custom Initial Approach**:
   - Selected AutoML for baseline due to rapid development capability
   - Strong performance validates dataset quality and preprocessing
   - Provides benchmark metrics to inform custom architecture design

2. **Higher Accuracy Optimization**:
   - Prioritized model accuracy over lower latency
   - Acceptable inference time (200-300ms) for non-real-time applications
   - Provides upper bound on expected performance for custom models

3. **No Deployment or Additional Testing**:
   - Intentionally limited to model development and evaluation
   - Deployment deferred to dedicated deployment phase
   - Focus on analysis to inform custom model development

4. **Confidence Threshold Retention**:
   - Maintained default 0.5 confidence threshold
   - Precision-recall analysis confirms appropriateness
   - Provides consistent comparison basis for future models

5. **Evaluation Focus**:
   - Emphasized per-class performance over aggregate metrics
   - Detailed confusion analysis to identify improvement opportunities
   - Special attention to challenging class relationships

### Status Summary
| Task | Status |
|------|--------|
| AutoML Configuration | ✅ |
| Training Execution | ✅ |
| Performance Evaluation | ✅ |
| Confusion Matrix Analysis | ✅ |
| Model Registration | ✅ |
| Documentation | ✅ |
| Per-Class Analysis | ✅ |
| Performance Visualization | ✅ |
| Deployment | ⬜ (Deferred) |
| Online Testing | ⬜ (Deferred) |

Phase 3 is in progress, with the AutoML baseline model successfully completed. The results demonstrate excellent performance and provide valuable insights for custom model development in the next steps. The high baseline accuracy (97.2% average precision) sets a challenging benchmark while validating the effectiveness of the data preparation from Phase 2.