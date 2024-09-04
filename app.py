from flask import Flask, jsonify, request
from flask_cors import CORS, cross_origin

from report_generation.driver import generateReport
from stock_analysis.driver import analyseStock
from qna_bot.driver import answerQuestion
from visualization_generation.fetchDataFromQuickFS import getFinanceData

import os
import time
from dotenv import load_dotenv
load_dotenv()

app = Flask(__name__)

# Enable CORS for all routes
CORS(app)

STATIC_OUTPUT = bool(int(os.environ["STATIC_OUTPUT"]))

# Example route
@app.route("/hello", methods=["GET", "OPTIONS"])
def hello_world():
    return jsonify(message="Hello, World!")

# Another example with a POST request
@app.route("/insights", methods=["POST", "OPTIONS"])
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
        print(company, year, form_type, quarter)

        if STATIC_OUTPUT:
            time.sleep(2)
            if company == "Oracle" and int(year) == 2023 and form_type == "10K":
                result = {
                    "report": "**Revolutionizing Data Management: Oracle's Latest Innovation Holds Promise, But Challenges Loom**<br><br>As technology continues to advance at breakneck speed, companies are constantly seeking ways to stay ahead of the curve. Oracle's latest innovation, as revealed in its 2023 SEC 10K filing, has the potential to revolutionize the way data is managed, but its long-term implications are still unclear.<br><br>According to the Senior Research Analyst report, the technology aims to address current limitations and pain points in the industry, such as improving the efficiency and effectiveness of database management. While the exact limitations and pain points are not specified, it is clear that this technology has the potential to disrupt traditional business models and create new opportunities for innovation and growth.<br><br>However, the adoption of this technology is not without its challenges. Significant investments in infrastructure and training will be required, and the exact nature of these risks and challenges is still unclear. Furthermore, the long-term implications of this technology on consumers, employees, and society as a whole are still unknown.<br><br>Despite these uncertainties, the Visionary's insights suggest that the long-term implications of this technology are likely to be significant. As the technology continues to evolve, it is crucial that companies stay informed and adapt to the changing landscape.<br><br>In conclusion, while Oracle's latest innovation holds promise, its long-term implications are still unclear. As the technology continues to advance, it is crucial that companies stay vigilant and prepare for the challenges and opportunities that lie ahead.<br><br>Source: Oracle's SEC 10K filing, 2023.<br><br>Note: The report is written in a professional tone and style, and all information is sourced from Oracle's SEC 10K filing of 2023. The report is one page long and includes the long-term implications insights provided by the Visionary."
                }
                return result, 200
            elif company == "Nvidia" and int(year) == 2023 and form_type == "10K":
                result = {
                    "report": "**NVIDIA's AI Computing Platform: A Catalyst for Transformation**<br><br>NVIDIA's artificial intelligence (AI) computing platform has the potential to revolutionize various industries, including healthcare, finance, and education. According to the company's 10-K filing for 2023, its technology can accelerate computationally intensive tasks, leading to significant performance improvements and cost savings.<br><br>**Transforming Healthcare**<br><br>NVIDIA's AI computing platform can transform the healthcare industry by enabling the development of personalized medicine. For instance, AI-powered algorithms can analyze medical images and diagnose diseases more accurately and quickly than human doctors. Additionally, AI can help develop targeted treatments and improve patient outcomes.<br><br>**Revolutionizing Finance**<br><br>NVIDIA's AI computing platform can also revolutionize the finance industry by enabling the development of AI-powered trading platforms. These platforms can analyze vast amounts of data and make predictions about market trends, allowing for more informed investment decisions.<br><br>**Enhancing Education**<br><br>Furthermore, NVIDIA's AI computing platform can enhance the education sector by enabling the development of AI-powered adaptive learning systems. These systems can analyze individual students' learning styles and abilities, providing personalized learning experiences that improve student outcomes.<br><br>**Long-term Implications**<br><br>The long-term implications of NVIDIA's AI computing platform are significant. According to our Visionary, the platform has the potential to transform industries, improve lives, and create new opportunities for innovation. However, it is essential to mitigate the risks and challenges associated with the adoption of this technology, such as job displacement, safety concerns, and regulatory compliance.<br><br>In conclusion, NVIDIA's AI computing platform is a catalyst for transformation, with the potential to revolutionize various industries and improve lives. As the company continues to develop and deploy its technology, it is essential to consider the long-term implications and ensure that the benefits of this technology are realized."
                }
                return result, 200
            elif (
                company == "Tesla"
                and int(year) == 2023
                and form_type == "10Q"
                and quarter == "Q3"
            ):
                result = {
                    "report": "**Accelerating the Future of Transportation and Energy: Tesla's Q3 2023 Financial Performance**<br><br>As the world shifts towards a more sustainable and technologically advanced future, Tesla continues to lead the charge. The company's Q3 2023 financial performance showcases its commitment to innovation and growth, with significant improvements in revenue, gross margin, and operating income.<br><br>**Revenue Growth and Gross Margin Expansion**<br><br>Tesla's revenue grew by 56% year-over-year, driven by strong demand for its electric vehicles and energy storage products. The company's gross margin percentage increased to 25.1%, up from 22.3% in Q3 2022, reflecting improved operational efficiency and economies of scale.<br><br>**Operational Efficiency and Expense Management**<br><br>Operating expenses as a percentage of revenue decreased to 12.1%, down from 14.1% in Q3 2022, demonstrating the company's ability to manage costs effectively. Research and development expenses increased 34% year-over-year, reflecting Tesla's continued investment in technology and product development.<br><br>**Capital Expenditures and Liquidity**<br><br>Capital expenditures for the quarter were $1.23 billion, up from $1.06 billion in Q3 2022, as the company continues to invest in its manufacturing capacity and technology development. Tesla's cash and cash equivalents balance increased to $15.4 billion, providing a strong liquidity position to support future growth initiatives.<br><br>**Long-term Implications**<br><br>The long-term implications of Tesla's technology are significant, with the potential to shape the future of the automotive and energy industries. As the company continues to innovate and expand its product offerings, it is well-positioned to capitalize on the growing demand for sustainable energy solutions and autonomous mobility.<br><br>In conclusion, Tesla's Q3 2023 financial performance demonstrates its commitment to growth, innovation, and sustainability. As the company continues to lead the charge towards a more sustainable future, investors can expect significant returns on their investment."
                }
                return result, 200

        quarter = "" if form_type == "10K" else quarter
        report = generateReport(company, year, form_type, quarter)
        report = report.replace("\n", "<br>")
        result = {"report": report}

        # Return the JSON data back in the response
        return result, 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Another example with a POST request
@app.route("/analyse-stock", methods=["POST", "OPTIONS"])
@cross_origin()
def getStockPrediction():
    try:
        # Access the JSON data sent in the request
        data = request.get_json()

        # Check if data is valid
        if not data:
            return jsonify({"error": "Invalid or missing JSON data"}), 400

        company = data["company"]
        if STATIC_OUTPUT:
            time.sleep(2)
            if company == "Google":
                result = {
                    "advice": "This growth is primarily driven by the company's strong financial performance, innovative products, and strategic investments in emerging technologies. The financial statements show a strong balance sheet with a low debt-to-equity ratio of 0.07, which is lower than the industry average. However, regulatory scrutiny and increasing competition in the tech industry pose potential risks to future performance.",
                    "growth-potential": "CAGR of 12% over 5 years",
                    "risk": "Medium",
                    "verdict": "Buy",
                }
                return result, 200
            elif company == "Oracle":
                result = {
                    "advice": "This growth is primarily driven by Oracle's strong position in the technology industry and its ability to adapt to changing market trends. The financial statements show a moderate level of debt and a declining EPS growth rate, but the company's market share and industry position are strong, outpacing many of its competitors.",
                    "growth-potential": "CAGR of 15% over 5 years",
                    "risk": "Medium",
                    "verdict": "Buy",
                }
                return result, 200
            elif company == "Amazon":
                result = {
                    "advice": "This growth is primarily driven by increased demand for its cloud computing services and e-commerce platform. The financial statements show that Amazon's growth rate outpaces most of its competitors, but its profit margin is still lower than many established technology companies.",
                    "growth-potential": "CAGR of 22% over 5 years",
                    "risk": "Medium",
                    "verdict": "Buy",
                }
                return result, 200

        report = analyseStock(company).strip()
        for delimiter in ["VERDICT:", "RISK:", "GROWTH POTENTIAL:", "ADVICE:"]:
            report = report.replace(delimiter, "$$")

        report = report.split("$$")
        result = {
            "verdict": report[1].strip(),
            "risk": report[2].strip(),
            "growth-potential": report[3].strip(),
            "advice": report[4].strip(),
        }

        # Return the JSON data back in the response
        return result, 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Another example with a POST request
@app.route("/qna", methods=["POST", "OPTIONS"])
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
        print(company, year, form_type, quarter, question)

        if STATIC_OUTPUT:
            time.sleep(2)
            if (
                company == "Microsoft"
                and int(year) == 2023
                and form_type == "10K"
                and "growth" in question
            ):
                result = {
                    "answer": "In 2023, Microsoft's growth was steady, with a 7% increase in revenue to $242,059 million, a 14% increase in net income to $69,385 million, and a 15% increase in diluted EPS to $9.65. The growth was driven by various segments, including Productivity and Business Processes, Intelligent Cloud, and More Personal Computing, as well as geographic regions such as the United States and international markets."
                }
                return result, 200
            elif (
                company == "AMD"
                and int(year) == 2022
                and form_type == "10K"
                and "management" in question
            ):
                result = {
                    "answer": "Yes, there were management changes in the company. In August 2022, the company announced the departure of its Chief Financial Officer, Devinder Kumar, and the appointment of Jean Hu as the new Chief Financial Officer, effective October 2022. Additionally, the company's President and Chief Executive Officer, Lisa Su, took on the additional role of Chair of the Board of Directors, effective January 2023."
                }
                return result, 200
            elif (
                company == "Oracle"
                and int(year) == 2023
                and form_type == "10Q"
                and quarter == "Q4"
                and "takeaways" in question
            ):
                result = {
                    "answer": "Based on Oracle's SEC 10Q filing for Q4 of 2023, some big takeaways include: revenue of $12.4 billion (up 18% from Q4 last year), Cloud Services and License Support revenues of $8.9 billion (up 14% from Q4 last year), Operating Income of $4.4 billion with a 35% Operating Margin, Net Income of $3.5 billion with an Earnings Per Share of $1.16, and strong cash flow generation with $14.8 billion in operating cash flow and $11.2 billion in free cash flow. Additionally, the results reflect the impact of the COVID-19 pandemic and the global economic environment."
                }
                return result, 200

        quarter = "" if form_type == "10K" else quarter
        answer = answerQuestion(company, year, form_type, quarter, question)
        answer = answer.replace("\n", "<br>")
        result = {"answer": answer}

        # Return the JSON data back in the response
        return result, 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

# Another example with a POST request
@app.route("/visualization", methods=["POST", "OPTIONS"])
@cross_origin()
def getVisualization():
    try:
        # Access the JSON data sent in the request
        data = request.get_json()

        # Check if data is valid
        if not data:
            return jsonify({"error": "Invalid or missing JSON data"}), 400

        company = data["company"]
        if STATIC_OUTPUT:
            time.sleep(2)
            if company == "Google":
                data = {
                    "eps_basic": [
                        {
                            "id": 0,
                            "series": "Earnings Per Share (EPS)",
                            "size": 100,
                            "value": 1.04,
                            "year": 2014,
                        },
                        {
                            "id": 1,
                            "series": "Earnings Per Share (EPS)",
                            "size": 100,
                            "value": 1.15,
                            "year": 2015,
                        },
                        {
                            "id": 2,
                            "series": "Earnings Per Share (EPS)",
                            "size": 100,
                            "value": 1.41,
                            "year": 2016,
                        },
                        {
                            "id": 3,
                            "series": "Earnings Per Share (EPS)",
                            "size": 100,
                            "value": 0.91,
                            "year": 2017,
                        },
                        {
                            "id": 4,
                            "series": "Earnings Per Share (EPS)",
                            "size": 100,
                            "value": 2.21,
                            "year": 2018,
                        },
                        {
                            "id": 0,
                            "series": "Earnings Per Share (EPS)",
                            "size": 100,
                            "value": 2.48,
                            "year": 2019,
                        },
                        {
                            "id": 1,
                            "series": "Earnings Per Share (EPS)",
                            "size": 100,
                            "value": 2.95,
                            "year": 2020,
                        },
                        {
                            "id": 2,
                            "series": "Earnings Per Share (EPS)",
                            "size": 100,
                            "value": 5.69,
                            "year": 2021,
                        },
                        {
                            "id": 3,
                            "series": "Earnings Per Share (EPS)",
                            "size": 100,
                            "value": 4.59,
                            "year": 2022,
                        },
                        {
                            "id": 4,
                            "series": "Earnings Per Share (EPS)",
                            "size": 100,
                            "value": 5.84,
                            "year": 2023,
                        },
                    ],
                    "fcf": [
                        {
                            "id": 0,
                            "series": "Free Cash Flow (FCF)",
                            "size": 100,
                            "value": 12065000000,
                            "year": 2014,
                        },
                        {
                            "id": 1,
                            "series": "Free Cash Flow (FCF)",
                            "size": 100,
                            "value": 16657000000,
                            "year": 2015,
                        },
                        {
                            "id": 2,
                            "series": "Free Cash Flow (FCF)",
                            "size": 100,
                            "value": 26064000000,
                            "year": 2016,
                        },
                        {
                            "id": 3,
                            "series": "Free Cash Flow (FCF)",
                            "size": 100,
                            "value": 23907000000,
                            "year": 2017,
                        },
                        {
                            "id": 4,
                            "series": "Free Cash Flow (FCF)",
                            "size": 100,
                            "value": 22832000000,
                            "year": 2018,
                        },
                        {
                            "id": 0,
                            "series": "Free Cash Flow (FCF)",
                            "size": 100,
                            "value": 30972000000,
                            "year": 2019,
                        },
                        {
                            "id": 1,
                            "series": "Free Cash Flow (FCF)",
                            "size": 100,
                            "value": 42843000000,
                            "year": 2020,
                        },
                        {
                            "id": 2,
                            "series": "Free Cash Flow (FCF)",
                            "size": 100,
                            "value": 67012000000,
                            "year": 2021,
                        },
                        {
                            "id": 3,
                            "series": "Free Cash Flow (FCF)",
                            "size": 100,
                            "value": 60010000000,
                            "year": 2022,
                        },
                        {
                            "id": 4,
                            "series": "Free Cash Flow (FCF)",
                            "size": 100,
                            "value": 69495000000,
                            "year": 2023,
                        },
                    ],
                    "gross_profit": [
                        {
                            "id": 0,
                            "series": "Gross Profit",
                            "size": 100,
                            "value": 40310000000,
                            "year": 2014,
                        },
                        {
                            "id": 1,
                            "series": "Gross Profit",
                            "size": 100,
                            "value": 46825000000,
                            "year": 2015,
                        },
                        {
                            "id": 2,
                            "series": "Gross Profit",
                            "size": 100,
                            "value": 55134000000,
                            "year": 2016,
                        },
                        {
                            "id": 3,
                            "series": "Gross Profit",
                            "size": 100,
                            "value": 65272000000,
                            "year": 2017,
                        },
                        {
                            "id": 4,
                            "series": "Gross Profit",
                            "size": 100,
                            "value": 77270000000,
                            "year": 2018,
                        },
                        {
                            "id": 0,
                            "series": "Gross Profit",
                            "size": 100,
                            "value": 89961000000,
                            "year": 2019,
                        },
                        {
                            "id": 1,
                            "series": "Gross Profit",
                            "size": 100,
                            "value": 97795000000,
                            "year": 2020,
                        },
                        {
                            "id": 2,
                            "series": "Gross Profit",
                            "size": 100,
                            "value": 146698000000,
                            "year": 2021,
                        },
                        {
                            "id": 3,
                            "series": "Gross Profit",
                            "size": 100,
                            "value": 156633000000,
                            "year": 2022,
                        },
                        {
                            "id": 4,
                            "series": "Gross Profit",
                            "size": 100,
                            "value": 174062000000,
                            "year": 2023,
                        },
                    ],
                    "revenue": [
                        {
                            "id": 0,
                            "series": "Revenue Growth",
                            "size": 100,
                            "value": 66001000000,
                            "year": 2014,
                        },
                        {
                            "id": 1,
                            "series": "Revenue Growth",
                            "size": 100,
                            "value": 74989000000,
                            "year": 2015,
                        },
                        {
                            "id": 2,
                            "series": "Revenue Growth",
                            "size": 100,
                            "value": 90272000000,
                            "year": 2016,
                        },
                        {
                            "id": 3,
                            "series": "Revenue Growth",
                            "size": 100,
                            "value": 110855000000,
                            "year": 2017,
                        },
                        {
                            "id": 4,
                            "series": "Revenue Growth",
                            "size": 100,
                            "value": 136819000000,
                            "year": 2018,
                        },
                        {
                            "id": 0,
                            "series": "Revenue Growth",
                            "size": 100,
                            "value": 161857000000,
                            "year": 2019,
                        },
                        {
                            "id": 1,
                            "series": "Revenue Growth",
                            "size": 100,
                            "value": 182527000000,
                            "year": 2020,
                        },
                        {
                            "id": 2,
                            "series": "Revenue Growth",
                            "size": 100,
                            "value": 257637000000,
                            "year": 2021,
                        },
                        {
                            "id": 3,
                            "series": "Revenue Growth",
                            "size": 100,
                            "value": 282836000000,
                            "year": 2022,
                        },
                        {
                            "id": 4,
                            "series": "Revenue Growth",
                            "size": 100,
                            "value": 307394000000,
                            "year": 2023,
                        },
                    ],
                }
                return data, 200
            elif company == "Oracle":
                data = {
                    "eps_basic": [
                        {
                            "id": 0,
                            "series": "Earnings Per Share (EPS)",
                            "size": 100,
                            "value": 2.26,
                            "year": 2014,
                        },
                        {
                            "id": 1,
                            "series": "Earnings Per Share (EPS)",
                            "size": 100,
                            "value": 2.11,
                            "year": 2015,
                        },
                        {
                            "id": 2,
                            "series": "Earnings Per Share (EPS)",
                            "size": 100,
                            "value": 2.3,
                            "year": 2016,
                        },
                        {
                            "id": 3,
                            "series": "Earnings Per Share (EPS)",
                            "size": 100,
                            "value": 0.87,
                            "year": 2017,
                        },
                        {
                            "id": 4,
                            "series": "Earnings Per Share (EPS)",
                            "size": 100,
                            "value": 3.05,
                            "year": 2018,
                        },
                        {
                            "id": 0,
                            "series": "Earnings Per Share (EPS)",
                            "size": 100,
                            "value": 3.16,
                            "year": 2019,
                        },
                        {
                            "id": 1,
                            "series": "Earnings Per Share (EPS)",
                            "size": 100,
                            "value": 4.67,
                            "year": 2020,
                        },
                        {
                            "id": 2,
                            "series": "Earnings Per Share (EPS)",
                            "size": 100,
                            "value": 2.49,
                            "year": 2021,
                        },
                        {
                            "id": 3,
                            "series": "Earnings Per Share (EPS)",
                            "size": 100,
                            "value": 3.15,
                            "year": 2022,
                        },
                        {
                            "id": 4,
                            "series": "Earnings Per Share (EPS)",
                            "size": 100,
                            "value": 3.82,
                            "year": 2023,
                        },
                    ],
                    "fcf": [
                        {
                            "id": 0,
                            "series": "Free Cash Flow (FCF)",
                            "size": 100,
                            "value": 13189000000,
                            "year": 2014,
                        },
                        {
                            "id": 1,
                            "series": "Free Cash Flow (FCF)",
                            "size": 100,
                            "value": 12496000000,
                            "year": 2015,
                        },
                        {
                            "id": 2,
                            "series": "Free Cash Flow (FCF)",
                            "size": 100,
                            "value": 12105000000,
                            "year": 2016,
                        },
                        {
                            "id": 3,
                            "series": "Free Cash Flow (FCF)",
                            "size": 100,
                            "value": 13650000000,
                            "year": 2017,
                        },
                        {
                            "id": 4,
                            "series": "Free Cash Flow (FCF)",
                            "size": 100,
                            "value": 12891000000,
                            "year": 2018,
                        },
                        {
                            "id": 0,
                            "series": "Free Cash Flow (FCF)",
                            "size": 100,
                            "value": 11575000000,
                            "year": 2019,
                        },
                        {
                            "id": 1,
                            "series": "Free Cash Flow (FCF)",
                            "size": 100,
                            "value": 13752000000,
                            "year": 2020,
                        },
                        {
                            "id": 2,
                            "series": "Free Cash Flow (FCF)",
                            "size": 100,
                            "value": 5028000000,
                            "year": 2021,
                        },
                        {
                            "id": 3,
                            "series": "Free Cash Flow (FCF)",
                            "size": 100,
                            "value": 8470000000,
                            "year": 2022,
                        },
                        {
                            "id": 4,
                            "series": "Free Cash Flow (FCF)",
                            "size": 100,
                            "value": 11807000000,
                            "year": 2023,
                        },
                    ],
                    "gross_profit": [
                        {
                            "id": 0,
                            "series": "Gross Profit",
                            "size": 100,
                            "value": 30694000000,
                            "year": 2014,
                        },
                        {
                            "id": 1,
                            "series": "Gross Profit",
                            "size": 100,
                            "value": 29568000000,
                            "year": 2015,
                        },
                        {
                            "id": 2,
                            "series": "Gross Profit",
                            "size": 100,
                            "value": 30340000000,
                            "year": 2016,
                        },
                        {
                            "id": 3,
                            "series": "Gross Profit",
                            "size": 100,
                            "value": 31323000000,
                            "year": 2017,
                        },
                        {
                            "id": 4,
                            "series": "Gross Profit",
                            "size": 100,
                            "value": 31511000000,
                            "year": 2018,
                        },
                        {
                            "id": 0,
                            "series": "Gross Profit",
                            "size": 100,
                            "value": 31130000000,
                            "year": 2019,
                        },
                        {
                            "id": 1,
                            "series": "Gross Profit",
                            "size": 100,
                            "value": 32624000000,
                            "year": 2020,
                        },
                        {
                            "id": 2,
                            "series": "Gross Profit",
                            "size": 100,
                            "value": 33563000000,
                            "year": 2021,
                        },
                        {
                            "id": 3,
                            "series": "Gross Profit",
                            "size": 100,
                            "value": 36390000000,
                            "year": 2022,
                        },
                        {
                            "id": 4,
                            "series": "Gross Profit",
                            "size": 100,
                            "value": 37818000000,
                            "year": 2023,
                        },
                    ],
                    "revenue": [
                        {
                            "id": 0,
                            "series": "Revenue Growth",
                            "size": 100,
                            "value": 38226000000,
                            "year": 2014,
                        },
                        {
                            "id": 1,
                            "series": "Revenue Growth",
                            "size": 100,
                            "value": 37047000000,
                            "year": 2015,
                        },
                        {
                            "id": 2,
                            "series": "Revenue Growth",
                            "size": 100,
                            "value": 37792000000,
                            "year": 2016,
                        },
                        {
                            "id": 3,
                            "series": "Revenue Growth",
                            "size": 100,
                            "value": 39383000000,
                            "year": 2017,
                        },
                        {
                            "id": 4,
                            "series": "Revenue Growth",
                            "size": 100,
                            "value": 39506000000,
                            "year": 2018,
                        },
                        {
                            "id": 0,
                            "series": "Revenue Growth",
                            "size": 100,
                            "value": 39068000000,
                            "year": 2019,
                        },
                        {
                            "id": 1,
                            "series": "Revenue Growth",
                            "size": 100,
                            "value": 40479000000,
                            "year": 2020,
                        },
                        {
                            "id": 2,
                            "series": "Revenue Growth",
                            "size": 100,
                            "value": 42440000000,
                            "year": 2021,
                        },
                        {
                            "id": 3,
                            "series": "Revenue Growth",
                            "size": 100,
                            "value": 49954000000,
                            "year": 2022,
                        },
                        {
                            "id": 4,
                            "series": "Revenue Growth",
                            "size": 100,
                            "value": 52961000000,
                            "year": 2023,
                        },
                    ],
                }
                return data, 200
            elif company == "Tesla":
                data = {
                    "eps_basic": [
                        {
                            "id": 0,
                            "series": "Earnings Per Share (EPS)",
                            "size": 100,
                            "value": -0.15,
                            "year": 2014,
                        },
                        {
                            "id": 1,
                            "series": "Earnings Per Share (EPS)",
                            "size": 100,
                            "value": -0.46,
                            "year": 2015,
                        },
                        {
                            "id": 2,
                            "series": "Earnings Per Share (EPS)",
                            "size": 100,
                            "value": -0.31,
                            "year": 2016,
                        },
                        {
                            "id": 3,
                            "series": "Earnings Per Share (EPS)",
                            "size": 100,
                            "value": -0.78,
                            "year": 2017,
                        },
                        {
                            "id": 4,
                            "series": "Earnings Per Share (EPS)",
                            "size": 100,
                            "value": -0.38,
                            "year": 2018,
                        },
                        {
                            "id": 0,
                            "series": "Earnings Per Share (EPS)",
                            "size": 100,
                            "value": -0.32,
                            "year": 2019,
                        },
                        {
                            "id": 1,
                            "series": "Earnings Per Share (EPS)",
                            "size": 100,
                            "value": 0.24,
                            "year": 2020,
                        },
                        {
                            "id": 2,
                            "series": "Earnings Per Share (EPS)",
                            "size": 100,
                            "value": 1.87,
                            "year": 2021,
                        },
                        {
                            "id": 3,
                            "series": "Earnings Per Share (EPS)",
                            "size": 100,
                            "value": 4.02,
                            "year": 2022,
                        },
                        {
                            "id": 4,
                            "series": "Earnings Per Share (EPS)",
                            "size": 100,
                            "value": 4.73,
                            "year": 2023,
                        },
                    ],
                    "fcf": [
                        {
                            "id": 0,
                            "series": "Free Cash Flow (FCF)",
                            "size": 100,
                            "value": -1027222000,
                            "year": 2014,
                        },
                        {
                            "id": 1,
                            "series": "Free Cash Flow (FCF)",
                            "size": 100,
                            "value": -2159349000,
                            "year": 2015,
                        },
                        {
                            "id": 2,
                            "series": "Free Cash Flow (FCF)",
                            "size": 100,
                            "value": -1564300000,
                            "year": 2016,
                        },
                        {
                            "id": 3,
                            "series": "Free Cash Flow (FCF)",
                            "size": 100,
                            "value": -4142000000,
                            "year": 2017,
                        },
                        {
                            "id": 4,
                            "series": "Free Cash Flow (FCF)",
                            "size": 100,
                            "value": -221000000,
                            "year": 2018,
                        },
                        {
                            "id": 0,
                            "series": "Free Cash Flow (FCF)",
                            "size": 100,
                            "value": 973000000,
                            "year": 2019,
                        },
                        {
                            "id": 1,
                            "series": "Free Cash Flow (FCF)",
                            "size": 100,
                            "value": 2711000000,
                            "year": 2020,
                        },
                        {
                            "id": 2,
                            "series": "Free Cash Flow (FCF)",
                            "size": 100,
                            "value": 4983000000,
                            "year": 2021,
                        },
                        {
                            "id": 3,
                            "series": "Free Cash Flow (FCF)",
                            "size": 100,
                            "value": 7561000000,
                            "year": 2022,
                        },
                        {
                            "id": 4,
                            "series": "Free Cash Flow (FCF)",
                            "size": 100,
                            "value": 4357000000,
                            "year": 2023,
                        },
                    ],
                    "gross_profit": [
                        {
                            "id": 0,
                            "series": "Gross Profit",
                            "size": 100,
                            "value": 881671000,
                            "year": 2014,
                        },
                        {
                            "id": 1,
                            "series": "Gross Profit",
                            "size": 100,
                            "value": 923503000,
                            "year": 2015,
                        },
                        {
                            "id": 2,
                            "series": "Gross Profit",
                            "size": 100,
                            "value": 1599257000,
                            "year": 2016,
                        },
                        {
                            "id": 3,
                            "series": "Gross Profit",
                            "size": 100,
                            "value": 2223000000,
                            "year": 2017,
                        },
                        {
                            "id": 4,
                            "series": "Gross Profit",
                            "size": 100,
                            "value": 4042000000,
                            "year": 2018,
                        },
                        {
                            "id": 0,
                            "series": "Gross Profit",
                            "size": 100,
                            "value": 4069000000,
                            "year": 2019,
                        },
                        {
                            "id": 1,
                            "series": "Gross Profit",
                            "size": 100,
                            "value": 6630000000,
                            "year": 2020,
                        },
                        {
                            "id": 2,
                            "series": "Gross Profit",
                            "size": 100,
                            "value": 13606000000,
                            "year": 2021,
                        },
                        {
                            "id": 3,
                            "series": "Gross Profit",
                            "size": 100,
                            "value": 20853000000,
                            "year": 2022,
                        },
                        {
                            "id": 4,
                            "series": "Gross Profit",
                            "size": 100,
                            "value": 17660000000,
                            "year": 2023,
                        },
                    ],
                    "revenue": [
                        {
                            "id": 0,
                            "series": "Revenue Growth",
                            "size": 100,
                            "value": 3198356000,
                            "year": 2014,
                        },
                        {
                            "id": 1,
                            "series": "Revenue Growth",
                            "size": 100,
                            "value": 4046025000,
                            "year": 2015,
                        },
                        {
                            "id": 2,
                            "series": "Revenue Growth",
                            "size": 100,
                            "value": 7000132000,
                            "year": 2016,
                        },
                        {
                            "id": 3,
                            "series": "Revenue Growth",
                            "size": 100,
                            "value": 11759000000,
                            "year": 2017,
                        },
                        {
                            "id": 4,
                            "series": "Revenue Growth",
                            "size": 100,
                            "value": 21461000000,
                            "year": 2018,
                        },
                        {
                            "id": 0,
                            "series": "Revenue Growth",
                            "size": 100,
                            "value": 24578000000,
                            "year": 2019,
                        },
                        {
                            "id": 1,
                            "series": "Revenue Growth",
                            "size": 100,
                            "value": 31536000000,
                            "year": 2020,
                        },
                        {
                            "id": 2,
                            "series": "Revenue Growth",
                            "size": 100,
                            "value": 53823000000,
                            "year": 2021,
                        },
                        {
                            "id": 3,
                            "series": "Revenue Growth",
                            "size": 100,
                            "value": 81462000000,
                            "year": 2022,
                        },
                        {
                            "id": 4,
                            "series": "Revenue Growth",
                            "size": 100,
                            "value": 96773000000,
                            "year": 2023,
                        },
                    ],
                }
                return data, 200

        data = getFinanceData(company)

        # Return the JSON data back in the response
        return data, 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)
