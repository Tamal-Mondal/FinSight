import os
from textwrap import dedent
from crewai import Agent, Task, Crew, Process

from langchain_community.llms import Ollama
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.llms import HuggingFaceHub, HuggingFaceEndpoint
from langchain_community.chat_models.huggingface import ChatHuggingFace
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

from tools import ExtractionTools, QuickFSDataFetchingTools, ChartingTools, MarkdownTools
from dotenv import load_dotenv

from typing import List
from pydantic import BaseModel

load_dotenv()

model_name = "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo"
llm = ChatOpenAI(model=model_name,
                 temperature=0.7,
                 api_key="d1a8e935548aec33569f825c0d297a26733226000b730c62e08f0c6945740055",
                 base_url="https://api.together.xyz")

def getAgents():
    research_analyst_agent = Agent(
        role="Senior Research Analyst",
        goal=dedent(
            f"""Retrieve accurate data of the metric requested for a particular symbol."""
        ),
        backstory=dedent(
            f"""You have 10 years of experience in gathering and researching financial data. You are the best at using tools to 
        gather data from APIs like QuickFS. You critically analyze the question and understand different symbols and metrics. 
        You STRICTLY follow the required output format while returning the data."""
        ),
        tools=[
            QuickFSDataFetchingTools.get_metric_data_from_quickfs,
        ],
        verbose=True,
        llm=llm,
    )

    chart_creator_agent = Agent(
        role="Senior Visualization Expert",
        goal=dedent(f"""Create a chart of the data provided using the chart creation tool."""),
        backstory=dedent(
            f"""You are an expert in creating charts and graphs from the data. You are known for receiving a list of 
        data points with the company symbol from the research analyst and meticulously creating an accurate chart. You MUST 
        use the tool provided and output the chart in the CORRECT format."""
        ),
        tools=[ChartingTools.create_chart],
        verbose=True,
        llm=llm,
    )
    return [research_analyst_agent, chart_creator_agent]


def tip_section():
    return "If you do your BEST WORK and return the result exactly in the format I asked, I'll give you a $10,000 commission!"

def getTasks(symbol, metric, research_analyst_agent, chart_creator_agent):
    gather_data_task = Task(
        description=dedent(
            f"""The symbol is {symbol} and the metric is {metric}. Use the QuickFS tool to get the data for the corresponding 
            metric and the symbol. Output the dictionary having metric name and data received from the QuickFS tool.
        
            Output Format: A dictionary containing the metric (str) and data (List[float])

            Notes: 
            {tip_section()}
            """
        ),
        agent=research_analyst_agent
    )

    create_chart_task = Task(
        description=dedent(
            f"""
            Create a chart using the data received from the research analyst representing {metric} metric of {symbol} company. 
            Use the chart creation tool to create and save the chart as a png file. Pass the dictionary having the metric name (str)
            and data (list) received from the research analyst to the chart creation tool. Output the file name of the saved png file.

            Notes: 
            {tip_section()}
            """
        ),
        agent=chart_creator_agent,
        expected_output="""The file location where the chart is saved as image eg. fcf_chart.png, cogs_chart.png"""
    )

    return [gather_data_task, create_chart_task]

if __name__=="__main__":
    print("## Welcome to Report Creator Crew")
    print("-------------------------------")
    data = input(dedent("""Enter company symbol followed by the metrics you want to add to the markdown file report:\n>> """))

    research_analyst_agent, chart_creator_agent = getAgents()
    symbol, metric = data.strip().split("and")
    gather_data_task, create_chart_task = getTasks(symbol.strip(), metric.strip(), research_analyst_agent, chart_creator_agent)

    crew = Crew(
        agents=[research_analyst_agent, chart_creator_agent],
        tasks=[gather_data_task, create_chart_task],
        verbose=True,
    )

    result = crew.kickoff()
    print(result)
