import streamlit as st
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt
import plotly.express as px

st.set_page_config(page_title="HR Attrition Dashboard", layout="wide")

@st.cache_data
def load_data():
    return pd.read_csv("EA.csv")

df = load_data()

# Sidebar filters
st.sidebar.header("🔍 Filter Options")
department_filter = st.sidebar.multiselect("Select Department", df["Department"].unique(), default=df["Department"].unique())
gender_filter = st.sidebar.multiselect("Select Gender", df["Gender"].unique(), default=df["Gender"].unique())
age_slider = st.sidebar.slider("Select Age Range", int(df["Age"].min()), int(df["Age"].max()), (int(df["Age"].min()), int(df["Age"].max())))

df_filtered = df[
    (df["Department"].isin(department_filter)) &
    (df["Gender"].isin(gender_filter)) &
    (df["Age"].between(age_slider[0], age_slider[1]))
]

st.title("📊 HR Attrition Dashboard")
st.markdown("This dashboard presents an in-depth analysis of employee attrition. Use the filters on the left to explore the data by department, gender, and age.")

# Tabs
tab1, tab2, tab3, tab4 = st.tabs(["Demographics", "Attrition Insights", "Work & Pay", "Correlations"])

with tab1:
    st.subheader("1️⃣ Gender Distribution")
    st.markdown("This pie chart shows the gender split among employees.")
    fig1 = px.pie(df_filtered, names='Gender', title='Gender Distribution')
    st.plotly_chart(fig1, use_container_width=True)

    st.subheader("2️⃣ Department Count")
    st.markdown("Number of employees in each department.")
    fig2 = px.bar(df_filtered['Department'].value_counts().reset_index(),
                  x='index', y='Department', labels={'index': 'Department', 'Department': 'Count'})
    st.plotly_chart(fig2, use_container_width=True)

    st.subheader("3️⃣ Age Distribution")
    st.markdown("Age distribution of employees using histogram.")
    fig3 = px.histogram(df_filtered, x='Age', nbins=20)
    st.plotly_chart(fig3, use_container_width=True)

with tab2:
    st.subheader("4️⃣ Attrition Rate by Gender")
    st.markdown("Shows percentage of attrition by gender.")
    attr_by_gender = df_filtered.groupby('Gender')['Attrition'].value_counts(normalize=True).unstack().fillna(0)
    fig4 = attr_by_gender.plot(kind='bar', stacked=True)
    st.pyplot(fig4.figure)

    st.subheader("5️⃣ Attrition by Department")
    st.markdown("Which departments see the most attrition?")
    fig5 = px.histogram(df_filtered[df_filtered['Attrition'] == 'Yes'], x='Department')
    st.plotly_chart(fig5, use_container_width=True)

    st.subheader("6️⃣ Education Field vs Attrition")
    st.markdown("Attrition count by education field.")
    fig6 = px.histogram(df_filtered[df_filtered['Attrition'] == 'Yes'], x='EducationField', color='Gender')
    st.plotly_chart(fig6, use_container_width=True)

with tab3:
    st.subheader("7️⃣ Monthly Income Distribution")
    st.markdown("See how employee salaries are distributed.")
    fig7 = px.box(df_filtered, x="JobRole", y="MonthlyIncome", color="Attrition")
    st.plotly_chart(fig7, use_container_width=True)

    st.subheader("8️⃣ Years at Company vs Attrition")
    st.markdown("Visualizing experience in years against attrition.")
    fig8 = px.violin(df_filtered, y="YearsAtCompany", x="Attrition", box=True, color="Attrition")
    st.plotly_chart(fig8, use_container_width=True)

    st.subheader("9️⃣ Job Satisfaction Level")
    st.markdown("Bar plot for job satisfaction across attrition groups.")
    fig9 = px.histogram(df_filtered, x="JobSatisfaction", color="Attrition", barmode="group")
    st.plotly_chart(fig9, use_container_width=True)

with tab4:
    st.subheader("🔟 Correlation Heatmap")
    st.markdown("See relationships between numeric HR variables.")
    numeric_cols = df_filtered.select_dtypes(include=['int64', 'float64']).drop(columns=["EmployeeNumber"], errors="ignore")
    corr_matrix = numeric_cols.corr()
    fig10, ax = plt.subplots(figsize=(12, 8))
    sns.heatmap(corr_matrix, annot=True, cmap="coolwarm", fmt=".2f", ax=ax)
    st.pyplot(fig10)

    st.subheader("1️⃣1️⃣ Age vs Monthly Income")
    st.markdown("Scatter plot to identify relationship between age and income.")
    fig11 = px.scatter(df_filtered, x='Age', y='MonthlyIncome', color='Attrition', trendline='ols')
    st.plotly_chart(fig11, use_container_width=True)

    st.subheader("1️⃣2️⃣ Years at Company vs Age")
    st.markdown("Explores if older employees stay longer.")
    fig12 = px.scatter(df_filtered, x='YearsAtCompany', y='Age', color='Attrition')
    st.plotly_chart(fig12, use_container_width=True)

st.markdown("---")
st.markdown("🔎 *This dashboard enables the HR team to analyze both macro and micro trends in employee attrition. Use it to inform your next retention strategy.*")
