import os
from flask import Flask, render_template
import json

app = Flask(__name__)

# Use environment variable for debug mode, defaulting to False for production
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'
json_file = "static/city_data.json"

def get_cities_from_json(json_file):
    with open(json_file, 'r') as f:
        city_data = json.load(f)
    
    cities = []
    for city_name in city_data.keys():
        parts = city_name.split(', ')
        if len(parts) == 3:
            city, state, country = parts
        elif len(parts) == 2:
            city, country = parts
            state = ''
        else:
            city, state, country = parts[0], '', parts[-1]
        
        cities.append({
            'city': city,
            'state': state,
            'country': country
        })
    
    return sorted(cities, key=lambda x: (x['country'], x['state'], x['city']))

@app.route('/')
def home():
    cities = get_cities_from_json(json_file)
    count_city = len(cities)
    return render_template('home.html', count_city=count_city, cities=cities)

if __name__ == '__main__':
    # Use environment variables for host and port
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('PORT', 8080))

    app.run(host=host, port=port, debug=True, use_reloader=True)
