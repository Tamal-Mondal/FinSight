from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

from report_generation.driver import generateReport
from stock_analysis.driver import analyseStock
from qna_bot.driver import answerQuestion

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

# Example route
@app.route('/api/hello', methods=['GET'])
def hello_world():
    return jsonify(message="Hello, World!")

# Another example with a POST request
@app.route('/insights', methods=['POST'])
def getInsights():
    try:
        # Access the JSON data sent in the request
        data = request.get_json()

        # Check if data is valid
        if not data:
            return jsonify({"error": "Invalid or missing JSON data"}), 400
        
        company = data["company"]
        year = data["year"]
        form_type = data["form-type"]
        quarter = data["quarter"]
        
        print(company, year, form_type, quarter)
        quarter = "" if form_type == "10K" else quarter
        report = generateReport(company, year, form_type, quarter)
        report.replace("\n", "\n\n\n")
        result = {"report": report}

        # Return the JSON data back in the response
        return result, 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Another example with a POST request
@app.route('/analyse-stock', methods=['POST'])
def getStockPrediction():
    try:
        # Access the JSON data sent in the request
        data = request.get_json()

        # Check if data is valid
        if not data:
            return jsonify({"error": "Invalid or missing JSON data"}), 400
        
        company = data["company"]
        
        report = analyseStock(company)
        result = {"report": report}

        # Return the JSON data back in the response
        return result, 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Another example with a POST request
@app.route('/qna', methods=['POST'])
def askQuestion():
    try:
        # Access the JSON data sent in the request
        data = request.get_json()

        # Check if data is valid
        if not data:
            return jsonify({"error": "Invalid or missing JSON data"}), 400
        
        company = data["company"]
        year = data["year"]
        form_type = data["form-type"]
        quarter = data["quarter"]
        question = data["question"]
        
        print(company, year, form_type, quarter, question)
        quarter = "" if form_type == "10K" else quarter
        answer = answerQuestion(company, year, form_type, quarter, question)
        result = {"answer": answer}

        # Return the JSON data back in the response
        return result, 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Another example with a POST request
@app.route('/visualization', methods=['POST'])
def getVisualization():
    data = request.json
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
