import os
from crewai import Agent, Task, Crew, Process
from langchain_openai import ChatOpenAI
from langchain_cohere import ChatCohere
from langchain.llms import OpenAI

from langchain_community.tools import DuckDuckGoSearchRun
from langchain_community.tools import BraveSearch
from report_generation.tools.sec_tools_new import SECTools
#from tools.openbb_tools import OpenBBTools

# from langchain_mistralai.chat_models import ChatMistralAI
# from langchain_anthropic import ChatAnthropic
from dotenv import load_dotenv

from textwrap import dedent

load_dotenv()

# Get BRAVE_API_KEY from environment variables
# api_key = os.getenv('BRAVE_API_KEY')

#search_tool = BraveSearch.from_api_key(api_key=api_key,
#                                       search_kwargs={"count": 3})
#openbb_tool = OpenBBTools()

#sec_tool = SecTools()

def getLLM():
    # Create a chat model
    # Using service http://together.ai

    #model_name = "Qwen/Qwen1.5-14B-Chat"
    #model_name = "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"
    #model_name = "NousResearch/Nous-Hermes-2-Mixtral-8x7B-SFT"
    #model_name = "meta-llama/Meta-Llama-3-70B-Instruct-Lite"
    model_name = "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo"
    llm = ChatOpenAI(model=model_name,
                 temperature=0.7,
                 api_key="d1a8e935548aec33569f825c0d297a26733226000b730c62e08f0c6945740055",
                 base_url="https://api.together.xyz")
    
    # llm = OpenAI(model_name="gpt-3.5-turbo", openai_api_key=os.getenv("OPENAI_API_KEY"))
    # llm = ChatOpenAI(model="gpt-3.5-turbo", api_key=os.getenv("OPENAI_API_KEY"))
    
    # anthropic_model = Anthropic(api_key=os.getenv('ANTHROPIC_API_KEY'), model_name="claude-v1")
    # cohere_model = ChatCohere(max_tokens=150, temperature=0.7)

    #llm_writer = ChatOpenAI(model="teknium/OpenHermes-2p5-Mistral-7B",
    #                        temperature=0.7,
    #                        base_url="https://api.together.xyz")

    #llm = ChatMistralAI(model="mistral-medium", temperature=0.7)
    #llm_writer = ChatAnthropic(model='claude-3-haiku-20240307')
    
    return llm

def getAgents(llm):
    
    # Define your agents with roles and goals
    researcher = Agent(
        role='Senior Research Analyst',
        goal='Gather and uncover insights from latest 10K, 10Q reports of the company',
        backstory="""You have worked as a research analyst at Goldman Sachs for past 10 years, focusing on fundamental research for 
                  tech companies""",
        verbose=True,
        allow_delegation=False,
        tools=[SECTools.search_10q, SECTools.search_10k],
        llm=llm)

    visionary = Agent(
        role='Visionary',
        goal='Deep thinking on the implications of an analysis',
        backstory="""you are a visionary technologist with a keen eye for identifying emerging trends and predicting their potential 
                  impact on various industries. Your ability to think critically and connect seemingly disparate dots allows you to 
                  anticipate disruptive technologies and their far-reaching implications.""",
        verbose=True,
        allow_delegation=False,
        llm=llm)

    writer = Agent(
        role='Senior Editor',
        goal='Writes professional quality articles that are easy to understand',
        backstory="""You are a details-oriented senior editor at the Wall Street Journal known for your insightful and engaging 
                  articles. You transform complex concepts into factual and impactful narratives.""",
        verbose=True,
        llm=llm,
        allow_delegation=True)
    
    return [researcher, visionary, writer]

def getTasks(company, year, form_type, quarter, researcher, visionary, writer):
    
    # Create tasks for your agents
    task1 = Task(
        description=
        f"""
        Gather information and conduct a comprehensive analysis of {company} for year {year} using the SEC filing of {form_type if quarter == "" else form_type + " for " + quarter}.
        
        The analysis should include the following key points:

        Business Overview: Briefly describe {company}'s business model, its products and services, and its target market.

        Risk Factors: Identify and discuss the major risk factors that {company} has disclosed in its {form_type} filing.

        Management's Discussion and Analysis (MD&A): Summarize the key points from the MD&A section, including any significant changes in operations, financial condition, or liquidity.

        Competitive Landscape: Discuss {company}'s competitive position in its industry and how it compares to its major competitors.

        Future Outlook: Based on the information in the {form_type} filing and your analysis, provide a brief outlook on {company}'s future performance.

        Please ensure that all information is sourced from {company}'s SEC {form_type} filing {"" if quarter == "" else " for " + quarter} of year {year} and that the analysis is unbiased and factual.""",
        expected_output="Full analysis report in bullet points",
        agent=researcher)

    task2 = Task(
        description=
        f"""
        Using the insights provided by the Senior Research Analyst, think through deeply the future implications of the points that are made. 
        
        Consider the following questions as you craft your response:

        What are the current limitations or pain points that this technology mentioned in the Senior Research Analyst report could address?

        How might this technology disrupt traditional business models and create new opportunities for innovation?

        What are the potential risks and challenges associated with the adoption of this technology, and how might they be mitigated?

        How could this technology impact consumers, employees, and society as a whole?

        What are the long-term implications of this technology, and how might it shape the future of the industry?

        Provide a detailed analysis of the technology's potential impact, backed by relevant examples, data, and insights. Your response should demonstrate your ability to think strategically, anticipate future trends, and articulate complex ideas in a clear and compelling manner.""",
        expected_output="Detailed analysis report with deeper insights in implications",
        agent=visionary)

    task3 = Task(
        description=
            f"""
            Using the insights provided by the Senior Research Analyst and Visionary, please craft an expertly styled 
            report (one page) that is targeted towards the investor community. Make sure to also include the long-term 
            implications insights that your co-worker, Visionary, has shared.
    
            Please ensure that the report (one page) is written in a professional tone and style, and that all information is sourced 
            from {company}'s SEC {form_type} filing {"" if quarter == "" else " for " + quarter} of year {year}. 
            
            Write a one-page report in a format and style worthy to be published in the Wall Street Journal. 
            Always start the report with a meaningful and interesting tagline.""",
        # expected_output=
        #     f"""A detailed comprehensive report based on the research and insights from the Senior Research Analyst and Visionary""",
        agent=writer)
    
    return [task1, task2, task3]

def generateReport(company, year, form_type, quarter):
    
    #print("\nSEC API KEY: " + os.environ['SEC_API_API_KEY'])
    llm = getLLM()
    researcher, visionary, writer = getAgents(llm)
    task1, task2, task3 = getTasks(company, year, form_type, quarter, researcher, visionary, writer)
    
    # Instantiate your crew with a sequential process
    crew = Crew(
        agents = [researcher, visionary, writer],
        tasks = [task1, task2, task3],
        verbose=2,  # You can set it to 1 or 2 to different logging levels
    )

    # Get your crew to work!
    result = crew.kickoff()
    return result
