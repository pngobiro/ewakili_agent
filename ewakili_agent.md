- NEO4J_URI=bolt://host.docker.internal:7687 # <-- Ensure this is correct here too
- NEO4J_USER=neo4j
- NEO4J_PASSWORD=f7DEfxd9wy5.

video: https://youtu.be/0p3S56JnTCg




Building AI Agents with Google’s Gen AI Toolbox and Neo4j Knowledge Graphs
Kurtis Van Gent
Kurtis Van Gent
7 min read
·
Mar 5, 2025

This blog was co-written by:
-
Michael Hunger
, Head of Product Innovation, Neo4j
-
Kurtis Van Gent
, Staff Software Engineer, Google

Prefer videos over text? Check out our previously recorded Webinar: Building AI Agents with Google’s Gen AI Toolbox.

Last month, Google announced the public beta launch of Gen AI Toolbox for Databases. Today, we are excited to announce Toolbox’s support for Neo4j, a graph database management system. Neo4j has been a key partner in the support and development of Toolbox. Their addition enables developers and organizations using Neo4j to create agentic tools that access their data using the popular GraphRAG techniques, expanding the Toolbox’s usefulness for Gen AI applications.
Neo4j — Graph Database Management System

Neo4j is the leading open source graph database — it manages information not as tables but as entities (nodes) and relationships between them allowing a flexible and powerful representation of connected information. Graphs add unique capabilities for many domains like biomedical, supply chain, manufacturing, fraud detection, and transport logistics. Knowledge Graphs which you can think of as digital twins of your organization (people, processes, products, partners etc.) are a great “factual memory” companion to LLMs’ language skills. The use of GraphRAG improves the accuracy, reliability and explainability of GenAI applications.
Gen AI Toolbox

When it comes to creating tools that access databases, developers quickly hit a number of challenges when building AI agents in production: authentication, authorization, sanitization, connection pooling, and more. These challenges can become a burden, slowing down development and leaving room for mistakes when implementing the same boilerplate code over and over again.

Enter Gen AI Toolbox — the open source server that can help you develop tools easier, faster, and more securely. Toolbox sits between your application and your database — handling the complexities such as connection pooling, authentication, and more. Toolbox enables you define the tools in a centralized location, and integrate with your agents in less than 3 lines of code:

from toolbox_langchain import ToolboxClient

# update the url to point to your server
client = ToolboxClient("http://127.0.0.1:5000")

# these tools can be passed to your agent! 
tools = await client.aload_toolset()

Toolbox is truly open-source: as part of the launch, Google Cloud partnered with other database vendors (such as Neo4j) to build support for a large number of open source and proprietary databases:

    PostgresSQL (including AlloyDB and Cloud SQL for MySQL)
    MySQL (including Cloud SQL for MySQL)
    SQL Server (including Cloud SQL for SQL Server)
    Spanner
    Neo4j

Accessing Neo4j with Toolbox

After you’ve installed the Toolbox server, you are ready to configure your tools.yaml. To create a tool that queries Neo4j, there are 2 things you’ll need to configure:

A Neo4j source, which defines how to connect and authenticate to your Neo4j instance. Here’s the Neo4j source for our example:

sources:
    companies-graph:
        kind: "neo4j"
        uri: "neo4j+s://demo.neo4jlabs.com"
        user: "companies"
        password: "companies"
        database: "companies"

Once you’ve defined the source, it’s time to define the tool. A neo4j-cypher tool defines the cypher query that should be run when the tool is invoked by your agent. Tools can do anything you can express in a cypher statement — including reading or writing! To be usable with an agentic setup it is really important to describe the tool, parameters and results in enough detail so that the LLM can reason about its applicability.

This is a part of the tool config for our example, including source, statement, description and parameters:

tools:
  articles_in_month:
    kind: neo4j-cypher
    source: companies-graph
    statement: |
      MATCH (a:Article)
      WHERE date($date) <= date(a.date) < date($date) + duration('P1M')
      RETURN a.id as article_id, a.author as author, a.title as title, toString(a.date) as date, a.sentiment as sentiment
      LIMIT 25
    description: List of Articles (article_id, author, title, date, sentiment) in a month timeframe from the given date
    parameters:
      - name: date
        type: string
        description: Start date in yyyy-mm-dd format
  companies_in_articles:
    kind: neo4j-cypher
    source: companies-graph
    statement: |
      MATCH (a:Article)-[:MENTIONS]->(c)
      WHERE a.id = $article_id AND not exists { (c)<-[:HAS_SUBSIDARY]-() }
      RETURN c.id as company_id, c.name as name, c.summary as summary
    description: Companies (company_id, name, summary) mentioned in articles by article id
    parameters:
      - name: article_id
        type: string
        description: Article id to find companies mentioned in

Investment Research Agent

This is a demonstration of an agentic LangChain application with tools that use GraphRAG patterns combining fulltext and graph search.

The example represents an investment research agent that can be used to find recent news about companies, their investors, competitors, partners and industries. It is powered by data from the diffbot knowledge graph that was imported into Neo4j. It captures the complexity of the domain through relationships between a basic set of entities.

The code for the example can be found in this repository:
neo4j-gcp-vertex-ai-langchain/toolbox-companies at main ·…
Neo4j Extensions and Integrations with Vertex AI and LangChain - neo4j-gcp-vertex-ai-langchain/toolbox-companies at…

github.com
Exploring a Public Graph Dataset

The dataset is a graph about companies, associated industries, people that work at or invested in the companies, and articles that report on those companies.

The news articles are chunked and the chunks are also stored in the graph.

The database is publicly available with a readonly user, you can explore the data at the following URL: https://demo.neo4jlabs.com:7473/browser/

    URI: neo4j+s://demo.neo4jlabs.com
    User: companies
    Password: companies
    Companies: companies

In our configuration we provide tools that make use of the fulltext index as well as a graph retrieval queries that fetch the following additional information:

    Parent Article of the Chunk (aggregate all chunks for a single article)
    Organization(s) mentioned
    Industry Category(ies) for the organization
    Person(s) connected to the organization and their roles (e.g. investor, chairman, CEO)

We utilize the agentic LangChain integration with Vertex AI that allows us to pass the tools we registered with Toolbox automatically to the LLM for tool calling. We will utilize both hybrid search as well as GraphRAG retrievers.
Connecting our Agent to Toolbox

We now can use LangChain with the Vertex AI Gemini 2.0 Flash model and feed our tool definitions to the model and do a quick test. We can follow the quickstart example in the toolbox documentation.

import asyncio
import os

from langgraph.prebuilt import create_react_agent
from langchain_google_vertexai import ChatVertexAI
from langgraph.checkpoint.memory import MemorySaver
from toolbox_langchain import ToolboxClient
prompt = """
  You're a helpful investment research assistant. 
  You can use the provided tools to search for companies, 
  people at companies, industries, and news articles from 2023.
  Don't ask for confirmations from the user.
  User: 
"""
queries = [
    "What industries deal with computer manufacturing?",
    "List 5 companies in the computer manufacturing industry with their description.",
]
def main():
    model = ChatVertexAI(model_name="gemini-1.5-pro")
    client = ToolboxClient("http://127.0.0.1:5000")
    tools = client.load_toolset()
    agent = create_react_agent(model, tools, checkpointer=MemorySaver())
    config = {"configurable": {"thread_id": "thread-1"}}
    for query in queries:
        inputs = {"messages": [("user", prompt + query)]}
        response = agent.invoke(inputs, stream_mode="values", config=config)
        print(response["messages"][-1].content)
main()



The industries that deal with computer manufacturing are: Computer Hardware Companies, Electronic Products Manufacturers, and Computer Storage Companies.

Here are 5 companies in the computer hardware industry along with their descriptions:1.  **Microsoft Egypt:** Microsoft branch in Egypt
2.  **Apigee:** Software company based in San Jose, California, United States and owned by Google
3.  **Microsemi:** Communications corporation
4.  **Intermec:** American electronics manufacturing company
5.  **Elitegroup Computer Systems:** No summary available

Example Conversation

Providing the agents with tools to inspect different aspects of the data, allows it to answer even complex and follow up questions, as we show in the example below.
Which companies are mentioned in the news in January 2023 with positive sentiment?

This question requires the call of multiple tools and proper parameter conversion. We give a partial date January 2023, that has to be converted to the format yyyy-mm-dd for the tool call. The agent has to understand that “good sentiment” refers to the numeric score and that it needs to post-filter the article results. Which then have to be fed individually into the companies_in_article tool to retrieve the companies.

    Here are the articles from January 2023 with positive sentiment scores, and the companies they mention:

    Mozilla’s Pocket App Just Got a Big Update (0.838, 0.83): Mozilla

    Onapsis Announces Collaboration with Wipro to Remove Security as a Digital Transformation Roadblock (0.804, 0.735): Onapsis, Wipro, SAP

    ….

Who is working there as board members?

Here we refer back to the companies from the previous answer with “there” and also specify the roles requirement for the API call choice only vaguely. The Agent needs to call the people_at_company endpoint multiple times, with the ids of the companies retrieved earlier in the agent memory and then aggregate and filter the information into the response.

    I was not able to retrieve board members for all of the companies. Here’s the information I found:

    Wipro:
    - Azim Premji (BOARD_MEMBER)
    - Rishad Premji (BOARD_MEMBER)

    SAP:
    - Hasso Plattner (BOARD_MEMBER)
    - Jennifer Morgan (BOARD_MEMBER)
    …

Next Steps

In this article we demonstrated how you can build agentic applications that integrate database based tools easily with Google’s Gen AI Toolbox. While we focused on a GraphRAG use-case with a knowledge graph in Neo4j, you can combine different data-sources and types of databases in the same agentic application.

If you are interested in exploring more with Toolbox and Neo4j, we recommend you check out the following resources:

    Quickstart for running Toolbox locally
    Get Started with GraphRAG with Neo4j
    Deploying Toolbox to Cloud Run

As Toolbox integrates with different agent frameworks you can define your tools once and reuse them for several use-cases. Neo4j found it easy to contribute to Toolbox and we hope you will make use of the feedback and discussion mechanisms to add your own data sources and provide feedback and improvements.