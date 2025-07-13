import streamlit as st
import joblib
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt

# Load mô hình và vectorizer
model = joblib.load("sql_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

# Prediction function
def predict_sql(query):
    query_vec = vectorizer.transform([query])
    prediction = model.predict(query_vec)[0]
    probability = model.predict_proba(query_vec)[0][prediction]

    if prediction == 1:
        result = "🚨 WARNING: DANGEROUS query (SQL Injection)"
    else:
        result = "✅ Query is safe"

    return prediction, round(probability * 100, 2), result

# Streamlit UI
st.set_page_config(page_title="AI SQL Firewall", page_icon="🛡️")
st.title("🛡️ AI Firewall: SQL Injection Detection")

st.markdown("Enter an SQL query to check:")

user_input = st.text_area("🔍 SQL Query:", height=100)

if st.button("Analyze"):
    if user_input.strip() == "":
        st.warning("Please enter an SQL query.")
    else:
        pred, prob, msg = predict_sql(user_input)
        st.subheader("📋 Analysis Result:")
        st.markdown(f"**{msg}**")
        st.metric(label="📊 Probability", value=f"{prob}%")

        # Pie chart
        labels = ['Safe', 'Attack']
        sizes = [100 - prob, prob] if pred == 1 else [prob, 100 - prob]
        colors = ['green', 'red'] if pred == 1 else ['green', 'orange']

        fig, ax = plt.subplots()
        ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=140)
        ax.axis('equal')
        st.pyplot(fig)

st.markdown("---")
st.caption("Project: AI-based SQL Injection Detection using NLP")
