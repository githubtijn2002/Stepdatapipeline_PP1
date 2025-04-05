import threading
import requests
import time
from datetime import datetime
from flask import Flask, jsonify, request
from functions import insert_data
import random

app = Flask(__name__)

# Generate fake step count for a given date
def generate_step_count(date_str):
    random.seed(date_str)  # So same date always returns same steps
    return {
        "minute_str": date_str,
        "steps": random.randint(0, 100)
    }

@app.route('/steps', methods=['GET'])
def get_steps():
    date_str = request.args.get('date')
    if not date_str:
        # Default to today
        date_str = datetime.today().strftime('%H%M')
    try:
        # Validate format
        datetime.strptime(date_str, '%H%M')
    except ValueError:
        return jsonify({"error": "Invalid date format. Use HHMM."}), 400
    # Generate step count for the given date
    data = generate_step_count(date_str)
    return jsonify(data)

# This is the function for polling every minute
def poll_steps():
    while True:
        response = requests.get("http://localhost:8080/steps", params={"date": datetime.today().strftime('%H%M')})
        if response.status_code == 200:
            insert_data(response.json())
        else:
            print(f"Error fetching data: {response.status_code}")
        # Wait 1 minute before the next request
        time.sleep(60)

if __name__ == '__main__':
    # Create a new thread to run the polling function
    polling_thread = threading.Thread(target=poll_steps)
    polling_thread.daemon = True  # This ensures the thread will stop when the main program exits
    polling_thread.start()
    
    # Run the Flask app (this will block and start the web server)
    app.run(debug=True, host="0.0.0.0", port=8080)
