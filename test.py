from flask import Flask
from supabase import create_client, Client
import os
from dotenv import load_dotenv
    
load_dotenv()
    
app = Flask(__name__)
    
# Supabase configuration
url: str = os.environ.get("SUPABASE_URL")
key: str = os.environ.get("SUPABASE_KEY")
supabase: Client = create_client(url, key)
    
@app.route('/')
def hello():
        return 'Hello, Flask with Supabase!'
    
if __name__ == '__main__':
        app.run(debug=True)
