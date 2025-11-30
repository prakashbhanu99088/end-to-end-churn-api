# 🤖 End-to-End Customer Churn Prediction Microservice


## 1. Project Overview & Business Goal 🎯

This project is a complete **Machine Learning Microservice** built for predicting customer churn for a telecommunications company. It demonstrates a full end-to-end MLOps pipeline, from data preparation and model training to deployment as a REST API.

**Goal:** To help the company proactively identify high-risk customers before they cancel their service, allowing marketing teams to offer retention incentives.

## 2. Technical Architecture & Flow ⚙️

The system is designed as a modular service that can be containerized (e.g., Docker) and scaled.

1.  **Training:** The `train.py` script loads data from a local **SQLite database**, performs feature selection (focusing on `tenure`, `charges`, `contract`), encodes categorical variables, and trains a **Random Forest Classifier**. The final model is saved as `model_churn.pkl`.
2.  **Deployment (API):** The `app.py` uses **FastAPI** to load the saved model and exposes a single `/predict` endpoint.
3.  **Prediction:** The API receives raw customer data (JSON), preprocesses it instantly, and returns a binary prediction (`Yes`/`No` for churn) along with the associated probability.

## 3. Tech Stack

| Category | Tool / Library | Purpose |
| :--- | :--- | :--- |
| **Model Serving** | **FastAPI** | High-performance, asynchronous web framework for the API. |
| **ML Libraries** | **Scikit-Learn** | Used for the Random Forest Classifier. |
| **Data Handling** | **Pandas, SQLite** | Data manipulation and persistence layer for the training data. |
| **Serialization** | **Joblib** | Efficiently saving and loading the trained model object. |

## 4. Local Setup and Installation 💻

To run this project locally, clone the repository and install the dependencies.

### Prerequisites
* Python 3.8+
* The trained model (`model_churn.pkl`) must be available in the root directory.

### Steps

1.  **Clone the Repository (If using the command line later):**
    ```bash
    git clone [https://github.com/prakashbhanu99088/end-to-end-churn-api.git](https://github.com/prakashbhanu99088/end-to-end-churn-api.git)
    cd end-to-end-churn-api
    ```

2.  **Install Dependencies:**
    ```bash
    pip install -r requirements.txt
    ```

3.  **Run the API Server:**
    ```bash
    python -m uvicorn app:app --reload
    ```
    *(The server runs on http://127.0.0.1:8000)*

## 5. API Usage and Testing

The API uses **Swagger UI** for testing and documentation.

1.  Open your browser to: `http://127.0.0.1:8000/docs`
2.  Expand the `POST /predict` endpoint.
3.  Click "Try it out" and submit the following JSON data to receive a real-time prediction:

```json
{
  "tenure": 12,
  "MonthlyCharges": 50.0,
  "TotalCharges": 600.0,
  "Contract": "One year"
}
