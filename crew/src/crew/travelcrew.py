from crewai import Agent, Crew, Process, Task, LLM
from crewai.project import CrewBase, agent, crew, task
from dotenv import load_dotenv
from src.crew.tools.calculator_tool import CalculatorTools
from src.crew.tools.scrape_website import ScrapeWebsiteTool
from src.crew.tools.serper import SerperDevTool

import os
load_dotenv()

os.getenv("GEMINI_API_KEY")

# Initialize Gemini model
llm = LLM(model="gemini/gemini-2.0-flash")

# Instantiate tools
search_tool = SerperDevTool()
scrape_tool = ScrapeWebsiteTool()
calculator_tool = CalculatorTools.calculate

@CrewBase
class TravelCrew():
    """Travel planning crew with specialized agents"""

    agents_config = 'config/agents.yaml'
    tasks_config = 'config/tasks.yaml'

    @agent
    def city_selector_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['city_selector_agent'],
            llm=llm,
            tools=[search_tool, scrape_tool]
        )

    @agent
    def local_expert_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['local_expert_agent'],
            llm=llm,
             max_iter=2,
            tools=[search_tool, scrape_tool]
        )

    @agent
    def travel_concierge_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['travel_concierge_agent'],
            llm=llm,
            max_iter=2,
            tools=[search_tool, scrape_tool, calculator_tool]
        )

    @agent
    def accommodation_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['accommodation_agent'],
            llm=llm,
            max_iter=2,
            tools=[search_tool, scrape_tool, calculator_tool]
        )

    @agent
    def food_expert_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['food_expert_agent'],
            llm=llm,
            max_iter=2,
            tools=[search_tool, scrape_tool]
        )

    @agent
    def interest_specialist_agent(self) -> Agent:
        return Agent(
            config=self.agents_config['interest_specialist_agent'],
            llm=llm,
            max_iter=2,
            tools=[search_tool, scrape_tool]
        )
    @agent
    def final_itenarary_agent(self) -> Agent:
            return Agent(
                config=self.agents_config['final_itinerary_agent'],
                llm=llm,
                max_iter=2,
                tools=[search_tool, scrape_tool]
            )
    @task
    def city_selection_task(self) -> Task:  
        return Task(
            config=self.tasks_config["city_selection_task"],
            agent=self.city_selector_agent(),
        )

    @task
    def local_expert_task(self) -> Task:
        return Task(
            config=self.tasks_config["local_expert_task"],
            agent=self.local_expert_agent(),
        )

    @task
    def travel_concierge_task(self) -> Task:    
        return Task(
            config=self.tasks_config["travel_concierge_task"],
            agent=self.travel_concierge_agent(),
        )

    @task
    def accommodation_task(self) -> Task:
        return Task(
            config=self.tasks_config["accommodation_task"],
            agent=self.accommodation_agent(),
        )

    @task
    def food_expert_task(self) -> Task:
        return Task(
            config=self.tasks_config["food_expert_task"],
            agent=self.food_expert_agent(),
        )

    @task
    def interest_specialist_task(self) -> Task:
        return Task(
            config=self.tasks_config["interest_specialist_task"],
            agent=self.interest_specialist_agent(),
        )
    @task
    def final_itinerary_task(self) -> Task:
        return Task(
            config=self.tasks_config["final_itinerary_task"],
            agent=self.final_itenarary_agent(),
        )

    @crew
    def crew(self) -> Crew:
        """Creates the travel planning crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True
        )
