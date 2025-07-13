import joblib

# Load trained model and vectorizer
model = joblib.load("sql_model.pkl")
vectorizer = joblib.load("vectorizer.pkl")


def predict_sql(query, threshold=0.5):
    query_vec = vectorizer.transform([query])
    proba = model.predict_proba(query_vec)[0]
    attack_prob = proba[1]
    is_attack = attack_prob >= threshold
    if is_attack:
        result = "WARNING: This query is potentially DANGEROUS (SQL Injection detected)."
    else:
        result = "This query is considered SAFE."
    return {
        "prediction": int(is_attack),
        "probability": round(attack_prob * 100, 2),
        "message": result
    }

if __name__ == "__main__":
    import argparse
    parser = argparse.ArgumentParser(description="SQL Injection Query Predictor")
    parser.add_argument('--threshold', type=float, default=0.5, help='Attack probability threshold (0-1, default=0.5)')
    args = parser.parse_args()

    test_query = input("Enter an SQL query to check: ")
    result = predict_sql(test_query, threshold=args.threshold)
    print(f"\nAnalysis Result: {result['message']}")
    print(f"Attack Probability: {result['probability']}%")
