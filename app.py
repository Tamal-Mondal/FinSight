from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

from report_generation.driver import generateReport
from stock_analysis.driver import analyseStock
from qna_bot.driver import answerQuestion
from visualization_generation.driver import generateVisualizations

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

STATIC_OUTPUT = True

# Example route
@app.route('/hello', methods=['GET', 'OPTIONS'])
def hello_world():
    return jsonify(message="Hello, World!")

# Another example with a POST request
@app.route('/insights', methods=['POST', 'OPTIONS'])
@cross_origin()
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
        quarter = data["quarter"] if "quarter" in data else ""
        
        if STATIC_OUTPUT and company == "Oracle":
            result = {
                "report": "**Expertly Styled Report: Implications of Emerging Trends on Oracle's Business**<br><br>As a senior editor at the Wall Street Journal, I have crafted a comprehensive report that provides an in-depth analysis of the implications of emerging trends on Oracle's business. The report is based on the insights provided by the Visionary and verified by the Senior Research Analyst using Oracle's SEC 10K filing of year 2023.<br><br>**Introduction**<br><br>Oracle, a leading technology company, operates in a highly competitive market with established players like Microsoft, Amazon, and Salesforce. The company's current limitations and pain points include intense competition, rapid technological changes, and global economic conditions. However, emerging trends like cloud computing, artificial intelligence, and the Internet of Things (IoT) may disrupt traditional business models and create new opportunities for Oracle.<br><br>**Current Limitations and Pain Points**<br><br>Oracle's current limitations and pain points are well-documented in its SEC 10K filing of year 2023. The company's intense competition may lead to pricing pressures, reduced market share, and decreased revenue. Rapid technological changes require Oracle to invest heavily in research and development to stay ahead of the curve. Global economic conditions may impact Oracle's global operations, affecting revenue and profitability.<br><br>**Disrupting Traditional Business Models and Creating New Opportunities**<br><br>Emerging trends may disrupt traditional business models and create new opportunities for Oracle. Cloud computing can disrupt traditional on-premise software models, offering greater flexibility, scalability, and cost savings. Artificial intelligence (AI) can enhance Oracle's software products, providing predictive analytics, automation, and improved customer experiences. IoT solutions can enable businesses to connect devices, collect data, and gain insights, creating new revenue streams.<br><br>**Potential Risks and Challenges**<br><br>The adoption of emerging trends may pose risks and challenges for Oracle. Increased reliance on cloud computing and IoT may expose Oracle to cybersecurity threats, compromising customer data and trust. Oracle may face challenges in attracting and retaining skilled talent to develop and implement emerging technologies. The company must navigate complex regulatory landscapes, ensuring compliance with laws and regulations related to data privacy, security, and intellectual property.<br><br>**Impact on Consumers, Employees, and Society**<br><br>Emerging trends may have a significant impact on consumers, employees, and society. Oracle's AI-powered software can provide personalized, intuitive, and efficient customer experiences, improving customer satisfaction and loyalty. Automation and AI may lead to job displacement, but also create new opportunities for employees to develop skills in emerging technologies. Oracle's IoT solutions can improve public services, transportation, and healthcare, contributing to a more connected, efficient, and sustainable society.<br><br>**Long-term Implications and Future Outlook**<br><br>In the long term, emerging trends may shape the future of the industry and Oracle's business. Oracle's cloud services will continue to grow, driving revenue and profitability. The company's investment in AI will lead to innovative software products, enhancing customer experiences and competitiveness. Oracle's IoT solutions will expand into new markets, creating new revenue streams and opportunities for growth.<br><br>**Conclusion**<br><br>In conclusion, emerging trends will have a profound impact on Oracle's business, presenting both opportunities and challenges. By embracing these trends, Oracle can disrupt traditional business models, create new revenue streams, and drive growth, while minimizing risks and challenges. As a senior editor at the Wall Street Journal, I am confident that this report provides a comprehensive analysis of the implications of emerging trends on Oracle's business, and I recommend it to investors and stakeholders seeking to understand the company's future prospects.<br><br>Sources:<br>Oracle's SEC 10K filing of year 2023<br>Detailed Analysis Report: Implications of Emerging Trends on Oracle's Business (Visionary)<br>Verification of Information (Senior Research Analyst)"
            }
            return result, 200

        print(company, year, form_type, quarter)
        quarter = "" if form_type == "10K" else quarter
        report = generateReport(company, year, form_type, quarter)
        report = report.replace("\n", "<br>")
        result = {"report": report}

        # Return the JSON data back in the response
        return result, 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Another example with a POST request
@app.route('/analyse-stock', methods=['POST', 'OPTIONS'])
@cross_origin()
def getStockPrediction():
    try:
        # Access the JSON data sent in the request
        data = request.get_json()

        # Check if data is valid
        if not data:
            return jsonify({"error": "Invalid or missing JSON data"}), 400

        company = data["company"]
        if STATIC_OUTPUT and company == "Google":
            result = {
                "advice": "This growth is primarily driven by the company's strong financial performance, innovative products, and strategic investments in emerging technologies. The financial statements show a strong balance sheet with a low debt-to-equity ratio of 0.07, which is lower than the industry average. However, regulatory scrutiny and increasing competition in the tech industry pose potential risks to future performance.",
                "growth-potential": "CAGR of 12% over 5 years",
                "risk": "Medium",
                "verdict": "Buy",
            }
            return result, 200

        report = analyseStock(company).strip()
        for delimiter in ['VERDICT:', 'RISK:', 'GROWTH POTENTIAL:', 'ADVICE:']:
            report = report.replace(delimiter, '$$')

        report = report.split('$$')
        result = {
                    "verdict": report[1].strip(), 
                    "risk": report[2].strip(), 
                    "growth-potential": report[3].strip(), 
                    "advice": report[4].strip()
                 }

        # Return the JSON data back in the response
        return result, 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Another example with a POST request
@app.route('/qna', methods=['POST', 'OPTIONS'])
@cross_origin()
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
        quarter = data["quarter"] if "quarter" in data else ""
        question = data["question"]
        
        if STATIC_OUTPUT and company == "Microsoft":
            result = {
                "answer": "In 2023, Microsoft's growth was steady, with a 7% increase in revenue to $242,059 million, a 14% increase in net income to $69,385 million, and a 15% increase in diluted EPS to $9.65. The growth was driven by various segments, including Productivity and Business Processes, Intelligent Cloud, and More Personal Computing, as well as geographic regions such as the United States and international markets."
            }
            return result, 200

        print(company, year, form_type, quarter, question)
        quarter = "" if form_type == "10K" else quarter
        answer = answerQuestion(company, year, form_type, quarter, question)
        answer = answer.replace("\n", "<br>")
        result = {"answer": answer}

        # Return the JSON data back in the response
        return result, 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Another example with a POST request
@app.route('/visualization', methods=['POST', 'OPTIONS'])
@cross_origin()
def getVisualization():
    data = request.json
    generateVisualizations()
    return jsonify(data)

if __name__ == '__main__':
    app.run(host='0.0.0.0', port=5000)
