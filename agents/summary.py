"""Summary Agent - analyzes Wikipedia articles and creates a coherent summary."""

import logging
from pydantic_ai import Agent

# Set up logging
logger = logging.getLogger(__name__)


# Create the summary agent (no structured output - returns string)
summary_agent = Agent(
    'openai:gpt-4o',
    system_prompt="""You are a summary and analysis agent. Your task is to:
1. Analyze the provided Wikipedia article content
2. Synthesize the information into a coherent summary
3. Identify key facts, concepts, and relationships
4. Create a comprehensive summary that contains all relevant information worth learning

The summary should be between 500 and 1000 words. Do not exceed 1000 words.
Focus on:
- Key concepts and definitions
- Important facts and figures
- Relationships between concepts
- Historical context where relevant
- Notable examples or applications

Write in clear, educational language suitable for creating flashcards.""",
)


async def generate_summary(combined_text: str) -> str:
    """
    Generate a summary from concatenated Wikipedia article content.
    
    Args:
        combined_text: The concatenated text from all Wikipedia articles
        
    Returns:
        A summary string (500-1000 words)
    """
    logger.info("Starting summary generation")
    logger.info(f"Input text length: {len(combined_text)} characters")
    
    # Run the agent
    result = await summary_agent.run(
        f"""Please analyze the following Wikipedia article content and create a comprehensive summary.
The summary should be between 500 and 1000 words and should cover all key concepts, facts, and relationships.

Article content:
{combined_text}

Please provide a clear, educational summary that synthesizes this information."""
    )
    
    summary = result.data
    word_count = len(summary.split())
    
    logger.info(f"Summary generation completed")
    logger.info(f"Summary length: {word_count} words, {len(summary)} characters")
    
    if word_count < 500:
        logger.warning(f"Summary is shorter than recommended (500 words), only {word_count} words")
    elif word_count > 1000:
        logger.warning(f"Summary exceeds recommended length (1000 words), has {word_count} words")
    
    return summary
