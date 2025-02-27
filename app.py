from flask import Flask, request, jsonify
import psycopg2
import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()
app = Flask(__name__)

DATABASE_URL = os.getenv("SUPABASE_DB_URL")

def get_db_connection():
    return psycopg2.connect(DATABASE_URL, sslmode="require")

@app.route('/career_assessment', methods=['POST'])
def career_assessment():
    data = request.json
    interest = data.get("interest")
    skills = data.get("skills", [])
    work_env = data.get("work_environment", [])
    visa_needs = data.get("visa_friendly")

    conn = get_db_connection()
    cur = conn.cursor()

    # Match user inputs to career fields
    cur.execute("""
        SELECT career_name, recommended_majors, avg_salary, job_growth_percentage
        FROM career_options
        WHERE $1 = ANY(recommended_majors) 
        AND $2 = ANY(key_skills)
        AND $3 = ANY(work_environment)
        AND ($4 IS NULL OR visa_friendly = $4)
    """, (interest, skills[0], work_env[0], visa_needs))

    matches = cur.fetchall()
    cur.close()
    conn.close()

    if matches:
        recommendations = [
            {"career": row[0], "majors": row[1], "salary": row[2], "growth": row[3]}
            for row in matches
        ]
        return jsonify({"recommended_careers": recommendations})
    else:
        return jsonify({"message": "No exact match found, but let’s explore related fields!"})

if __name__ == '__main__':
    app.run(debug=True)