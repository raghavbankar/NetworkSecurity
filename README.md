# Network Security Phishing Detection Pipeline

An end-to-end machine learning project for phishing website detection, built with a strong network security focus. This repository demonstrates how security-oriented feature engineering, data validation, experiment tracking, and model training can be combined into a production-style ML pipeline.

The project uses phishing-related URL and website attributes, stores the source data in MongoDB, validates the dataset against a schema, checks for drift, applies preprocessing, trains multiple classification models, and logs experiments with MLflow and DagsHub.

## Table of Contents

- [Project Overview](#project-overview)
- [Problem Statement](#problem-statement)
- [Dataset Summary](#dataset-summary)
- [Key Highlights](#key-highlights)
- [Machine Learning Workflow](#machine-learning-workflow)
- [Project Structure](#project-structure)
- [Tech Stack](#tech-stack)
- [Getting Started](#getting-started)
- [How to Run](#how-to-run)
- [Artifacts Generated](#artifacts-generated)
- [Why This Project Stands Out](#why-this-project-stands-out)
- [Future Improvements](#future-improvements)

## Project Overview

Phishing attacks remain one of the most common and damaging threats in network security. This project focuses on identifying malicious or suspicious websites using machine learning on structured phishing indicators such as URL characteristics, domain signals, HTTPS behavior, page rank, DNS information, iframe usage, and related web-security features.

From an engineering perspective, this repository is more than a notebook-based experiment. It is organized as a modular pipeline with separate components for:

- data ingestion
- data validation
- data transformation
- model training
- experiment tracking
- artifact generation

This makes the project suitable for showcasing both security domain understanding and applied ML engineering skills.

## Problem Statement

The objective is to build a binary classification pipeline that can distinguish phishing-related patterns from legitimate-looking website behavior using structured website and URL features.

This project is relevant to:

- phishing detection
- threat intelligence enrichment
- secure browsing systems
- network monitoring and anomaly screening
- security analytics portfolios

## Dataset Summary

The repository contains a phishing dataset at `Network_Data/phisingData.csv`.

- Total records: `11,055`
- Total columns: `31`
- Input features: `30`
- Target column: `Result`

The available features represent security-related website signals, including:

- IP address usage in URLs
- URL length and shortening services
- presence of `@` symbols and redirect patterns
- sub-domain and prefix/suffix patterns
- SSL state and HTTPS token behavior
- favicon, port, iframe, request URL, and anchor-based signals
- DNS record, page rank, Google index, web traffic, and domain age indicators

The target labels are transformed during preprocessing so the training pipeline can work cleanly with binary classification output.

## Key Highlights

- Built an end-to-end ML pipeline for a real cybersecurity use case
- Integrated MongoDB for data storage and ingestion
- Added schema-driven validation for dataset consistency
- Implemented data drift checks using the Kolmogorov-Smirnov test
- Applied preprocessing with `KNNImputer` for missing-value handling
- Compared multiple machine learning models using hyperparameter tuning
- Logged metrics and models with MLflow and DagsHub
- Saved reusable artifacts such as transformed arrays, preprocessing objects, and trained models

## Machine Learning Workflow

### 1. Data Ingestion

Raw phishing data is first pushed to MongoDB using `push_data.py`. The training pipeline then reads the collection, converts it into a DataFrame, stores a feature-store copy, and performs a train/test split.

### 2. Data Validation

The validation stage checks:

- whether the dataset matches the expected schema
- whether the numerical columns are consistent with the schema definition
- whether train and test data show drift

The schema is defined in `Data_schema/schema.yaml`, and the drift report is written to the generated artifacts directory.

### 3. Data Transformation

The transformation stage:

- separates features and target
- converts the target label format for model training
- applies a preprocessing pipeline with `KNNImputer`
- saves transformed training and testing arrays
- serializes the fitted preprocessing object

### 4. Model Training

The trainer evaluates multiple classification models, including:

- Random Forest
- Decision Tree
- Gradient Boosting
- Logistic Regression
- AdaBoost

Hyperparameter search is performed through `GridSearchCV`, and the selected model is wrapped together with the preprocessor for inference.

### 5. Experiment Tracking

Model metrics are logged to MLflow, with DagsHub used for experiment tracking integration. The pipeline records classification metrics such as:

- F1 score
- Precision
- Recall

## Project Structure

```text
project2/
|-- main.py
|-- push_data.py
|-- requirements.txt
|-- setup.py
|-- README.md
|-- Network_Data/
|   |-- phisingData.csv
|-- Data_schema/
|   |-- schema.yaml
|-- networksecurity/
|   |-- components/
|   |   |-- data_ingestion.py
|   |   |-- data_validation.py
|   |   |-- data_transfromation.py
|   |   |-- Model_trainer.py
|   |-- entity/
|   |   |-- config_entity.py
|   |   |-- artifact_entity.py
|   |-- constant/
|   |   |-- Training_pipeline/
|   |-- Utils/
|   |   |-- utils_main/
|   |   |-- ML_utils/
|   |-- logging/
|   |-- exception/
|-- Artifacts/
|-- Logs/
```

## Tech Stack

### Languages and Libraries

- Python
- Pandas
- NumPy
- Scikit-learn
- PyYAML
- PyMongo
- python-dotenv

### MLOps and Tracking

- MLflow
- DagsHub

### Storage

- MongoDB Atlas

## Getting Started

### 1. Clone the Repository

```bash
git clone <your-repository-url>
cd project2
```

### 2. Create a Virtual Environment

```bash
python -m venv venv
```

On Windows:

```bash
venv\Scripts\activate
```

On Linux/macOS:

```bash
source venv/bin/activate
```

### 3. Install Dependencies

```bash
pip install -r requirements.txt
```

### 4. Configure Environment Variables

Create a `.env` file in the project root and add:

```env
MONGO_DB="your_mongodb_connection_string"
```

## How to Run

### Step 1: Push Source Data to MongoDB

```bash
python push_data.py
```

This reads `Network_Data/phisingData.csv` and inserts the records into the configured MongoDB database and collection.

### Step 2: Run the Training Pipeline

```bash
python main.py
```

This executes the full pipeline:

1. ingestion
2. validation
3. transformation
4. model training
5. artifact creation

### Step 3: Run the FastAPI Inference Endpoint

A separate inference service has been added in `app.py` so you can serve the trained model without changing the training pipeline.

Install the dependencies and start the app:

```bash
pip install -r requirements.txt
uvicorn app:app --reload --host 0.0.0.0 --port 8000
```

Example prediction request:

```bash
curl -X POST "http://127.0.0.1:8000/predict" \
  -H "Content-Type: application/json" \
  -d '{"features": {"having_IP_Address": 1, "URL_Length": 54, "Shortining_Service": 0, "having_At_Symbol": 0, "double_slash_redirecting": 0, "Prefix_Suffix": 0, "having_Sub_Domain": 0, "SSLfinal_State": 1, "Domain_registeration_length": 1, "Favicon": 0, "port": 0, "HTTPS_token": 1, "Request_URL": 0, "URL_of_Anchor": 0, "Links_in_tags": 0, "SFH": 0, "Submitting_to_email": 0, "Abnormal_URL": 0, "Redirect": 0, "on_mouseover": 0, "RightClick": 0, "popUpWidnow": 0, "Iframe": 0, "age_of_domain": 1, "DNSRecord": 1, "web_traffic": 1, "Page_Rank": 1, "Google_Index": 1, "Links_pointing_to_page": 1, "Statistical_report": 1}}'
```

## Artifacts Generated

Each execution creates a timestamped folder inside `Artifacts/`. Typical outputs include:

- feature store data
- training and testing CSV files
- validated datasets
- drift reports
- transformed NumPy arrays
- preprocessing object (`preprocessing.pkl`)
- trained model (`Model.pkl`)

Logs are also generated under `Logs/` for traceability and debugging.

## Why This Project Stands Out

This repository is a strong portfolio project because it demonstrates more than model fitting. It shows practical ML engineering for cybersecurity:

- translating a network security problem into a structured ML solution
- building modular pipeline components instead of a single notebook script
- validating input data before training
- checking for drift as part of pipeline quality control
- comparing models rather than relying on a single algorithm
- tracking experiments with MLflow and DagsHub
- packaging the final preprocessing + model object for reuse

If you want to showcase your machine learning skills in a security context, this project clearly reflects:

- data engineering fundamentals
- applied classification modeling
- model evaluation discipline
- MLOps awareness
- secure and scalable pipeline thinking

## Future Improvements

- expose predictions through a FastAPI or Flask service
- add Docker support for reproducible deployment
- create GitHub Actions for CI/CD
- include EDA and model performance reports in the repository
- add feature importance visualization and explainability
- support batch or real-time phishing prediction workflows

---

This project demonstrates the intersection of network security and machine learning by turning phishing detection into a reproducible and modular ML pipeline suitable for experimentation, extension, and professional presentation.
