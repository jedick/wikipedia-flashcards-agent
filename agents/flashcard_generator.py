"""Flashcard Generator Agent - creates flashcards from summary text."""

import logging
from pydantic_ai import Agent

from models.flashcards import Flashcard, FlashcardsResult

# Set up logging
logger = logging.getLogger(__name__)


# Create the flashcard generator agent with structured output
flashcard_generator_agent = Agent(
    'openai:gpt-4o',
    output_type=FlashcardsResult,
    system_prompt="""You are a flashcard generator agent. Your task is to:
1. Analyze the provided summary text
2. Extract key facts, concepts, and information
3. Create educational flashcards with question-answer pairs
4. Generate between 20 and 50 flashcards

Each flashcard should:
- Have a clear, concise question
- Have a comprehensive answer that covers the key information
- Focus on important concepts, facts, definitions, and relationships
- Be suitable for learning and studying

Generate flashcards that cover a diverse range of topics from the summary.
Ensure the questions are well-formed and the answers are informative.""",
)


async def generate_flashcards(summary: str) -> FlashcardsResult:
    """
    Generate flashcards from summary text.
    
    Args:
        summary: The summary text to generate flashcards from
        
    Returns:
        FlashcardsResult with list of flashcards
    """
    logger.info("Starting flashcard generation")
    logger.info(f"Summary length: {len(summary)} characters")
    
    # Run the agent
    result = await flashcard_generator_agent.run(
        f"""Please analyze the following summary and create educational flashcards.
Generate between 20 and 50 flashcards with question-answer pairs.

Summary:
{summary}

Please create flashcards that cover the key concepts, facts, and information from this summary.
Each flashcard should have a clear question and a comprehensive answer."""
    )
    
    flashcards_result = result.output
    
    logger.info("Flashcard generation completed")
    logger.info(f"Generated {len(flashcards_result.flashcards)} flashcards")
    
    if len(flashcards_result.flashcards) < 20:
        logger.warning(f"Generated {len(flashcards_result.flashcards)} flashcards, fewer than recommended (20)")
    elif len(flashcards_result.flashcards) > 50:
        logger.warning(f"Generated {len(flashcards_result.flashcards)} flashcards, more than recommended (50)")
    
    # Log first few flashcards as preview
    for i, flashcard in enumerate(flashcards_result.flashcards[:3], 1):
        logger.info(f"Flashcard {i} preview:")
        logger.info(f"  Q: {flashcard.question[:100]}...")
        logger.info(f"  A: {flashcard.answer[:100]}...")
    
    return flashcards_result
