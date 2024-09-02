# FinSight - A financial AI assistant tool for US-based companies 

## Requirements 

1. Anaconda
2. Python 3.11+
3. Poetry
4. CrewAI
5. LangChain
6. Flask

## Installation Steps

### 1. Add .env file in the root directory with all the API Keys
### 2. Clone the FinSight project 
```
git clone https://github.com/Tamal-Mondal/FinSight.git
cd FinSight
```
### 3. Create a conda environment with Python 3.11
```
conda create -n crewai-finance python=3.11 -y
conda activate crewai-finance
```
### 4. Install all the depenedencies as per pyproject.toml
```
pip install poetry platformdirs flask flask-cors
poetry install --no-root
```

## Usage

### Summarizing 10K/10Q Reports
Mention a specific 10K/10Q report of any US based company, the model will return a brief summary of it.
#### End-point
```
https://localhost:5000/insights
```
#### Payload
```
{ 
    "company": "Oracle",
    "year": 2023,
    "form-type": "10Q",
    "quarter": "Q4"
}
```

### Question-Answering on the basis of 10K/10Q reports
Based on the specific 10K/10Q reports, you can ask any question and should get a crisp answer.
#### End-point
```
https://localhost:5000/qna
```
#### Payload
```
{ 
    "company": "Microsoft",
    "year": 2023,
    "form-type": "10K",
    "quarter": "",
    "question": "How was the growth of the company in 2023?"
}
```

### Stock Analysis and Prediction
Mention a company name for which you want stock related prediction. The model will analyze the company financials and advice you accordingly.
#### End-point
```
https://localhost:5000/analyse-stock
```
#### Payload
```
{ 
    "company": "Google"
}
```

### Trends Visualization
Enter a company name, the model will return the past 10 years of data for some of the important metrics.
#### End-point
```
https://localhost:5000/visualization
```
#### Payload
```
{ 
    "company": "Google"
}
```


