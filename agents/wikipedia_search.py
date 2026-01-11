"""Wikipedia Search Agent - searches Wikipedia and retrieves relevant articles."""

import json
import logging
import wikipedia
from pydantic_ai import Agent
from pydantic_ai.tools import Tool

from models.wikipedia import WikipediaArticle, WikipediaSearchResult

# Set up logging
logger = logging.getLogger(__name__)

# Configure Wikipedia library
wikipedia.set_lang("en")
wikipedia.set_rate_limiting(True)


@Tool
def search_wikipedia_tool(query: str) -> str:
    """
    Search Wikipedia for articles and retrieve full content.
    
    This tool searches Wikipedia for up to 10 results, then fetches
    the full content of the 2-3 most relevant articles.
    
    Args:
        query: The search query string
        
    Returns:
        A formatted string with article titles and content
    """
    logger.info(f"Searching Wikipedia for query: {query}")
    
    try:
        # Search Wikipedia for up to 10 results
        search_results = wikipedia.search(query, results=10)
        logger.info(f"Found {len(search_results)} search results")
        
        # Select top 2-3 most relevant articles (take first 3 for now)
        selected_titles = search_results[:3]
        logger.info(f"Selected {len(selected_titles)} articles for retrieval: {selected_titles}")
        
        articles_data = []
        for title in selected_titles:
            try:
                logger.info(f"Fetching article: {title}")
                page = wikipedia.page(title, auto_suggest=False)
                articles_data.append({
                    "title": page.title,
                    "content": page.content
                })
                logger.info(f"Successfully retrieved article: {page.title} ({len(page.content)} characters)")
            except wikipedia.exceptions.DisambiguationError as e:
                # Handle disambiguation pages by using the first option
                first_option = e.options[0] if e.options else None
                logger.warning(f"Disambiguation error for {title}, trying first option: {first_option}")
                if first_option:
                    try:
                        page = wikipedia.page(first_option, auto_suggest=False)
                        articles_data.append({
                            "title": page.title,
                            "content": page.content
                        })
                        logger.info(f"Successfully retrieved disambiguation result: {page.title}")
                    except Exception as e2:
                        logger.error(f"Failed to retrieve disambiguation result: {e2}")
            except wikipedia.exceptions.PageError:
                logger.warning(f"Page not found: {title}")
            except Exception as e:
                logger.error(f"Error retrieving article {title}: {e}")
        
        logger.info(f"Successfully retrieved {len(articles_data)} articles")
        
        # Return the articles data as JSON string for the agent to process
        # The agent will parse this and format it into WikipediaSearchResult
        return json.dumps({
            "articles": articles_data
        })
        
    except Exception as e:
        logger.error(f"Error in Wikipedia search: {e}")
        return json.dumps({"articles": []})


# Create the agent with structured output
wikipedia_search_agent = Agent(
    'openai:gpt-4o',
    output_type=WikipediaSearchResult,
    system_prompt="""You are a Wikipedia search agent. Your task is to:
1. Use the search_wikipedia_tool to find relevant Wikipedia articles for the user's query
2. The tool will search Wikipedia and retrieve 2-3 most relevant articles with their full content
3. Parse the tool's output and return a structured WikipediaSearchResult containing the articles

The tool returns JSON with articles array. Each article has 'title' and 'content' fields.
You must return a WikipediaSearchResult object with an 'articles' field containing WikipediaArticle objects.

Be thorough and ensure you retrieve articles that are most relevant to the user's query.""",
    tools=[search_wikipedia_tool],
)


async def search_wikipedia(query: str) -> WikipediaSearchResult:
    """
    Search Wikipedia for articles related to the query.
    
    Args:
        query: The search query string
        
    Returns:
        WikipediaSearchResult with list of articles
    """
    logger.info(f"Starting Wikipedia search for query: {query}")
    
    # Run the agent
    result = await wikipedia_search_agent.run(
        f"Search Wikipedia for articles about: {query}. Use the search_wikipedia_tool to retrieve the articles."
    )
    
    logger.info(f"Wikipedia search completed. Retrieved {len(result.output.articles)} articles")
    for article in result.output.articles:
        logger.info(f"  - {article.title} ({len(article.content)} characters)")
    
    return result.output
