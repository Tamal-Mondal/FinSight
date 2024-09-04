import os
from crewai import Crew
from textwrap import dedent

from stock_analysis.stock_analysis_agents import StockAnalysisAgents
from stock_analysis.stock_analysis_tasks import StockAnalysisTasks

from dotenv import load_dotenv
load_dotenv()

class FinancialCrew:
    def __init__(self, company):
        self.company = company

    def run(self):
        agents = StockAnalysisAgents()
        tasks = StockAnalysisTasks()

        research_analyst_agent = agents.research_analyst()
        financial_analyst_agent = agents.financial_analyst()
        investment_advisor_agent = agents.investment_advisor()
        # editor_agent = agents.senior_editor()

        research_task = tasks.research(research_analyst_agent, self.company)
        financial_task = tasks.financial_analysis(financial_analyst_agent, self.company)
        filings_task = tasks.filings_analysis(financial_analyst_agent, self.company)
        recommend_task = tasks.recommend(investment_advisor_agent, self.company)
        # writing_task = tasks.write(editor_agent, [recommend_task])

        crew = Crew(
            agents=[
                research_analyst_agent,
                financial_analyst_agent,
                investment_advisor_agent,
            ],
            tasks=[research_task, financial_task, filings_task, recommend_task],
            verbose=bool(int(os.environ["LOG_LEVEL"]))
        )

        result = crew.kickoff()
        return result

def analyseStock(company):
  financial_crew = FinancialCrew(company)
  result = financial_crew.run()
  return result
