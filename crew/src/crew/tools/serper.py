from crewai_tools.tools import SerperDevTool
from dotenv import load_dotenv
import os

load_dotenv()
os.getenv("SERPER_API_KEY")

search_tool = SerperDevTool()