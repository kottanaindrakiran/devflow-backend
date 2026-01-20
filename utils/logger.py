import logging
import sys
import logfire
from pydantic_ai import Agent

def setup_logger(name: str = "devflow_ai"):
    """
    Sets up a structured logger.
    """
    # Configure logfire
    try:
        logfire.configure(send_to_logfire='if-token-present')
    except Exception as e:
        print(f"Logfire configuration skipped: {e}")
    
    logger = logging.getLogger(name)
    logger.setLevel(logging.INFO)
    
    # Check if handlers already exist to avoid duplicate logs
    if not logger.handlers:
        handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(
            '%(asctime)s - %(name)s - %(levelname)s - %(message)s'
        )
        handler.setFormatter(formatter)
        logger.addHandler(handler)
        
    return logger

logger = setup_logger()
