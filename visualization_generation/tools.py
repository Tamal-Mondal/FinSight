import os
import json
from dotenv import load_dotenv
from quickfs import QuickFS
from langchain.tools import tool
from pydantic.v1 import BaseModel, validator, Field
from typing import List
import random
import matplotlib.pyplot as plt
load_dotenv()

class ExtractionTools():
    @tool("Extract symbol and metrics")
    def parse_string(data:str):
        """
        Useful to extract the relevant information from the input string. Parses string and extracts the symbol and all of the relevant metrics requested.
        """
        words = data.split()
        symbol = words[0]
        result_list = [{"symbol":symbol, "metric":metric} for metric in words[1:]]

        return result_list 

class QuickFSDataFetchingTools():
    @tool("Retrieve metric data from QuickFS API")
    def get_metric_data_from_quickfs(symbol, metric: str):
        """
        Useful to retrieve data from the QuickFS API based on the given symbol and metric.

        :param symbol: str, only one symbol
        :param metric: str, only one metric
        :return value: dictionary, A dictionary having the metric and data
        """
        # api_key = os.environ["QUICKFS_API_KEY"]
        # print("QUICKFS_API_KEY: "+ api_key)
        client = QuickFS("05e444903edd0d799288e5ef8ce2c67dec042965")
      
        data = client.get_data_range(symbol=f'{symbol}:US', metric=metric, period='FY-9:FY')

        return {"metric": metric, "data": data}

class CreateChartInput(BaseModel):
    metric: str
    data: List[float]

class CreateChartOutput(BaseModel):
    file_path: str

class ChartingTools():
    @tool("Create a chart of the data")
    def create_chart(data) -> CreateChartOutput:
        """
        Creates a bar chart graphic based on the provided metric and data.

        Parameters:
        - data (Dictionary): A dictionary having the metric name and data

        Returns:
        - file_path (str): The file path to the saved chart image.
        """
        years = list(range(len(data["data"])))

        # Generate a random color for all bars
        bar_color = f'#{random.randint(0, 0xFFFFFF):06x}'

        fig, ax = plt.subplots()
        ax.bar(years, data["data"], color=bar_color)
        ax.set_xlabel('Years')
        ax.set_title(data["metric"])

        # Save the figure to the current directory
        metric = data["metric"]
        file_path = f"./{metric.replace(' ', '_')}_chart.png"
        fig.savefig(file_path, format='png')
        plt.close(fig)  # Close the Matplotlib figure to free resources

        return CreateChartOutput(file_path=file_path)


class MarkdownTools():
    @tool("Write text to markdown file")
    def write_text_to_markdown_file(text: str) -> str:
        """Useful to write markdown text in a *.md file.
           The input to this tool should be a string representing what should used to create markdown syntax. Takes the location of the file as a string and creates the correct syntax thats compatible with an .md file eg report.md

            **Example** Writes `![](fcf_chart.png)` to report.md file.
           
           :param text: str, the string to write to the file
           """
        try:
            markdown_file_path = r'report.md'
            
            with open(markdown_file_path, 'w') as file:
                file.write(text)
            
            return f"File written to {markdown_file_path}."
        except Exception:
            return "Something has gone wrong writing images to markdown file."