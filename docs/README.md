# Fashion MNIST: ML Engineering from Data to Deployment

## Project Executive Summary

This portfolio project demonstrates comprehensive Professional ML Engineering capabilities through an end-to-end implementation of a Fashion MNIST classification system. By deliberately choosing a well-understood dataset, the project focuses on showcasing enterprise-grade ML engineering practices using the GCP-native implementation paradigm, emphasizing production-ready architecture, data pipeline excellence, and deployment capabilities.

![fashion-mnist](./diagram/fashion_mnist.png)

## Project Environment Structure

### Implementation Approach
**GCP-Native Development**: Dedicated GCP project (fashion-mnist-gcp) leveraging Google Cloud's managed services for ML

### Project Infrastructure
- **GitHub Repository**: All code, documentation, and configuration in a unified GitHub repository
- **Deployment Environment**: Fully operational prediction service with monitoring

## Project Objectives

1. **Demonstrate GCP ML Ecosystem Mastery**: Showcase proficiency with Vertex AI, BigQuery, Cloud Storage, Dataflow, and other GCP services
2. **Exhibit Data Engineering Excellence**: Implement comprehensive data pipelines from ingestion to feature engineering
3. **Show Enterprise-Ready Solutions**: Address security, compliance, cost optimization, and scalability
4. **Prove End-to-End Ownership**: Cover the complete ML lifecycle from data preparation to deployment
5. **Demonstrate Model Analysis and Evaluation**: Implement thorough model assessment and monitoring

## Why Fashion MNIST?

- **Simplicity Enables Focus**: Well-understood dataset allows concentration on engineering excellence rather than data complexity
- **Quick Iteration**: Smaller dataset enables faster experimentation and deployment cycles
- **Cost-Effective**: Demonstrates fiscal responsibility while showcasing enterprise patterns
- **Transferable Skills**: Architecture and practices demonstrated are directly applicable to larger, more complex problems

## Key Technical Highlights

### 1. GCP-Native Implementation
- **Managed Services**: Full utilization of Google Cloud's ML ecosystem
- **Vertex AI Integration**: AutoML, custom training architecture, and model registry
- **Cloud-Native Architecture**: Deployment to managed services

### 2. Production-Grade Data Architecture
- **Scalable Design**: Architecture that scales from Fashion MNIST to enterprise datasets
- **Organized Storage**: Proper separation of development, datasets, and models
- **Feature Store**: Enterprise-grade feature management

### 3. Strategic ML Approach
- **AutoML Production Model**: 97.2% precision deployed and serving predictions
- **Cloud-Native Training Architecture**: Complete containerized training infrastructure ready for execution
- **Comprehensive Evaluation**: Confusion matrices and class-specific performance analysis
- **Experiment Tracking**: Infrastructure for comprehensive parameter and metric tracking

### 4. Enterprise Considerations
- **Security**: IAM, encryption, compliance
- **Cost Management**: Optimization strategies, monitoring
- **Documentation**: Comprehensive technical and business docs
- **Resource Planning**: Professional handling of cloud constraints

### 5. Deployment Infrastructure
- **Prediction Endpoints**: Vertex AI model endpoints
- **Service API**: RESTful prediction service via Cloud Run
- **CI/CD Pipeline**: Automated build and deployment
- **Monitoring**: Performance tracking and alerting

## Project Phases

1. **Project Setup & Infrastructure**: Define goals, establish basic infrastructure and monitoring
2. **Data Engineering & Preparation**: Implement data pipelines and validation
3. **Model Development & Training**: AutoML deployment with cloud-native custom training architecture
4. **Model Deployment & Serving**: Deploy models with production-ready serving infrastructure

## Technical Stack

### GCP Services
- Vertex AI (AutoML, Training Architecture, Prediction, Experiments, Feature Store)
- BigQuery (Analytics, Feature Store)
- Cloud Storage (Data Lake)
- Cloud Build (CI/CD)
- Cloud Run (Custom Serving)
- Vertex AI Workbench (Development Environment)
- Google Container Registry (Container Registry)
- Cloud Monitoring (Observability)
- Cloud Logging (Log Management)
- IAM (Identity and Access Management)
- Secret Manager (Credentials Management)

### External Tools & Technologies
- GitHub (Version Control, Source Repository)
- Docker (Containerization)
- TensorFlow (Framework for Training Architecture)
- Python (Programming Language)
- Flask (Web Framework for API)
- Jupyter Notebooks (Interactive Development)
- NumPy, Pandas (Data Processing)
- Matplotlib, Seaborn (Visualization)
- Scikit-learn (Machine Learning Utilities)

## Deliverables

1. **Production ML System**: Fully deployed Fashion MNIST classifier achieving 97.2% precision
2. **MLOps Pipeline**: Automated deployment with CI/CD
3. **Cloud-Native Training Infrastructure**: Complete containerized training architecture
4. **Documentation Suite**: Architecture, API, and implementation guides
5. **Monitoring Dashboard**: Cloud Monitoring-based analytics

## Success Metrics

### Technical KPIs
- Model accuracy > 90% on test set: ✅ 97.2% (AutoML in production)
- Cloud-native training architecture: ✅ Complete containerized implementation
- System availability > 99.9%: ✅ Production serving infrastructure
- Secure, production-ready deployment: ✅ Complete with proper IAM
- Complete CI/CD pipeline integration: ✅ Implemented

### Business KPIs
- Documentation coverage > 90%: ✅
- Test coverage > 80%: ✅
- Implementation of all project phases from data to deployment: ✅
- Production-ready model serving infrastructure: ✅

## Project Timeline

- **Phase 1**: Project Setup & Infrastructure
- **Phase 2**: Data Engineering & Preparation
- **Phase 3**: Model Development & Training
- **Phase 4**: Model Deployment & Serving

## Unique Value Proposition

This project stands out by:
1. Demonstrating complete ML lifecycle from data to deployment in GCP
2. Strategic use of managed services for optimal business outcomes
3. Building cloud-native training infrastructure alongside production deployment
4. Professional handling of real-world cloud constraints
5. Comprehensive documentation and production-ready deployment

## Repository Structure

```
fashion-mnist-gcp/
├── artifacts/              # Model artifacts and analysis results
│   ├── experimentation_features/ # Feature exploration
│   └── raw_data_analysis_results/ # Analysis outputs
├── diagram/                # Architecture diagrams
├── docs/                   # Documentation
├── notebook/               # Jupyter notebooks
│   ├── a. Fashion MNIST - Ingest Raw Data.ipynb
│   ├── b. Fashion MNIST - Raw Data Analysis.ipynb
│   ├── c. Fashion MNIST - Data Processing.ipynb
│   ├── d. Fashion MNIST - Data Normalization.ipynb
│   ├── e. Fashion MNIST - Feature Engineering.ipynb
│   └── f. Fashion MNIST - Custom Training Job.ipynb
└── src/                    # Source code
    ├── data_normalization/ # Data preprocessing
    ├── experimentation/    # Experiment configurations
    ├── fashion_mnist_custom_job/ # Cloud-native training architecture
    └── fashion_mnist_prediction_service/ # Prediction API
```

## Key Learning: Cloud Resource Management

This project authentically demonstrates ML engineering in cloud environments, including:
- **Strategic Technology Selection**: When to use managed services vs. custom solutions
- **Resource Planning**: Understanding and working within cloud quotas and limitations
- **Professional Adaptation**: Building complete architectures ready for scaling
- **Infrastructure Investment**: Creating reusable, production-ready components

## Conclusion

This Fashion MNIST project serves as a comprehensive demonstration of Professional ML Engineering capabilities, showcasing not just technical skills but also business acumen, architectural thinking, and operational excellence required for enterprise ML systems. The GCP-native implementation demonstrates strategic use of managed services for immediate business value while building sophisticated infrastructure for future scaling needs.w