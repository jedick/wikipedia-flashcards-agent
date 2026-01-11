# Wikipedia Flashcard Generator Project

We're building a Wikipedia flashcard generator. It's a command line tool that takes a topic, searches Wikipedia, and creates educational flashcards from the articles it finds.

## Architecture

The architecture is pretty straightforward. There are three agents working in sequence, each doing one specialized task. The output of one agent becomes the input of the next one.

From the user's perspective, you run a single command with your topic. The system logs everything very verbosely so that we can see the progress and understand what it does in each step. And at the end you get the markdown file with your flashcards ready for download.

## Tech Stack

The tech stack we'll be using is:
- Pydantic AI for the agent orchestration
- OpenAI GPT-4o model
- Wikipedia Python library for searching and fetching articles
- python-dotenv for loading the API key from .env
- Python 3.12 or higher

## The Three Agents

### Agent 1: Wikipedia Search

This agent searches Wikipedia for relevant articles and fetches their full content.

What happens is the agent receives the user's query and calls its Wikipedia search tool. The tool finds two to three relevant articles and retrieves their full text. The agent logs the retrieval and all the functionality for searching and fetching articles lives in the tool itself.

The agent returns data with structured outputs with specific models:
- A model for a Wikipedia article that has a title and content
- Wikipedia search result which has an articles field with a list of Wikipedia articles

The tool, which is a plain Pydantic AI tool, searches Wikipedia with the query getting up to 10 results and it picks from these results two or three most relevant articles and for each one it fetches the complete page from Wikipedia and then returns them as the Wikipedia search results.

### Agent 2: Analysis and Summary

The second agent is analysis and summary. The agent analyzes these multiple Wikipedia articles and synthesizes them into a coherent summary.

The way it works is it receives a combined text of all the articles that the first agent retrieved and it reads them and processes them and produces a summary that has all the relevant facts and concepts and relationships and all the information that is worth learning from these articles. And it should produce something like between 500 and 1000 words, not more than that.

The summary agent should produce a string. So it doesn't use structured outputs. It should just return a string with a complete summary. And of course like the other agents it should be verbose in logging explaining what it does so that we can follow its progress very well.

### Agent 3: Flashcard Generator

The third agent is the flashcard generator agent. This agent can read the summary text that was produced by the second agent and it processes this information and creates flashcards from it.

The flashcards are returned as objects as structured outputs with Pydantic models where there's a:
- Flashcard model with a question field and an answer field
- Flashcards results with the flashcards field which is a list of flashcard objects

It should produce between 20 to 50 flashcards.

## Final Output

Finally when we have the results from the flashcards agent, we should prepare a markdown file from them with just one question and answer pair then a separator and then the next one and save this file to disk and again report about everything so that the users can see how the agent operates and where it saved the file.

## Program Flow

The way the program works is the script is run. It would be possible to run it with `uv run` and then the script followed by the query as the trailing parameters and the script just sort of collects all the parameters and constructs from them the query the user is asking even if it's multiple words.

And with that, it kicks off the first agent, passing to it the user's query. And throughout, as everything works, we report about every step, what succeeds, what fails, what the different agents are doing.

Once the first agent is done, it takes the results, concatenates them, passes them to the second, the summary agent. And with the summary produced by this agent, it passes things on to the flashcard generator agent.

## Implementation Plan - Three Steps

The way we're going to work on this project is in three distinct steps. And so it's very important you create that you plan for working in three steps.

### Step 1: Setup and Wikipedia Search Agent

The first step will be setting things up, creating the script file and making sure that you have access to all the relevant documentation, doing whatever research you need. And then in the first step we'll just be working on the first agent, the Wikipedia search agent. We'll be implementing this, testing that it works correctly and then we stop.

### Step 2: Summary and Analysis Agent

Then in the second step we'll be implementing the summary and analysis agent. Once again testing beginning to end that the script works and completes all the way to getting us a workable summary. And again then we stop.

### Step 3: Flashcard Generator Agent

And finally in the third step we'll be implementing the flashcard generator agent. And at this point we'll be completing the implementation of this project, testing it end to end and then we're done.

## Your Task

Your task now is to do all the research you need so that you understand all the different libraries we're going to use like Pydantic AI and the Python Wikipedia library and how to write a script for running with uv run and so on and so forth and write a detailed plan for implementing all of this in three steps and then save this plan in tmp/plan.md.
