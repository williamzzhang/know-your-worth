import streamlit as st 
import pandas as pd
import matplotlib.pyplot as mpl

def shorten_categories(categories, cutoff):
    categorical_map = {}
    for i in range(len(categories)):
        if categories.values[i] >= cutoff:
            categorical_map[categories.index[i]] = categories.index[i]
        else:
            categorical_map[categories.index[i]] = 'Other'
    return categorical_map

def convert_experience(x):
    if x == 'More than 50 years':
        return 50
    if x == 'Less than 1 year':
        return 0.5
    return float(x)

def convert_education(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional degree' in x or 'Other doctoral' in x:
        return 'Post grad'
    return 'Less than a Bachelors'


@st.cache
def load_data():
    df = pd.read_csv("survey_results_public.csv")
    df = df[["Country", "EdLevel", "YearsCodePro", "Employment", "ConvertedCompYearly"]]
    df = df.rename({"ConvertedCompYearly": "Salary"}, axis=1)
    df = df[df["Salary"].notnull()]
    df = df.dropna()
    df = df[df["Employment"] == "Employed, full-time"]
    df = df.drop("Employment", axis=1)
    
    country_map = shorten_categories(df.Country.value_counts(), 400)
    df['Country'] = df['Country'].map(country_map)
    df = df[df["Salary"] <= 500000]
    df = df[df["Salary"] >= 10000]
    df = df[df['Country'] != 'Other']
    
    df['YearsCodePro'] = df['YearsCodePro'].apply(convert_experience)
    df['EdLevel'] = df['EdLevel'].apply(convert_education)
    return df

df = load_data()

def show_explore_page():
    st.write("""## Explore Software Engineer Salaries""")
    
    st.write("""#### Data from Stack Overflow Developer Survey 2022""")
    
    data = df["Country"].value_counts()
    
    fig1, ax1 = mpl.subplots()
    ax1.pie(data, labels=data.index, autopct="%1.1f", shadow=False, rotatelabels=False, startangle=180)
    ax1.axis("equal") # Ensure pie is drawn as a circle by enforcing an equal aspect ratio
    
    st.write("""#### Number of Data from different countries""")
    
    st.pyplot(fig1)
    
    st.write("""### Mean Salary Based On Country""")
    
    data = df.groupby(["Country"])["Salary"].mean().sort_values(ascending=True)
    st.bar_chart(data,100, 800)
    
    st.write("""### Mean Salary Based On Experience""")
    data = df.groupby(["YearsCodePro"])["Salary"].mean().sort_values(ascending=True)
    st.line_chart(data)