import os
from flask import Flask, render_template
import json

app = Flask(__name__)

# Use environment variable for debug mode, defaulting to False for production
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
json_file = "static/city_data.json"
def count_cities_from_json(json_file):
    with open(json_file, 'r') as f:
        city_data = json.load(f)
    
    city_count = len(city_data)
    print(f"Number of unique cities: {city_count}")
    return city_count

@app.route('/')
def home():
    count_city = count_cities_from_json(json_file)
    return render_template('home.html', count_city=count_city)

if __name__ == '__main__':
    # Use environment variables for host and port
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 8000))
    app.run(host=host, port=port, debug=True, use_reloader=True)