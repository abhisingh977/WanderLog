import os
from flask import Flask, render_template

app = Flask(__name__)

# Use environment variable for debug mode, defaulting to False for production
app.config['DEBUG'] = os.environ.get('FLASK_DEBUG', 'False').lower() == 'true'

@app.route('/')
def home():
    return render_template('home.html')

if __name__ == '__main__':
    # Use environment variables for host and port
    host = os.environ.get('FLASK_HOST', '0.0.0.0')
    port = int(os.environ.get('FLASK_PORT', 8000))
    app.run(host=host, port=port)