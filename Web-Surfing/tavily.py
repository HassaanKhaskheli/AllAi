from dotenv import load_dotenv
import os
from tavily import TavilyClient, MissingAPIKeyError

### read up on submit_tool open ai

load_dotenv()

#get key
try:
    api_key = os.getenv("TAVILY_API_KEY")
except MissingAPIKeyError:
     print("API key is missing. Please provide a valid API key.")   

#client initialization
tavily_client = TavilyClient(api_key=api_key)

# response = tavily_client.search("Who is Leo Messi?") 
# # This is a simple search query, it returns relevance score of each webpage's results but doesn't compile them into one answer field, 
# # formatting compexity : mid

""" search(query, **kwargs)

##Performs a Tavily Search query and returns the response as a well-structured dict.
## Additional parameters can be provided as keyword arguments (detailed below). The keyword arguments supported by this method are:
 
search_depth 
    str = "basic" or "advanced", default is basic
    basic is quicker, searches web for well-known information, better for quick info that is available easily
    advanced is slower, searches web for less well-known information, better if you need to dig deeper into the web
topic
    category of the search
    str = "general" or "news", default is general
    general is more broad in context, searches everything
    news is more specific, searches only recent events and news from reputable sources
days
    int = days from the current date to search back from, default is 3
    only usable if topic is set to news
max_results
    int = max number of search results to return, default is 5
include_domains
    url = domains to definitely include in the search, default is none
exclude_domains
    url = domains to exclude from the search, default is none
include_answer
    bool
    includes a short answer along with the main answer it scrapes from the web sources 
include_raw_content
    bool = includes the cleaned and parsed HTML content of each search result. Default is False.
include_images
    bool = includes a list of images, from the web, that help in answering/explaining the query in the response. Default is False.
include_image_descriptions
    bool = includes a list of query-related images and their descriptions in the response. Default is False.
##Returns a dict with all related response fields. If you decide to use the asynchronous client, returns a coroutine resolving to that dict. The details of the exact response format are given in the Search Responses section.

"""

# response = tavily_client.get_search_context(query="What happened during the Burning Man floods?")
# # This is a search query with contextual compilation and answers, doesn't provide relevance scores but does give one compiled answer 
# # formatting complexity : high

""" get_search_context(query, **kwargs)

##Performs a Tavily Search query and returns a str of content and sources within the provided token limit. It's useful for getting only related content from retrieved websites without having to deal with context extraction and token management.
##Returns a str containing the content and sources of the results. If you decide to use the asynchronous client, returns a coroutine resolving to that str.
## Additional parameters can be provided as keyword arguments (detailed below). The keyword arguments supported by this method are:

search_depth 
    str = "basic" or "advanced", default is basic
    basic is quicker, searches web for well-known information, better for quick info that is available easily
    advanced is slower, searches web for less well-known information, better if you need to dig deeper into the web
topic
    category of the search
    str = "general" or "news", default is general
    general is more broad in context, searches everything
    news is more specific, searches only recent events and news from reputable sources
days
    int = days from the current date to search back from, default is 3
    only usable if topic is set to news
max_results
    int = max number of search results to return, default is 5
include_domains
    url = domains to definitely include in the search, default is none
exclude_domains
    url = domains to exclude from the search, default is none
"""

response= tavily_client.qna_search(query="Who is Leo Messi?") 
# This is a search query that returns one short answer with maximum summarization 
# #formatting complexity : low

""" qna_search(query, **kwargs)

##Performs a search and returns a str containing an answer to the original query. This is optimal to be used as a tool for AI agents.
##Returns a str containing a short answer to the search query. If you decide to use the asynchronous client, returns a coroutine resolving to that str.
##Additional parameters can be provided as keyword arguments (detailed below). The keyword arguments supported by this method are:

search_depth 
    str = "basic" or "advanced", default is advanced
    basic is quicker, searches web for well-known information, better for quick info that is available easily
    advanced is slower, searches web for less well-known information, better if you need to dig deeper into the web
topic
    category of the search
    str = "general" or "news", default is general
    general is more broad in context, searches everything
    news is more specific, searches only recent events and news from reputable sources
days
    int = days from the current date to search back from, default is 3
    only usable if topic is set to news
max_results
    int = max number of search results to return, default is 5
include_domains
    url = domains to definitely include in the search, default is none
exclude_domains
    url = domains to exclude from the search, default is none
"""

print(response)

"""response = {
  "query": "The query provided in the request",
  "answer": "A short answer to the query",  # This will be None if include_answer is set to False in the request
  "follow_up_questions": None,  # This feature is still in development
  "images": [ 
    {
      "url": "Image 1 URL",
      "description": "Image 1 Description",  
    },
    {
      "url": "Image 2 URL",
      "description": "Image 2 Description",
    },
    {
      "url": "Image 3 URL",
      "description": "Image 3 Description",
    },
    {
      "url": "Image 4 URL",
      "description": "Image 4 Description",
    },
    {
      "url": "Image 5 URL",
      "description": "Image 5 Description",
    }
  ],  # This will be a list of string URLs if `include_images` is True and `include_image_descriptions` is False, or an empty list if both set to False.
  "results": [
    {
      "title": "Source 1 Title",
      "url": "Source 1 URL",
      "content": "Source 1 Content",
      "score": 0.99  # This is the "relevancy" score of the source. It ranges from 0 to 1.
    },
    {
      "title": "Source 2 Title",
      "url": "Source 2 URL",
      "content": "Source 2 Content",
      "score": 0.97
    }
  ],  # This list will have max_results elements
  "response_time": 1.09 # This will be your search response time
}
"""