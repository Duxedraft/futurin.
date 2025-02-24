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
    user_id = data.get("user_id")
    
    # Sample scoring logic
    interest_area = data.get("interest_area")  # Example: "Technology and computing"
    skills = data.get("skills", [])
    values = data.get("career_values", [])
    
    conn = get_db_connection()
    cur = conn.cursor()
    
    # Query careers matching interest area
    cur.execute("SELECT major, interest_alignment, skill_match, value_alignment FROM career_scoring WHERE major ILIKE %s", 
                (f"%{interest_area}%",))
    
    career_matches = cur.fetchall()
    recommendations = []
    
    for career in career_matches:
        major, interest_score, skill_score, value_score = career
        total_score = interest_score + skill_score + value_score
        
        if total_score >= 70:  # Adjust threshold if needed
            recommendations.append({
                "major": major,
                "score": total_score
            })
    
    cur.close()
    conn.close()
    
    return jsonify({"recommended_careers": sorted(recommendations, key=lambda x: x["score"], reverse=True)[:3]})

if __name__ == '__main__':
    app.run(debug=True)