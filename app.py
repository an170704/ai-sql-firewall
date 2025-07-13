import streamlit as st
import joblib
import pandas as pd
import seaborn as sns
import matplotlib.pyplot as plt


# Load model and vectorizer
model = joblib.load("sql_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")


# Add threshold parameter for probability
def predict_sql(query, threshold=0.5):
    query_vec = vectorizer.transform([query])
    proba = model.predict_proba(query_vec)[0]
    attack_prob = proba[1]
    is_attack = attack_prob >= threshold
    if is_attack:
        result = "🚨 WARNING: DANGEROUS query (SQL Injection)"
    else:
        result = "✅ Query is safe"
    return int(is_attack), round(attack_prob * 100, 2), result

st.set_page_config(page_title="AI SQL Firewall", page_icon="🛡️")
st.title("🛡️ AI Firewall: SQL Injection Detection")

st.markdown("Enter an SQL query to check:")


# Add threshold slider and pie chart toggle
col1, col2 = st.columns(2)
with col1:
    threshold = st.slider("Attack probability threshold (%)", min_value=1, max_value=99, value=50, step=1)
with col2:
    show_pie = st.checkbox("Show pie chart", value=True)

user_input = st.text_area("🔍 SQL Query:", height=100)


if st.button("Analyze"):
    if user_input.strip() == "":
        st.warning("Please enter an SQL query.")
    else:
        pred, prob, msg = predict_sql(user_input, threshold=threshold/100)
        st.subheader("📋 Analysis Result:")
        st.markdown(f"**{msg}**")
        st.metric(label="📊 Attack Probability", value=f"{prob}%")

        if show_pie:
            labels = ['Safe', 'Attack']
            sizes = [100 - prob, prob] if pred == 1 else [prob, 100 - prob]
            colors = ['green', 'red'] if pred == 1 else ['green', 'orange']
            fig, ax = plt.subplots()
            ax.pie(sizes, labels=labels, autopct='%1.1f%%', colors=colors, startangle=140)
            ax.axis('equal')
            st.pyplot(fig)

st.markdown("---")
st.caption("Project: AI-based SQL Injection Detection using NLP")
