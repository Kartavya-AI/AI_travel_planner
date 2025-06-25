import asyncio
from agno.agent import Agent
from agno.models.google import Gemini
from agno.tools.mcp import MCPTools
import json

def airbnb_search(query: str) -> str:
    """
    Search for Airbnb accommodations using natural language query.
    
    Args:
        query (str): Search query for accommodations (e.g., "Best rooms in Delhi under 2000 per night")
    
    Returns:
        str: Search results with accommodation details
    """
     #{'query': 'find the best hotels in delhi under 1000 per night'}
    json.dumps({'query': query})
    return asyncio.run(_async_airbnb_search(query))


async def _async_airbnb_search(query: str) -> str:
    """Internal async function to handle MCP Airbnb search"""
    try:
        async with MCPTools(
            "npx -y @openbnb/mcp-server-airbnb --ignore-robots-txt"
        ) as mcp_tools:
            agent = Agent(
                model=Gemini(id="gemini-2.0-flash", api_key="AIzaSyA_RithdgsWoUpSqwpzIPj_n-xvWrUGw3Q"),
                tools=[mcp_tools],
                markdown=True,
            )

            response_stream = await agent.arun(query, stream=True)
            # Collect response text
            response_text = ""
            async for chunk in response_stream:
                if hasattr(chunk, 'content'):
                    response_text += str(chunk.content)
                elif isinstance(chunk, str):
                    response_text += chunk
            
            return response_text if response_text else "No results found"
            
    except Exception as e:
        return f"Error searching Airbnb: {str(e)}"

if __name__ == "__main__":
    # Test the tool
    result = airbnb_search("Best rooms in Delhi under 2000 per night")
    print(result)