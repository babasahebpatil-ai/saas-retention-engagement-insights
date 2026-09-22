# Replication Package: User Engagement-Based Institutional Churn Analysis in Educational SaaS: An End-to-End Business Analytics and Lakehouse Approach

This repository contains the processed dataset and implementation code for the research study investigating institutional customer churn within a B2B Educational SaaS platform (AIO Class).

---

## 📂 Repository Contents

1. **`Churn Prediction Dataset-2026-08-02.csv`**
   * Anonymized Gold-layer dataset containing institution-level operational metrics and binary churn labels.
2. **`Churn Prediction Model - Random Forest Balanced.ipynb`**
   * Databricks Jupyter Notebook containing the full machine learning pipeline, including data loading, class-weight-adjusted Random Forest training, evaluation metrics, and MLflow experiment tracking.

---

## 📊 Dataset Description (`Churn Prediction Dataset`)

The dataset comprises **1,083 institutions** aggregated using a temporal split (observation window ending before May 1, 2026) to prevent data leakage. Each row represents a single educational institution characterized by the following variables:

* **`institution_id`**: Unique anonymized identifier for each customer institution.
* **`attendance_count`**: Total attendance tracking events recorded within the observation window.
* **`material_count`**: Total learning materials published or accessed.
* **`assessment_count`**: Total assessments created.
* **`teacher_count`**: Total active teachers/staff members.
* **`student_count`**: Total registered students.
* **`class_count`**: Total active classes.
* **`engagement_score`**: Normalized composite score reflecting learning intensity relative to institutional scale.
* **`churn_label`**: Binary target variable (`0` = Active, `1` = Churned based on future inactivity rules).

---

## 🛠️ Requirements & Environment

To run the replication code in Databricks or a local Python environment, ensure the following libraries are installed:
* `pandas` >= 2.0
* `numpy` >= 1.20
* `scikit-learn` >= 1.2
* `mlflow` >= 2.0
* `matplotlib` >= 3.5
* `seaborn` >= 0.11

---

## 🚀 How to Run the Replication Code

1. Upload `Churn Prediction Dataset-2026-08-02.csv` into your Databricks Workspace Volume (or local directory).
2. Open the `Churn Prediction Model - Random Forest Balanced.ipynb` notebook.
3. Update the `data_path` variable to point to your storage volume path.
4. Run all cells sequentially to reproduce the exploratory data analysis, feature correlations, stratified train-test splitting (80/20), model training (`class_weight='balanced'`), and evaluation metrics (Accuracy, Precision, Recall, F1-Score, ROC-AUC, PR-AUC).

---

## 🔒 Data Availability Statement

Due to commercial confidentiality and data privacy agreements with **CV Smart Edutek Solusi** (owner of the AIO Class platform), raw transactional tables (containing personal/sensitive operational logs) are restricted. However, the processed, anonymized **Gold-layer analytical dataset** and replication scripts are made publicly available via Zenodo to ensure scientific transparency and reproducibility.

---

## 📝 Citation

If you use this dataset or code in your research, please cite the corresponding paper:
> Simanjuntak, T., Hafizh, M., Siahaan, H., & Prasandy, T. (2026). *User Engagement-Based Institutional Churn Analysis in Educational SaaS: An End-to-End Business Analytics and Lakehouse Approach*.