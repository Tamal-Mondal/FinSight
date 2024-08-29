from crewai import Agent
from crewai import Task
from crewai import Crew, Process
# from crewai_tools import SerperDevTool

from qna_bot.tools.calculator_tools import CalculatorTools
from qna_bot.tools.search_tools import SearchTools
from qna_bot.tools.sec_tools import SECTools

from langchain_openai import ChatOpenAI
from textwrap import dedent

def getLLM():
    #model_name = "Qwen/Qwen1.5-14B-Chat"
    #model_name = "meta-llama/Meta-Llama-3.1-8B-Instruct-Turbo"
    #model_name = "NousResearch/Nous-Hermes-2-Mixtral-8x7B-SFT"
    #model_name = "meta-llama/Meta-Llama-3-70B-Instruct-Lite"
    model_name = "meta-llama/Meta-Llama-3.1-70B-Instruct-Turbo"
    llm = ChatOpenAI(model=model_name,
                     temperature=0.7,
                     api_key="ec62094143cbf9e978aa4b62b7ff1698a67a40081475353b65bf9e10bf7b94ea",
                     base_url="https://api.together.xyz")
    return llm

def getAgents(llm):
    
    # Senior Chat Manager
    manager_agent = Agent(
        role='Senior Chat Manager',
        goal='Understand the question, utilize the past questions-answers, and coordinate with Researcher and Q&A Specialist as needed to answer the current question',
        backstory=(
            """You have decades of experience managing people and resolving the query quickly, which involves everyone's help. You 
            specialize in critical thinking and coordination among agents. You are sharp at remembering past conversations and resolving 
            current query accordingly"""
        ),
        memory=True,
        verbose=True,
        llm=llm,
        allow_delegation=True
    )

    # Researcher Agent for complex queries
    researcher_agent = Agent(
        role='Senior Researcher',
        goal='Collect and analyse 10K or 10Q reports of a company to answer complex user queries',
        backstory=(
            """You are skilled at fetching and conducting in-depth research on 10K and 10Q reports 
            to uncover precise and accurate information about a company."""
        ),
        tools=[SECTools.search_10k, SECTools.search_10q],
        memory=True,
        verbose=True,
        llm=llm
    )

    # Q&A Agent
    qa_agent = Agent(
        role='Senior Q&A Specialist',
        goal='Answer user questions accurately and efficiently',
        backstory=(
            "You are an expert in providing clear and concise answers to a wide range of finance related questions."
        ),
        tools=[CalculatorTools.calculate],
        memory=True,
        verbose=True,
        llm=llm
    )
    
    return [manager_agent, researcher_agent, qa_agent]

def getTasks(company, year, form_type, quarter, question, researcher_agent, qa_agent):
    
    # Research Task for complex queries
    research_task = Task(
        description=(
            f"""User's query is given below, fetch the required 10K/10Q reports and conduct in-depth research to find detailed 
            information on the user's question. The question is based on {company}'s 
            SEC {form_type} filing {"" if quarter == "" else " for " + quarter} of year {year}.
                
            Company: {company}
            Year: {year}
            Filing: {form_type if quarter == "" else form_type + " for " + quarter}
            Question: {question}"""
        ),
        expected_output="A detailed and accurate report on the query that Q&A specialist can use to generate final answer.",
        agent=researcher_agent,
    )

    # Answer Question Task
    answer_task = Task(
        description=(
            f"""User's query is given below, find the best possible answer from the research conducted by Senior Researcher, 
            and return it. The question is based on {company}'s SEC {form_type} filing {"" if quarter == "" else " for " + quarter} 
            of year {year}.
                
            Company: {company}
            Year: {year}
            Filing: {form_type if quarter == "" else form_type + " for " + quarter}
            Question: {question}"""
        ),
        expected_output="A concise and accurate answer to the user's question.",
        agent=qa_agent,
    )

    return [research_task, answer_task]

def answerQuestion(company, year, form_type, quarter, question):
    llm = getLLM()
    manager_agent, researcher_agent, qa_agent = getAgents(llm)
    research_task, answer_task = getTasks(company, year, form_type, quarter, question, researcher_agent, qa_agent)

    research_qa_crew = Crew(
        agents=[researcher_agent, qa_agent],
        tasks=[research_task, answer_task],
        process=Process.sequential  # Or Process.parallel if you want both tasks to run simultaneously
    )

    # Start the crew
    result = research_qa_crew.kickoff()
    return result

def chatContiniously():
    
    while True:
    
        # Example question
        question = "What the future looks like for NVIDIA from the latest 10K/10Q reports?"
        question = input(dedent("""\nWhat is your question?\n"""))
        
        llm = getLLM()
        manager_agent, researcher_agent, qa_agent = getAgents(llm)
        research_task, answer_task = getTasks("", "", "", "", question, manager_agent, researcher_agent, qa_agent)

        research_qa_crew = Crew(
            agents=[researcher_agent, qa_agent],
            tasks=[research_task, answer_task],
            process=Process.sequential  # Or Process.parallel if you want both tasks to run simultaneously
        )

        # Start the crew
        result = research_qa_crew.kickoff()
        print("\n============================= FINAL ANSWER ======================================\n")
        print(result)
