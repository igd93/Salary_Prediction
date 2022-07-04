import streamlit as st
import pandas as pd
import matplotlib.pyplot as plt


def clean_experience(x):
    if x == 'More than 50 years':
        return 50.0
    if x == 'Less than 1 year':
        return 0.5
    return float(x)


def clean_education(x):
    if 'Bachelor’s degree' in x:
        return 'Bachelor’s degree'
    if 'Master’s degree' in x:
        return 'Master’s degree'
    if 'Professional’s degree' in x or 'Other doctoral' in x:
        return 'Post grad'
    return 'Less than a Bachelors'


@st.cache
def load_data():
    df = pd.read_csv('survey_results_public.csv', usecols=[
                     'Country', 'EdLevel', 'YearsCodePro', 'Employment', 'ConvertedComp'], low_memory=True)
    df = df.rename({'ConvertedComp': 'Salary'}, axis=1)
    df = df.dropna()
    df = df[df['Employment'] == 'Employed full-time']
    df = df.drop('Employment', axis=1)
    df = df[(df['Salary'] >= 10000) & (df['Salary'] <= 250000)]
    df = df.groupby('Country').filter(lambda x: len(x) >= 400)
    df['YearsCodePro'] = df['YearsCodePro'].apply(clean_experience)
    df['EdLevel'] = df['EdLevel'].apply(clean_education)
    return df


df = load_data()


def show_explore_page():
    st.title("Explore Software Engineer Salaries")

    st.write(
        """
        ### Stack Overflow Developer Survey 2020
        """
    )

    data = df['Country'].value_counts()
    fig1, ax1 = plt.subplots()
    ax1.pie(data, autopct='%1.1f', textprops={'fontsize': 8}, 
            labeldistance=1.4, pctdistance=0.8, startangle=90)
    ax1.axis("equal")  # For pie to be drawn as a circle

    ax1.legend(labels = data.index, loc='best', fontsize = 8)     

    st.write(""" ### Number of data from different countries, in percentages""")

    st.pyplot(fig1)
    
    st.write(""" ### Mean salary based on a country""")

    data = df.groupby(['Country'])['Salary'].mean().sort_values(ascending=True)
    st.bar_chart(data)

    st.write(""" ### Mean salary based on years of experience  """)
    data1 = df.groupby(["YearsCodePro"])['Salary'].mean().sort_values(ascending=True)
    st.line_chart(data1)