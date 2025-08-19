# app.py

# Import Flask and pickle for loading the model.
# Note: We no longer need to import numpy or StandardScaler
import flask
from flask import Flask, request, render_template
import pickle

# Create an instance of the Flask application.
app = Flask(__name__)

# --- Load the Model Pipeline ---
# This single file contains both the scaler and the linear regression model.
try:
    with open('model.pkl', 'rb') as model_file:
        pipeline = pickle.load(model_file)
except FileNotFoundError:
    print("Error: The model file 'model.pkl' was not found.")
    print("Please ensure you have saved your pipeline in the same directory.")
    pipeline = None

# --- Define the Routes ---

@app.route('/')
def home():
    """
    This is the main route for our application.
    It renders the HTML template 'index.html' which contains the form.
    """
    return render_template('index.html')

@app.route('/predict', methods=['POST'])
def predict():
    """
    This route handles the form submission and makes a prediction.
    It is only accessible via a POST request from the form.
    """
    if pipeline is None:
        return "Error: Model pipeline not loaded. Please check the console for details."

    # Get the weight value from the form input.
    try:
        weight = float(request.form['weight'])
    except ValueError:
        return "Error: Invalid input. Please enter a valid number for weight."

    # The pipeline handles the reshaping and scaling automatically.
    # We pass the input as a list of lists, which is what the pipeline expects.
    prediction = pipeline.predict([[weight]])[0]

    # Format the prediction to a more readable string with 2 decimal places.
    prediction_text = f"The predicted height is: {prediction:.2f} cm"

    # Render the same template, but this time pass the prediction text to be displayed.
    return render_template('index.html', prediction_text=prediction_text)

# --- Run the Application ---
if __name__ == "__main__":
    app.run(debug=True)
