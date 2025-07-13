import joblib

# Load trained model and vectorizer
model = joblib.load("sql_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")

def predict_sql(query):
    query_vec = vectorizer.transform([query])
    prediction = model.predict(query_vec)[0]
    probability = model.predict_proba(query_vec)[0][prediction]

    if prediction == 1:
        result = "WARNING: This query is potentially DANGEROUS (SQL Injection detected)."
    else:
        result = "This query is considered SAFE."

    return {
        "prediction": prediction,
        "probability": round(probability * 100, 2),
        "message": result
    }

# Quick test:
if __name__ == "__main__":
    test_query = input("Enter an SQL query to check: ")
    result = predict_sql(test_query)
    print(f"\nAnalysis Result: {result['message']}")
    print(f"Probability: {result['probability']}%")
