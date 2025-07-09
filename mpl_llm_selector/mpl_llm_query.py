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

plot_properties_example = """
## Data limits of the axes

x = (-0.5, 3.5)
y = (0.6829999999999998, 53.197)

## Properties of Artists

|         xmin |         ymin |         xmax |         ymax | kind    | color   | facecolor   | edgecolor   |   linewidth | label      |              id | selector   |
|-------------:|-------------:|-------------:|-------------:|:--------|:--------|:------------|:------------|------------:|:-----------|----------------:|:-----------|
| -0.2         | 10.34        | -0.2         | 13.51        | lines   | #6f6f6f |             |             |           1 | _nolegend_ | 126196268825968 | lines[0]   |
| -0.2         | 19.81        | -0.2         | 28.44        | lines   | #6f6f6f |             |             |           1 | _nolegend_ | 126196270496512 | lines[1]   |
| -0.3         | 10.34        | -0.1         | 10.34        | lines   | #6f6f6f |             |             |           1 | _nolegend_ | 126196269007552 | lines[2]   |
| -0.3         | 28.44        | -0.1         | 28.44        | lines   | #6f6f6f |             |             |           1 | _nolegend_ | 126196269008272 | lines[3]   |
| -0.4         | 16.47        |  2.22045e-16 | 16.47        | lines   | #6f6f6f |             |             |           1 | _nolegend_ | 126196269008944 | lines[4]   |
| -0.233661    | 32.087       | -0.166339    | 43.703       | lines   | #000000 |             |             |           1 | _nolegend_ | 126196269009664 | lines[5]   |
|  0.8         |  5.75        |  0.8         | 11.69        | lines   | #6f6f6f |             |             |           1 | _nolegend_ | 126196269010720 | lines[6]   |
|  0.8         | 18.665       |  0.8         | 28.97        | lines   | #6f6f6f |             |             |           1 | _nolegend_ | 126196269011440 | lines[7]   |
|  0.7         |  5.75        |  0.9         |  5.75        | lines   | #6f6f6f |             |             |           1 | _nolegend_ | 126196269012160 | lines[8]   |
|  0.7         | 28.97        |  0.9         | 28.97        | lines   | #6f6f6f |             |             |           1 | _nolegend_ | 126196269012928 | lines[9]   |
|  0.6         | 13.42        |  1           | 13.42        | lines   | #6f6f6f |             |             |           1 | _nolegend_ | 126196269013648 | lines[10]  |
|  0.766339    | 39.577       |  0.833661    | 40.763       | lines   | #000000 |             |             |           1 | _nolegend_ | 126196269014320 | lines[11]  |
|  1.8         |  3.07        |  1.8         | 13.405       | lines   | #6f6f6f |             |             |           1 | _nolegend_ | 126196269015520 | lines[12]  |
|  1.8         | 26.7925      |  1.8         | 44.3         | lines   | #6f6f6f |             |             |           1 | _nolegend_ | 126196269016240 | lines[13]  |
|  1.7         |  3.07        |  1.9         |  3.07        | lines   | #6f6f6f |             |             |           1 | _nolegend_ | 126196269016912 | lines[14]  |
|  1.7         | 44.3         |  1.9         | 44.3         | lines   | #6f6f6f |             |             |           1 | _nolegend_ | 126196269017680 | lines[15]  |
|  1.6         | 20.39        |  2           | 20.39        | lines   | #6f6f6f |             |             |           1 | _nolegend_ | 126196269018304 | lines[16]  |
|  1.76634     | 50.217       |  1.83366     | 51.403       | lines   | #000000 |             |             |           1 | _nolegend_ | 126196269018976 | lines[17]  |
|  2.8         |  7.25        |  2.8         | 17.165       | lines   | #6f6f6f |             |             |           1 | _nolegend_ | 126196269020032 | lines[18]  |
|  2.8         | 32.375       |  2.8         | 45.35        | lines   | #6f6f6f |             |             |           1 | _nolegend_ | 126196269020656 | lines[19]  |
|  2.7         |  7.25        |  2.9         |  7.25        | lines   | #6f6f6f |             |             |           1 | _nolegend_ | 126196269021328 | lines[20]  |
|  2.7         | 45.35        |  2.9         | 45.35        | lines   | #6f6f6f |             |             |           1 | _nolegend_ | 126196269022000 | lines[21]  |
|  2.6         | 23.1         |  3           | 23.1         | lines   | #6f6f6f |             |             |           1 | _nolegend_ | 126196269022768 | lines[22]  |
| -1.17882     | -7.41204     | -1.1115      | -6.22596     | lines   | #000000 |             |             |           1 | _nolegend_ | 126196269187344 | lines[23]  |
|  0.2         |  7.51        |  0.2         | 11.69        | lines   | #6f6f6f |             |             |           1 | _nolegend_ | 126196269190320 | lines[24]  |
|  0.2         | 20.27        |  0.2         | 29.8         | lines   | #6f6f6f |             |             |           1 | _nolegend_ | 126196269188256 | lines[25]  |
|  0.1         |  7.51        |  0.3         |  7.51        | lines   | #6f6f6f |             |             |           1 | _nolegend_ | 126196269189024 | lines[26]  |
|  0.1         | 29.8         |  0.3         | 29.8         | lines   | #6f6f6f |             |             |           1 | _nolegend_ | 126196269190560 | lines[27]  |
|  2.22045e-16 | 15.95        |  0.4         | 15.95        | lines   | #6f6f6f |             |             |           1 | _nolegend_ | 126196269191232 | lines[28]  |
|  0.166339    | 33.707       |  0.233661    | 41.783       | lines   | #000000 |             |             |           1 | _nolegend_ | 126196269191808 | lines[29]  |
|  1.2         | 12.46        |  1.2         | 15.1         | lines   | #6f6f6f |             |             |           1 | _nolegend_ | 126196269192864 | lines[30]  |
|  1.2         | 22.555       |  1.2         | 22.75        | lines   | #6f6f6f |             |             |           1 | _nolegend_ | 126196269193344 | lines[31]  |
|  1.1         | 12.46        |  1.3         | 12.46        | lines   | #6f6f6f |             |             |           1 | _nolegend_ | 126196269194064 | lines[32]  |
|  1.1         | 22.75        |  1.3         | 22.75        | lines   | #6f6f6f |             |             |           1 | _nolegend_ | 126196269194736 | lines[33]  |
|  1           | 19.235       |  1.4         | 19.235       | lines   | #6f6f6f |             |             |           1 | _nolegend_ | 126196269195312 | lines[34]  |
| -1.17882     | -7.41204     | -1.1115      | -6.22596     | lines   | #000000 |             |             |           1 | _nolegend_ | 126196269196032 | lines[35]  |
|  2.2         |  7.25        |  2.2         | 14.73        | lines   | #6f6f6f |             |             |           1 | _nolegend_ | 126196269197088 | lines[36]  |
|  2.2         | 20.65        |  2.2         | 29.03        | lines   | #6f6f6f |             |             |           1 | _nolegend_ | 126196269197760 | lines[37]  |
|  2.1         |  7.25        |  2.3         |  7.25        | lines   | #6f6f6f |             |             |           1 | _nolegend_ | 126196269198528 | lines[38]  |
|  2.1         | 29.03        |  2.3         | 29.03        | lines   | #6f6f6f |             |             |           1 | _nolegend_ | 126196269199248 | lines[39]  |
|  2           | 17.82        |  2.4         | 17.82        | lines   | #6f6f6f |             |             |           1 | _nolegend_ | 126196269199920 | lines[40]  |
|  2.16634     | 30.677       |  2.23366     | 48.923       | lines   | #000000 |             |             |           1 | _nolegend_ | 126196269200544 | lines[41]  |
|  3.2         |  8.77        |  3.2         | 14.78        | lines   | #6f6f6f |             |             |           1 | _nolegend_ | 126196269201648 | lines[42]  |
|  3.2         | 25           |  3.2         | 38.07        | lines   | #6f6f6f |             |             |           1 | _nolegend_ | 126196269202368 | lines[43]  |
|  3.1         |  8.77        |  3.3         |  8.77        | lines   | #6f6f6f |             |             |           1 | _nolegend_ | 126196269203088 | lines[44]  |
|  3.1         | 38.07        |  3.3         | 38.07        | lines   | #6f6f6f |             |             |           1 | _nolegend_ | 126196269400528 | lines[45]  |
|  3           | 18.43        |  3.4         | 18.43        | lines   | #6f6f6f |             |             |           1 | _nolegend_ | 126196269401152 | lines[46]  |
|  3.16634     | 47.577       |  3.23366     | 48.763       | lines   | #000000 |             |             |           1 | _nolegend_ | 126196269401776 | lines[47]  |
| -0.4         | 13.51        |  2.22045e-16 | 19.81        | patches |         | #d3c4f6     | #6f6f6f     |           1 |            | 126196268825200 | patches[0] |
|  0.6         | 11.69        |  1           | 18.665       | patches |         | #d3c4f6     | #6f6f6f     |           1 |            | 126196270484416 | patches[1] |
|  1.6         | 13.405       |  2           | 26.7925      | patches |         | #d3c4f6     | #6f6f6f     |           1 |            | 126196269014464 | patches[2] |
|  2.6         | 17.165       |  3           | 32.375       | patches |         | #d3c4f6     | #6f6f6f     |           1 |            | 126196269018640 | patches[3] |
|  2.22045e-16 | 11.69        |  0.4         | 20.27        | patches |         | #98daa7     | #6f6f6f     |           1 |            | 126196268822656 | patches[4] |
|  1           | 15.1         |  1.4         | 22.555       | patches |         | #98daa7     | #6f6f6f     |           1 |            | 126196268576560 | patches[5] |
|  2           | 14.73        |  2.4         | 20.65        | patches |         | #98daa7     | #6f6f6f     |           1 |            | 126196269196320 | patches[6] |
|  3           | 14.78        |  3.4         | 25           | patches |         | #98daa7     | #6f6f6f     |           1 |            | 126196269200496 | patches[7] |
|  2.22045e-16 |  8.88178e-16 |  2.22045e-16 |  8.88178e-16 | patches |         | #d3c4f6     | #6f6f6f     |           1 | Yes        | 126196270236016 | patches[8] |
|  2.22045e-16 |  8.88178e-16 |  2.22045e-16 |  8.88178e-16 | patches |         | #98daa7     | #6f6f6f     |           1 | No         | 126196270485664 | patches[9] |

## X-axis tick labeles and their location

|   x | value   |
|----:|:--------|
|   0 | Thur    |
|   1 | Fri     |
|   2 | Sat     |
|   3 | Sun     |


## y-axis tick labeles and their location

|   x |   value |
|----:|--------:|
|  10 |      10 |
|  20 |      20 |
|  30 |      30 |
|  40 |      40 |
|  50 |      50 |

## legend

| label   | kind        | color   | facecolor   | edgecolor   |   linewidth |
|:--------|:------------|:--------|:------------|:------------|------------:|
| Yes     | collections |         | #d3c4f6     | #6f6f6f     |           1 |
| No      | collections |         | #98daa7     | #6f6f6f     |           1 |

"""

instruction = """A user want to query the artists of specific properties. You
will answer the list of artist id defined in the 'Properties of Artists' table.

Here are some notes you need to be aware,

- All x & y coordinates are in data coordinates.
- Properties of Artists table include bounding-box of each artist (xmin, xmax, ymin
  and ymax).
- For categorical plots, x- or y-labels often represents the category. However, a category may span a range of values in the numerical coordinate not a specific value. For example, given apple at 1, orange at 2 and banana at 3, apple means 0.5 to 1.5, orange from 1.5 to 2.5 and banana from 2.5 to 3.5.
"""

example1 = """
rectangles that belong to smoker

Received response:
1. 126196268825200
2. 126196270484416
3. 126196269014464
4. 126196269018640
5. 126196270236016

"""

async def _query(full_query):

    try:

        response = await get_response_from_gemini(full_query)
        print("\nReceived response:")
        for i, item in enumerate(response.items):
            print(f"{i + 1}. {item}")

        return response
    except Exception as e:
        print(f"\nAn error occurred: {e}")


def query(plot_properties, q):

    full_query = get_full_query(role, instruction, plot_properties, q)

    # Run the asynchronous main function
    response = asyncio.run(_query(full_query))

    return response

# def quer
# full_query = mpl_llm_query.get_full_query(mpl_llm_query.role,
#                                           mpl_llm_query.instruction,
#                                           ax_prop_context, q)

# response = query(plot_properties_context, q)



# Example usage of the function
if __name__ == "__main__":
    # context = plot_properties
    # # query = "rectangles that belong to smoker"
    q = "artists for Friday"
    # full_query = get_full_query(role, instruction, context, q)

    response = query(plot_properties_example, q)
    print(response)
    # import asyncio

    # async def main():
    #     """Main function to run the example."""
    #     # Provide the context and the question separately
    #     full_query = get_full_query(role, instruction, context, query)

    #     try:

    #         response = await get_response_from_gemini(full_query)
    #         print("\nReceived response:")
    #         for i, item in enumerate(response.items):
    #             print(f"{i + 1}. {item}")

    #         return response
    #     except Exception as e:
    #         print(f"\nAn error occurred: {e}")

    # # Run the asynchronous main function
    # response = asyncio.run(main())
