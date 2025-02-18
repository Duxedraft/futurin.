from flask import Flask, request, jsonify
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

app = Flask(__name__)

# Supabase Database Connection
DATABASE_URL = os.getenv("SUPABASE_DB_URL")

def get_db_connection():
    try:
        conn = psycopg2.connect(DATABASE_URL, sslmode="require")
        return conn
    except Exception as e:
        print("❌ Database connection error:", e)
        return None

# ✅ Test Route to Confirm Flask is Running
@app.route('/')
def home():
    return "✅ Flask API is Running!"

# ✅ Career Recommendation Route
@app.route('/get_career_recommendations', methods=['GET'])
def get_career_recommendations():
    user_interest = request.args.get('interest')  # Get interest from URL params

    if not user_interest:
        return jsonify({"error": "Interest parameter is required"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    cur = conn.cursor()

    # Query job market data based on interest
    query = """
        SELECT industry, top_majors, average_salary, job_growth_percentage
        FROM job_market
        WHERE industry ILIKE %s OR top_majors ILIKE %s
    """
    cur.execute(query, (f"%{user_interest}%", f"%{user_interest}%"))
    
    results = cur.fetchall()
    cur.close()
    conn.close()

    if results:
        formatted_careers = []
        for row in results:
            career_message = (
            f"💼 **{row[0]}** is a great field to explore! \n"
            f"📚 **Recommended Majors:** {row[1]}\n"
            f"💰 **Average Salary:** ${row[2]:,} per year\n"
            f"📈 **Job Growth:** {row[3]}% projected increase\n"
        )
        formatted_careers.append(career_message)
        return jsonify({"fulfillmentText": "\n\n".join(formatted_careers)})
    else:
        return jsonify({"fulfillmentText": "I'm sorry, I couldn't find a matching career. Try another interest!"})

if __name__ == '__main__':
    app.run(debug=True)