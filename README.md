# 🏥 Insurance Premium Prediction

This project predicts **insurance premium tiers** (`low`, `medium`, `high`) using customer information such as **BMI, age group, lifestyle risk, city tier, income, and occupation**.  

The solution is built using:
- **scikit-learn** for training a machine learning model
- **FastAPI** for serving predictions via REST API
- **Streamlit** for creating an interactive frontend

---

##  Dataset

The dataset contains the following features:

- `bmi` – Body Mass Index (float)  
- `age_group` – Age group (`adult`, `middle_aged`, `senior`)  
- `lifestyle_risk` – Lifestyle risk (`low`, `medium`, `high`)  
- `city_tier` – City category (1, 2, 3)  
- `income_lpa` – Annual income (in Lakhs per Annum)  
- `occupation` – Occupation type (unemployed, freelancer, private_job, business_owner)  
- `premium_tier` – **Target** label (`low`, `medium`, `high`)  

---

##  Model Used

The model used is **RandomForestClassifier** from scikit-learn.  

- Random Forest is an **ensemble model** that combines multiple decision trees to make more robust and accurate predictions.  
- It works well with both numerical (BMI, income, city_tier) and categorical (occupation, lifestyle risk, age group) features.  
- The categorical features are encoded using **OneHotEncoder** inside a **ColumnTransformer** pipeline.

---

## ⚡ FastAPI (Backend)

- **FastAPI** is a modern Python web framework for building APIs.  
- In this project, it is used to expose the ML model as REST endpoints.  
- Available endpoints:  
  - `/health` → check if API is running  
  - `/predict` → send user input and get predicted premium tier  


---

##  Streamlit (Frontend)

- **Streamlit** is a Python framework for building interactive web applications for data science and ML projects.  
- It provides a simple UI where users can enter their details (BMI, income, age group, etc.) and click **Predict**.  
- The app sends the input to the FastAPI backend and displays the **predicted premium tier** along with a confidence score.  

---

