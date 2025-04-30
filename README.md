# 🧪 Diffusion Network Inference — Setup & Execution Guide

## ✅ Prerequisites

Ensure you have **Python 3** installed:
```bash
python3 --version
```
If Python 3 is not installed, download and install it from:
👉 https://www.python.org/

---

## 🔧 Script Configuration

Before running the script, make the following changes to the file `MergedScriptV3_new.py`:

- **Line 479:** Replace the placeholder with your **Twitter username**
- **Line 480:** Update with your **Twitter API credentials** (`cline`) for authentication

---

## 🚀 Running Instructions

Follow these steps in order:

### 1. Run the Data Collector
```bash
python3 MergedScriptV3_new.py
```
This script collects relevant data from Twitter using the credentials and parameters you provided.

### 2. Run the Data Analysis Script
```bash
python3 code_realData_new.py
```
This script performs inference over the collected data to generate diffusion networks.

---

## 📊 Project Description

Understanding how information spreads across social networks is critical for uncovering influence patterns and hidden connections. A **post-specific diffusion network** models the "who-saw-from-whom" pathways for a given post on social media.

However, such networks are **not directly observable** through typical platform data. This project introduces a novel **inference mechanism** that reconstructs diffusion networks by leveraging:
- **Temporal dynamics** (timestamps of shares)
- **Textual content** of posts
- **Underlying network structure**

The proposed algorithm utilizes a **conditional point process** to infer the most likely diffusion paths. It is scalable to thousands of shares and suitable for **real-time analytics**.

📎 Learn more at the official project site:  
🔗 https://sites.google.com/view/diffuscope/home
