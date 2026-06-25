"""
Configuration settings for the hiring agent application.
"""

import os

# Global development mode flag
DEVELOPMENT_MODE = True

# Mock mode for testing without LLM API
MOCK_MODE = False

# Fast mode - extract only basics section for quick testing
FAST_MODE = os.getenv("FAST_MODE", "false").lower() == "true"

# Sections to extract (reorder for priority)
# Set to ["basics"] for fastest, or full list for complete extraction
EXTRACT_SECTIONS = ["basics", "work", "education", "skills", "projects", "awards"]
