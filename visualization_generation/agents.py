from crewai import Agent
from textwrap import dedent
from langchain_community.llms import Ollama
from langchain_google_genai import ChatGoogleGenerativeAI
from langchain_community.llms import HuggingFaceHub, HuggingFaceEndpoint
from langchain_community.chat_models.huggingface import ChatHuggingFace
from langchain_openai import ChatOpenAI
from langchain_google_genai import ChatGoogleGenerativeAI

from visualization_generation.tools import ExtractionTools, QuickFSDataFetchingTools, ChartingTools, MarkdownTools
from dotenv import load_dotenv
import os

load_dotenv() 

class FinancialResearchAgents:
    def __init__(self):
        
        # oai_api_key = os.getenv("OPENAI_API_KEY")
        # self.OpenAIGPT35 = ChatOpenAI(model_name="gpt-3.5-turbo-0125", temperature=0.4, api_key=oai_api_key)
        # self.OpenAIGPT4 = ChatOpenAI(model_name="gpt-4-turbo-preview", temperature=0.5)
        # self.Ollama = Ollama(model="openhermes")
        
        #model_name = "Qwen/Qwen1.5-14B-Chat"
        #model_name = "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"
        #model_name = "NousResearch/Nous-Hermes-2-Mixtral-8x7B-SFT"
        #model_name = "meta-llama/Meta-Llama-3-70B-Instruct-Lite"
        model_name = "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo"
        self.llm = ChatOpenAI(model=model_name,
                     temperature=0.7,
                     api_key="d1a8e935548aec33569f825c0d297a26733226000b730c62e08f0c6945740055",
                     base_url="https://api.together.xyz")
        
        gemini_api_key = os.getenv("GEMINI_API_KEY")
        print("GEMINI API KEY: " + gemini_api_key)
        self.gemini = ChatGoogleGenerativeAI(model="gemini-1.5-flash",
                                             verbose=True, 
                                             temperature=0.5, 
                                             google_api_key=gemini_api_key)

    def markdown_report_creator(self):
        return Agent(
            role="Markdown Report Creator",
            goal=dedent(f"""Retrieve accurate data of the metrics requested for a particular symbol."""),
            backstory=dedent(f"""Expert in creating markdown reports. The best at using tools to gather data from an API. You retrieve **EVERY** metric from QuickFS when asked and never miss a single one."""),
            tools=[
                ExtractionTools.parse_string, 
                QuickFSDataFetchingTools.get_metric_data_from_quickfs],
            verbose=True,
            llm=self.llm,
        )

    def chart_creator(self):
        return Agent(
            role="Chart Creator",
            goal=dedent(f"""Create a chart of the data provided using the tool."""),
            backstory=dedent(f"""Expert in creating charts. You are known for receiving a list of data points and meticulously creating an accurate chart. You must use the tool provided. """),
            tools=[
                ChartingTools.create_chart
            ] ,
            verbose=True,
            llm=self.llm,
        )

    def markdown_writer(self):
        return Agent(
            role="Data Report Creator",
            goal=dedent(f"""Use *.png files in same directory to add the correct syntax a markdown file."""),
            backstory=dedent(f"""Expert in writing text inside a markdown file. You take a text input and write the contents to a markdown file in the same directory. You always add a new line after inserting into the markdown file. **YOU USE MARKDOWN SYNTAX AT ALL TIMES NO MATTER WHAT** YOU NEVER INSERT ANYTHING INTO THE report.md FILE THAT ISN'T MARKDOWN SYNTAX. """),
            tools=[MarkdownTools.write_text_to_markdown_file],
            verbose=True,
            llm=self.llm,
        )



     