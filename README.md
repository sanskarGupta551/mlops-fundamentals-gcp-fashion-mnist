# Cloud-Native MLOps Fundamentals on GCP (Fashion-MNIST)

## 📌 Overview

This project was developed as a **hands-on exploration of cloud-native AI engineering and MLOps fundamentals** using the **Fashion-MNIST dataset**. The goal was not to build a production-grade automated ML system, but to gain structured **exposure to core lifecycle stages** — data ingestion, preprocessing, training (AutoML & custom), deployment, and monitoring — by leveraging **Google Cloud Platform (GCP) services**.

---

## 🎯 Objectives

* Learn and apply **MLOps fundamentals** in a **cloud-native environment**.
* Compare **AutoML Vision** baseline vs. **custom CNN training** using TensorFlow.
* Build practical experience with **data pipelines, CI/CD, deployment, and monitoring** on GCP.
* Understand the trade-offs between **managed vs custom approaches** in cloud ML.

---

## 🛠 Tech Stack & Services

* **Programming & Frameworks**: Python, TensorFlow, Docker, Flask
* **Cloud Services**:

  * **Vertex AI** (Workbench, AutoML, Custom Training, Model Registry, Endpoints)
  * **Cloud Run** (serving Flask API)
  * **Cloud Functions** (automated preprocessing pipeline)
  * **Cloud Build** (CI/CD integration with GitHub for serving infrastructure)
  * **Cloud Storage (GCS)** (raw, processed, and model artifacts)
  * **BigQuery** (exploratory data analysis & dataset profiling)
  * **Cloud Monitoring & Logging** (basic observability)

---

## 📂 Project Phases

### **Phase 1: Setup & Infrastructure**

* Created GCP project, billing, cost alerts, IAM service accounts.
* Set up **Vertex AI Workbench** environment and GCS bucket architecture (raw, processed, models).

### **Phase 2: Data Engineering**

* Ingested Fashion-MNIST dataset into **GCS**.
* Conducted exploratory analysis (class distribution, PCA, t-SNE, similarity matrices, outlier detection).
* Built preprocessing pipeline → automated execution via **Cloud Functions** from raw → processed buckets.

### **Phase 3: Model Development**

* Baseline: trained **AutoML Vision model** in Vertex AI (achieved \~97% precision).
* Custom: developed **CNN training pipeline** in TensorFlow, containerized with Docker, submitted to **Vertex AI Custom Training jobs**.
* Compared performance of AutoML vs custom models, and registered models in Vertex AI.

### **Phase 4: Deployment & Monitoring**

* Deployed model to **Vertex AI Endpoint**.
* Wrapped with **Flask API**, containerized, and deployed via **Cloud Run**.
* Set up **CI/CD with GitHub + Cloud Build** for serving infrastructure.
* Added basic monitoring via **Cloud Monitoring & Logging**.

---

## 📊 Results & Learnings

* **AutoML Vision baseline** → achieved \~97% precision.
* **Custom CNN** → enabled more flexibility for experimentation and long-term learning.
* Delivered a **cloud-native ML pipeline** covering ingestion → preprocessing → training → deployment → monitoring.
* Key learning: trade-offs between **fully managed services (faster, simpler)** vs. **custom pipelines (flexible, scalable)**.

---

## 🔮 Future Improvements 

* Extend pipeline to include **automated retraining** triggers.
* Add **feature store integration** for production-scale datasets.
* Enhance monitoring with **drift detection and alerting**.

