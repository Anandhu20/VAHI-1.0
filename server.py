from flask import Flask, render_template, request
import subprocess

app = Flask(__name__)

# Variable to hold the subprocess
subprocess_instance = None

# Define a route to render the HTML template
@app.route('/')
def index():
    return render_template('va12.html')

# Define a route to handle the POST request from the HTML button
@app.route('/run_app', methods=['POST'])
def run_app():
    global subprocess_instance
    # Check if the subprocess is already running
    if subprocess_instance and subprocess_instance.poll() is None:
        return 'Voice Assistant is already running.'

    # Run the voice assistant script using subprocess
    subprocess_instance = subprocess.Popen(["python", "app.py"])

    return 'Voice Assistant started successfully.'

# Define a route to handle stopping the subprocess
@app.route('/stop_app', methods=['POST'])
def stop_app():
    global subprocess_instance
    if subprocess_instance and subprocess_instance.poll() is None:
        # Terminate the subprocess if it exists and is running
        subprocess_instance.terminate()
        subprocess_instance = None  # Reset subprocess instance
        return 'Voice Assistant stopped successfully.'
    else:
        return 'No running Voice Assistant to stop.'

# Define a route to handle the POST request from the HTML button for data collection
@app.route('/run_inference_classifier', methods=['POST'])
def run_inference_classifier():
    global subprocess_instance
    # Check if the subprocess is already running
    if subprocess_instance and subprocess_instance.poll() is None:
        return 'Inference Classifier is already running.'

    # Run the data collection script using subprocess
    subprocess_instance = subprocess.Popen(["python", "inference_classifier.py"])

    return 'Inference Classifier started successfully.\nPlease wait,this will take a few seconds.'

# Define a route to handle stopping the data collection subprocess
@app.route('/stop_inference_classifier', methods=['POST'])
def stop_inference_classifier():
    global subprocess_instance
    if subprocess_instance and subprocess_instance.poll() is None:
        # Terminate the subprocess if it exists and is running
        subprocess_instance.terminate()
        subprocess_instance = None  # Reset subprocess instance
        return 'Inference Classifier stopped successfully.'
    else:
        return 'No running Inference Classifier to stop.'

 

if __name__ == '__main__':
    app.run(debug=True, port=5000)
