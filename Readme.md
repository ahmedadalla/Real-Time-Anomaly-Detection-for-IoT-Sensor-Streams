# Cyber-Physical Security in Modern Water Treatment Facilities

Real-time anomaly and cyber-attack detection for industrial water treatment systems using multivariate time-series data.

## Overview

Modern water treatment plants rely on interconnected Industrial Control Systems (ICS) composed of distributed sensors and actuators. As these systems become increasingly networked and digitized, their exposure to cyber threats grows significantly.

Attackers may inject false sensor data, manipulate control commands, or disrupt communication networks while keeping operations seemingly normal — making detection challenging.

## Problem

Detect cyber-attacks and anomalies in real time from high-dimensional, heterogeneous sensor data across interdependent process stages while:

- Maintaining high system availability  
- Minimizing false alarms  
- Meeting strict sub-second latency requirements  

## Objective

Develop an intelligent detection system that achieves:

- **High recall** (maximize attack detection)  
- **Balanced precision** (avoid unnecessary shutdowns)  
- **Real-time performance under operational constraints**  

## 📦 Install Requirements

Make sure you have Python 3.9+ installed.

Then install all required dependencies using:

```bash
pip install -r requirements.txt
```

If you are using Google Colab, run:

```python
!pip install -r requirements.txt
```

This will install all necessary libraries listed in the `requirements.txt` file.

## 📂 How to Run the Data Loading Notebook in Google Colab

Follow these simple steps:

### 1️⃣ Create a Folder in Google Drive

1. Open **Google Drive**.
2. Click **New → Folder**.
3. Name the folder exactly:

```
DepiPrpject
```

---

### 2️⃣ Upload the Notebook

Upload the file:

```
Data_loading_cleaning.ipynb
```

into the `DepiProject` folder.

---

### 3️⃣ Open in Google Colab

1. Right-click on `Data_loading_cleaning.ipynb`.
2. Select **Open with → Google Colaboratory**.

---

### 4️⃣ Run the Notebook

Click:

```
Runtime → Run all
```

The notebook will automatically:

- Mount Google Drive  
- Load the dataset  
- Store the data inside the `DepiPrpject` folder  
- Perform data loading and cleaning  

No additional setup is required.

---

✅ After execution, your data will be properly prepared and ready for the next modeling steps.