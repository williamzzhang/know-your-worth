import streamlit as st
import pickle
import numpy as np


def load_model():
    with open('saved_steps.pkl', 'rb') as file:
        data = pickle.load(file)
    return data

data = load_model()

regressor = data["model"]
le_country = data["le_country"]
le_education = data["le_education"]

def show_predict_page():
    st.write("""## Software Developer Salary Prediction""")
    
    st.write("""#### We need some information to predict the salary""")
    
    countries = (
        "United States of America",
        "Germany",
        "United Kingdom of Great Britain and Northern Ireland",
        "India",
        "Canada",
        "France",
        "Brazil",
        "Spain",
        "Netherlands",
        "Australia",
        "Italy",
        "Poland",
        "Sweden",
        "Russian Federation",
        "Switzerland"
    )
    
    education = (
        "Bachelor’s degree",
        "Master’s degree",
        "Post grad",
        "Less than a Bachelors"
    )
    
    countrySelect = st.selectbox("Country", countries)
    
    educationSelect = st.selectbox("Education Level", education)
    
    experienceSelect = st.slider("Years of Experience", 0, 50, 1)
    
    clicked = st.button("Calculate Compensation")
    
    if clicked:
        x = np.array([[countrySelect, educationSelect, experienceSelect]])
        x[:, 0] = le_country.transform(x[:,0])
        x[:, 1] = le_education.transform(x[:,1])
        x = x.astype(float)
        
        compensation = regressor.predict(x)
        st.subheader(f"The estimated total compensation in USD is ${compensation[0]:.2f}")
        
    