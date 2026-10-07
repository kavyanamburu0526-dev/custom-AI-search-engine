import os
from dotenv import load_dotenv
from tavily import TavilyClient
from google import genai
# Load API keys
load_dotenv()
# TAVILY SETUP
tavily = TavilyClient(
    api_key=os.getenv("TAVILY_API_KEY")
)
# GEMINI SETUP
gemini = genai.Client()
# SEARCH ENGINE
print("       🔎 CUSTOM AI SEARCH ENGINE")
query = input("\nWhat do you want to search? ")
print("\n🌐 Searching the web...")
# Search Tavily
response = tavily.search(
    query=query,
    max_results=5
)
# Collect search results
search_context = ""
for result in response["results"]:
    search_context += f"""
Title: {result["title"]}
URL: {result["url"]}
Content: {result["content"]}
"""
# ASK GEMINI
print("🤖 Gemini is analyzing the results...")
prompt = f"""
You are an AI search assistant.
Answer the user's question using the web search results provided below.
User question:
{query}
Web search results:
{search_context}
Instructions:
- Give a clear and useful answer.
- Use the information from the search results.
- Do not invent facts.
- If the search results are insufficient, say so.
- Keep the answer easy to understand.
"""
answer = gemini.models.generate_content(
    model="gemini-3.5-flash-lite",
    contents=prompt
)
# DISPLAY ANSWER
print("\n====================================")
print("🤖 AI ANSWER")
print(answer.text)
# DISPLAY SOURCES
print("\n====================================")
print("📚 SOURCES")
for result in response["results"]:
    print("\n-", result["title"])
    print(" ", result["url"])