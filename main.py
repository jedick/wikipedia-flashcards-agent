"""Main entry point for the Wikipedia Flashcard Generator."""
# Load environment variables FIRST, before any imports that might need them
from dotenv import load_dotenv
load_dotenv()

import asyncio
import logging
import re
import sys
from pathlib import Path

from agents.wikipedia_search import search_wikipedia
from agents.summary import generate_summary
from agents.flashcard_generator import generate_flashcards
from models.flashcards import FlashcardsResult

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s',
    datefmt='%Y-%m-%d %H:%M:%S'
)

logger = logging.getLogger(__name__)


def sanitize_filename(topic: str) -> str:
    """
    Sanitize topic string to create a valid filename.
    
    Args:
        topic: The topic string
        
    Returns:
        Sanitized filename string
    """
    # Replace spaces and special characters with underscores
    sanitized = re.sub(r'[^\w\s-]', '', topic)
    sanitized = re.sub(r'[-\s]+', '_', sanitized)
    # Remove leading/trailing underscores
    sanitized = sanitized.strip('_')
    # Convert to lowercase
    sanitized = sanitized.lower()
    return sanitized


def save_flashcards_to_markdown(flashcards_result: FlashcardsResult, topic: str) -> Path:
    """
    Save flashcards to a markdown file.
    
    Args:
        flashcards_result: The flashcards result object
        topic: The topic string for filename generation
        
    Returns:
        Path to the created markdown file
    """
    # Generate filename from topic
    filename = f"flashcards_{sanitize_filename(topic)}.md"
    filepath = Path(filename)
    
    logger.info(f"Writing flashcards to markdown file: {filepath}")
    
    # Format flashcards as markdown
    with open(filepath, 'w', encoding='utf-8') as f:
        for flashcard in flashcards_result.flashcards:
            f.write(f"**Question:** {flashcard.question}\n\n")
            f.write(f"**Answer:** {flashcard.answer}\n\n")
            f.write("---\n\n")
    
    logger.info(f"Successfully saved {len(flashcards_result.flashcards)} flashcards to {filepath.absolute()}")
    
    return filepath


async def main_async():
    """Main async function that orchestrates the agents."""
    # Get the topic from command line arguments
    # All trailing arguments are combined into the topic query
    if len(sys.argv) < 2:
        logger.error("Usage: python main.py <topic>")
        logger.error("Example: python main.py quantum physics")
        sys.exit(1)
    
    # Combine all arguments after the script name into the topic
    topic = " ".join(sys.argv[1:])
    logger.info(f"Starting Wikipedia flashcard generation for topic: {topic}")
    
    try:
        # Step 1: Wikipedia Search Agent
        logger.info("=" * 60)
        logger.info("STEP 1: Wikipedia Search Agent")
        logger.info("=" * 60)
        
        search_result = await search_wikipedia(topic)
        
        logger.info("Wikipedia Search Agent completed successfully")
        logger.info(f"Retrieved {len(search_result.articles)} articles:")
        for article in search_result.articles:
            logger.info(f"  - {article.title}")
        
        # Concatenate article contents
        logger.info("Concatenating article contents...")
        combined_text = "\n\n".join([
            f"=== {article.title} ===\n{article.content}"
            for article in search_result.articles
        ])
        logger.info(f"Combined text length: {len(combined_text)} characters")
        
        # Step 2: Summary Agent
        logger.info("")
        logger.info("=" * 60)
        logger.info("STEP 2: Summary and Analysis Agent")
        logger.info("=" * 60)
        
        summary = await generate_summary(combined_text)
        
        logger.info("Summary Agent completed successfully")
        logger.info(f"Summary length: {len(summary)} characters")
        logger.info(f"Summary preview: {summary[:200]}...")
        
        # Step 3: Flashcard Generator Agent
        logger.info("")
        logger.info("=" * 60)
        logger.info("STEP 3: Flashcard Generator Agent")
        logger.info("=" * 60)
        
        flashcards_result = await generate_flashcards(summary)
        
        logger.info("Flashcard Generator Agent completed successfully")
        logger.info(f"Generated {len(flashcards_result.flashcards)} flashcards")
        
        # Save flashcards to markdown file
        logger.info("")
        logger.info("=" * 60)
        logger.info("Saving Flashcards to Markdown File")
        logger.info("=" * 60)
        
        filepath = save_flashcards_to_markdown(flashcards_result, topic)
        
        logger.info("")
        logger.info("=" * 60)
        logger.info("COMPLETE: Wikipedia Flashcard Generation")
        logger.info("=" * 60)
        logger.info(f"Topic: {topic}")
        logger.info(f"Articles retrieved: {len(search_result.articles)}")
        logger.info(f"Summary length: {len(summary)} characters")
        logger.info(f"Flashcards generated: {len(flashcards_result.flashcards)}")
        logger.info(f"Output file: {filepath.absolute()}")
        logger.info("=" * 60)
        
    except Exception as e:
        logger.error(f"Error during execution: {e}", exc_info=True)
        sys.exit(1)


def main():
    """Main entry point."""
    try:
        asyncio.run(main_async())
    except KeyboardInterrupt:
        logger.info("Interrupted by user")
        sys.exit(1)
    except Exception as e:
        logger.error(f"Fatal error: {e}", exc_info=True)
        sys.exit(1)


if __name__ == "__main__":
    main()
