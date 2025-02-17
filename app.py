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
    return psycopg2.connect(DATABASE_URL)

# API Endpoint: Fetch Career Recommendations Based on User Interests
@app.route('/get_career_recommendations', methods=['GET'])
def get_career_recommendations():
    user_interest = request.args.get('interest')  # Get interest from query params

    if not user_interest:
        return jsonify({"error": "Interest parameter is required"}), 400

    conn = get_db_connection()
    cur = conn.cursor()

    # Query job market data based on interest
    cur.execute("""
        SELECT industry, top_majors, average_salary, job_growth_percentage
        FROM job_market
        WHERE industry ILIKE %s OR top_majors ILIKE %s
    """, (f"%{user_interest}%", f"%{user_interest}%"))

    results = cur.fetchall()
    cur.close()
    conn.close()

    if results:
        careers = [{"industry": row[0], "top_majors": row[1], "average_salary": row[2], "growth": row[3]} for row in results]
        return jsonify({"careers": careers})
    else:
        return jsonify({"message": "No relevant careers found. Try another interest."})

if __name__ == '__main__':
    app.run(debug=True)