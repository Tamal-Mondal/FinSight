import os
from crewai import Agent

from stock_analysis.tools.browser_tools import BrowserTools
from stock_analysis.tools.calculator_tools import CalculatorTools
from stock_analysis.tools.search_tools import SearchTools
from stock_analysis.tools.sec_tools import SECTools

from langchain.tools.yahoo_finance_news import YahooFinanceNewsTool

from langchain_openai import ChatOpenAI
# from langchain_mistralai.chat_models import ChatMistralAI
# from langchain_anthropic import ChatAnthropic

llm = ChatOpenAI(model="NousResearch/Nous-Hermes-2-Mixtral-8x7B-SFT",
                 temperature=0.7,
                 api_key="ec62094143cbf9e978aa4b62b7ff1698a67a40081475353b65bf9e10bf7b94ea",
                 base_url="https://api.together.xyz")

class StockAnalysisAgents():
  
  def research_analyst(self):
    return Agent(
      role='Staff Research Analyst',
      goal="""Being the best at gather, interpret data for any company and amaze your customer with it""",
      backstory="""Known as the BEST research analyst, you're skilled in sifting through news, company announcements, 
                and market sentiments. Now you're responsible for market research on a super 
                important customer""",
      verbose=True,
      llm = llm,
      tools=[
        BrowserTools.scrape_and_summarize_website,
        SearchTools.search_internet,
        SearchTools.search_news,
        YahooFinanceNewsTool(),
        SECTools.search_10q,
        SECTools.search_10k
      ]
  )
  
  def financial_analyst(self):
    return Agent(
      role='Senior Financial Analyst',
      goal="""Impress all customers with your financial data and market trends analysis""",
      backstory="""The most seasoned financial analyst with lots of expertise in stock market analysis and investment
                strategies. You are a critical thinker and can extract effective insights from all the financial data that 
                investment advisors use to make important decisions.""",
      verbose=True,
      llm = llm,
      tools=[
        BrowserTools.scrape_and_summarize_website,
        SearchTools.search_internet,
        CalculatorTools.calculate,
        SECTools.search_10q,
        SECTools.search_10k
      ]
    )

  def investment_advisor(self):
    return Agent(
      role='Senior Investment Advisor',
      goal="""Impress your customers with a full analysis of stocks and complete investment recommendations that are backed by numbers.""",
      backstory="""You're the most experienced investment advisor and you combine various analytical insights to formulate
                strategic investment advice that are backed by numbers. You are now working for a super important customer whom 
                you need to impress. You MUST have to keep the answers crisp and as per the specified format.""",
      verbose=True,
      llm = llm,
      tools=[
        BrowserTools.scrape_and_summarize_website,
        SearchTools.search_internet,
        SearchTools.search_news,
        CalculatorTools.calculate,
        YahooFinanceNewsTool()
      ],
      response_template = """Example Output about a company stocks
        
                          VERDICT: buy
                          RISK: medium
                          GROWTH POTENTIAL: CAGR of 20% over 5 years
                          ADVICE: This growth is primarily driven by increased demand for the electric 
                                  vehicles. The financial statements show a strong balance sheet with a cash and cash equivalent position 
                                  of $17.5 billion...but its profit margin is still lower than many established automakers."""
    )
    
  def senior_editor(self):
    writer = Agent(
        role='Senior Editor',
        goal='Writes professional quality articles and answers based on financial analysis that follows spcific format',
        backstory="""You are a details-oriented senior editor at the Wall Street Journal known for your insightful and engaging 
                  articles. You transform complex concepts into factual and impactful narratives. You MUST have to keep the answers 
                  crisp and as per the specified format.""",
        verbose=True,
        llm=llm,
        response_template = """Example Output about a company stocks
        
                          VERDICT: buy
                          RISK: medium
                          GROWTH POTENTIAL: CAGR of 20% over 5 years
                          ADVICE: This growth is primarily driven by increased demand for the electric 
                                  vehicles. The financial statements show a strong balance sheet with a cash and cash equivalent position 
                                  of $17.5 billion...but its profit margin is still lower than many established automakers."""
        )
    return writer