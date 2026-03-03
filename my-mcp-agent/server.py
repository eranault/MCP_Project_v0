#lets write our mcp server.
#the goal is to have our llm use two tools, read bullet and modify bullet. 
#by doing that we can have the llm read the bullet point, and then modify it based on the content of the bullet point and the context .


import os
import re
import sys
import time

from dotenv import load_dotenv
from groq import Groq, AuthenticationError, RateLimitError, APIConnectionError
from fastmcp import FastMCP
from fastmcp.exceptions import ToolError
from loguru import logger


load_dotenv()
GROQ_API_KEY = os.getenv("GROQ_API_KEY")

GROQ_MODEL = "llama-3.3-70b-versatile"
SERVER_NAME  = "cv-optimizer"
MAX_CV_CHARS = 20_000  

if not GROQ_API_KEY:
    logger.error("Groq API key not found. Please set GROQ_API_Key in your .env file.")
    sys.exit(1)
if not GROQ_API_KEY.startswith("gsk_"):
    logger.error("Invalid Groq API key format. Please ensure it starts with 'gsk_'.")
    sys.exit(1)

logger.info(f"Starting {SERVER_NAME} with model {GROQ_MODEL}")


mcp = FastMCP(
    name=SERVER_NAME,
    instructions="""
    CV Optimizer — AI-powered resume assistant.

    Available tools:
    1. analyze_cv    → Get a quality score and issues list for any CV
    2. rewrite_bullets → AI-rewrite weak bullet points using Llama 3.3 70B

    Recommended workflow:
    - Call analyze_cv first to understand the CV's current state
    - Then call rewrite_bullets on the weakest sections
    """
)


@mcp.tool()
def analyze_cv(cv_text: str) -> dict:
    """
    Analyze a CV and return a quality score (0-100) along with identified issues.
    Issues may include: lack of quantification, weak action verbs, formatting problems, etc.
    """
    if len(cv_text) > MAX_CV_CHARS:
        raise ToolError(f"CV text exceeds maximum length of {MAX_CV_CHARS} characters.")
    start= time.time()
    

    
    return {"score": score, "issues": issues}