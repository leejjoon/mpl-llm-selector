import os
from typing import List
import asyncio
from pydantic import BaseModel, Field
from pydantic_ai import Agent
from pydantic_ai.agent import AgentRunResult
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# It's recommended to use a .env file to store your API key
# Create a .env file in the same directory as this script and add the following line:
# GOOGLE_API_KEY="your_google_api_key"

# Ensure the GOOGLE_API_KEY is set
if "GOOGLE_API_KEY" not in os.environ:
    print("Error: GOOGLE_API_KEY environment variable not set.")
    exit()

# Define the desired output structure using Pydantic
class StringListOutput(BaseModel):
    """A Pydantic model to represent a list of strings."""
    items: List[int] = Field(..., description="A list of strings as the response.")


def get_full_query(role: str,
                   instruction: str,
                   context: str, question: str) -> str:

    # Combine context and question into a single prompt for the model
    full_query = f"""
Role:

{role}


Instruction:

{instruction}


Context:
{context}


Question:

{question}


    """

    return full_query


# Define the main function to interact with the AI
async def get_response_from_gemini(full_query: str) -> StringListOutput:
    """
    Sends a query with context to the Gemini 2.5 Pro model and returns a list of strings.

    Args:
        context: The context or background information for the query.
        question: The specific question to ask based on the context.

    Returns:
        An instance of StringListOutput containing the list of strings.
    """
    # Corrected the model name to 'gemini-2.5-pro'
    # You can specify different models from the Gemini family.
    # For example: 'gemini-pro', 'gemini-1.5-pro-latest'
    agent = Agent('gemini-2.5-pro')

    # Corrected the parameter from 'result_type' to 'output_type'
    result: AgentRunResult = await agent.run(full_query, output_type=StringListOutput)

    # The result object is a wrapper; the actual Pydantic model is in the 'output' attribute.
    return result.output


role = "You are a plot analyzer. You analyze various properties of the plot and try to answer the question from the user,"

instruction = """A user want to query the artists of specific properties. You
will answer the list of artist id defined in the 'Properties of Artists' table.

Here are some notes you need to be aware,

- All x & y coordinates are in data coordinates.
- Properties of Artists table include bounding-box of each artist (xmin, xmax, ymin
  and ymax).
- For categorical plots, x- or y-labels often represents the category. However, a category may span a range of values in the numerical coordinate not a specific value. For example, given apple at 1, orange at 2 and banana at 3, apple means 0.5 to 1.5, orange from 1.5 to 2.5 and banana from 2.5 to 3.5.
"""

async def _query(full_query):

    try:

        response = await get_response_from_gemini(full_query)
        # print("\nReceived response:")
        # for i, item in enumerate(response.items):
        #     print(f"{i + 1}. {item}")

        return response
    except Exception as e:
        print(f"\nAn error occurred: {e}")


async def async_query(plot_properties, q):

    full_query = get_full_query(role, instruction, plot_properties, q)

    # Run the asynchronous main function
    response = await _query(full_query)

    return response


def query(plot_properties, q):

    response = asyncio.run(async_query(plot_properties, q))

    return response
