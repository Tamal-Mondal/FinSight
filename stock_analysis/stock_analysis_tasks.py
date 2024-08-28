from crewai import Task
from textwrap import dedent

class StockAnalysisTasks():
    def research(self, agent, company):
        return Task(description=dedent(f"""
              The company selected by customer: {company}
              
              Collect and summarize recent news articles, press
              releases, and market analyses related to the stock and
              its industry.
              
              Pay special attention to any significant events, market
              sentiments, and analysts' opinions. Also include upcoming 
              events like earnings and others.
        
              Your final answer MUST be a report that includes a
              comprehensive summary of the latest news, any notable
              shifts in market sentiment, and potential impacts on 
              the stock.
              
              Make sure to use the most recent data as possible. 
              Also make sure to return the stock ticker.
              
              {self.__tip_section()}
      """),
      agent=agent
    )

    def financial_analysis(self, agent, company): 
        return Task(description=dedent(f"""
              The company selected by customer: {company}
              
              Conduct a thorough analysis of the stock's financial
              health and market performance. 
              This includes examining key financial metrics such as
              P/E ratio, EPS growth, revenue trends, and 
              debt-to-equity ratio. 
              Also, analyze the stock's performance in comparison 
              to its industry peers and overall market trends.

              Your final report MUST expand on the summary provided
              but now including a clear assessment of the stock's
              financial standing, its strengths and weaknesses, 
              and how it fares against its competitors in the current
              market scenario.
              
              Make sure to use the most recent data possible.
              
              {self.__tip_section()}
      """),
      agent=agent
    )

    def filings_analysis(self, agent, company):
        return Task(description=dedent(f"""
              The company selected by customer: {company}
              
              Analyze the latest 10-Q and 10-K filings from EDGAR for
              the stock in question. 
              Focus on key sections like Management's Discussion and
              Analysis, financial statements, insider trading activity, 
              and any disclosed risks.
              Extract relevant data and insights that could influence
              the stock's future performance.

              Your final answer must be an expanded report that now
              also highlights significant findings from these filings,
              including any red flags or positive indicators for
              your customer.
              
              Make sure to use the most recent 10K and 10Q filings data.
              {self.__tip_section()}
      """),
      agent=agent
    )

    def recommend(self, agent, company):
        return Task(
            description=dedent(
                      f"""
              The company selected by customer: {company}
              
              Review and synthesize the analyses provided by the
              Financial Analyst and the Research Analyst.
              Combine these insights to form a comprehensive
              investment recommendation. 
              
              You MUST Consider all aspects, including financial
              health, risks, market sentiment, and qualitative data from
              EDGAR filings along with insider trading activity, and 
              upcoming events like earnings.

              Your final answer MUST be a detailed report that would include VERDICT (buy, sale, not sure), 
              RISK (low, medium, high), GROWTH POTENTIAL (in % in next 5 years), and 
              ADVICE (it's general advice on company health and future prospects that are backed by numbers).
              
              {self.__tip_section()}
            """),
            # expected_output="""
            #             VERDICT: buy
            #             RISK: medium
            #             GROWTH POTENTIAL: CAGR of 20% over 5 years
            #             ADVICE: This growth is primarily driven by increased demand for the electric 
            #                     vehicles. The financial statements show a strong balance sheet with a cash and cash equivalent position 
            #                     of $17.5 billion. However, one red flag that stands out is the continuous high volume of insider 
            #                     selling, which could be a cause for concern for potential investors. In terms of its industry peers, 
            #                     company's growth rate outpaces most of its competitors, but its profit margin is still lower than many 
            #                     established automakers.
            #             """,
            agent=agent
        )

    def write(self, agent, previous_tasks):
        return Task(
            description=dedent(
                f"""
        Use the recommendation report generated by senior investment advisor and write top quality investment guide.

        You MUST extract the information needed to answer in 4 sections which are VERDICT (buy, sale, not sure), 
        RISK (low, medium, high), GROWTH POTENTIAL (in % in next 5 years), and 
        ADVICE (it's general advice in maximum 5 sentences on company health and future prospects that are backed by numbers).
        
        Example Output:
        
        VERDICT: buy
        RISK: medium
        GROWTH POTENTIAL: CAGR of 20% over 5 years
        ADVICE: This growth is primarily driven by increased demand for the electric 
                vehicles. The financial statements show a strong balance sheet with a cash and cash equivalent position 
                of $17.5 billion...but its profit margin is still lower than many established automakers.
        
        {self.__tip_section()}
      """
            ),
            expected_output="""
                        VERDICT: buy
                        RISK: medium
                        GROWTH POTENTIAL: CAGR of 20% over 5 years
                        ADVICE: This growth is primarily driven by increased demand for the electric 
                                vehicles. The financial statements show a strong balance sheet with a cash and cash equivalent position 
                                of $17.5 billion. However, one red flag that stands out is the continuous high volume of insider 
                                selling, which could be a cause for concern for potential investors. In terms of its industry peers, 
                                company's growth rate outpaces most of its competitors, but its profit margin is still lower than many 
                                established automakers.
                        """,
            agent=agent
        )

    def __tip_section(self):
        return "If you do your BEST WORK, I'll give you a $10,000 commission!"
