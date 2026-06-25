from typing import List, Optional, Dict, Tuple, Any, Protocol, runtime_checkable
from pydantic import BaseModel, Field, field_validator
from enum import Enum


class ModelProvider(Enum):
    """Enum for supported model providers."""

    OLLAMA = "ollama"
    GEMINI = "gemini"
    OPENAI = "openai"


@runtime_checkable
class LLMProvider(Protocol):
    """Protocol for LLM providers."""

    def chat(
        self,
        model: str,
        messages: List[Dict[str, str]],
        options: Dict[str, Any] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Send a chat request to the LLM provider."""
        ...


class Location(BaseModel):
    """Location information for JSON Resume format."""

    address: Optional[str] = None
    postalCode: Optional[str] = None
    city: Optional[str] = None
    countryCode: Optional[str] = None
    region: Optional[str] = None


class Profile(BaseModel):
    """Social profile information for JSON Resume format."""

    network: Optional[str] = None
    username: Optional[str] = None
    url: str


class Basics(BaseModel):
    """Basic information for JSON Resume format."""

    name: str
    email: Optional[str] = None
    phone: Optional[str] = None
    url: Optional[str] = None
    summary: Optional[str] = None
    location: Optional[Location] = None
    profiles: Optional[List[Profile]] = None


class Work(BaseModel):
    """Work experience for JSON Resume format."""

    name: Optional[str] = None
    position: Optional[str] = None
    url: Optional[str] = None
    startDate: Optional[str] = None
    endDate: Optional[str] = None
    summary: Optional[str] = None
    highlights: Optional[List[str]] = None


class Volunteer(BaseModel):
    """Volunteer experience for JSON Resume format."""

    organization: Optional[str] = None
    position: Optional[str] = None
    url: Optional[str] = None
    startDate: Optional[str] = None
    endDate: Optional[str] = None
    summary: Optional[str] = None
    highlights: Optional[List[str]] = None


class Education(BaseModel):
    """Education information for JSON Resume format."""

    institution: Optional[str] = None
    url: Optional[str] = None
    area: Optional[str] = None
    studyType: Optional[str] = None
    startDate: Optional[str] = None
    endDate: Optional[str] = None
    score: Optional[str] = None
    courses: Optional[List[str]] = None


class Award(BaseModel):
    """Award information for JSON Resume format."""

    title: Optional[str] = None
    date: Optional[str] = None
    awarder: Optional[str] = None
    summary: Optional[str] = None


class Certificate(BaseModel):
    """Certificate information for JSON Resume format."""

    name: Optional[str] = None
    date: Optional[str] = None
    issuer: Optional[str] = None
    url: Optional[str] = None


class Publication(BaseModel):
    """Publication information for JSON Resume format."""

    name: Optional[str] = None
    publisher: Optional[str] = None
    releaseDate: Optional[str] = None
    url: Optional[str] = None
    summary: Optional[str] = None


class Skill(BaseModel):
    """Skill information for JSON Resume format."""

    name: Optional[str] = None
    level: Optional[str] = None
    keywords: Optional[List[str]] = None


class Language(BaseModel):
    """Language information for JSON Resume format."""

    language: Optional[str] = None
    fluency: Optional[str] = None


class Interest(BaseModel):
    """Interest information for JSON Resume format."""

    name: Optional[str] = None
    keywords: Optional[List[str]] = None


class Reference(BaseModel):
    """Reference information for JSON Resume format."""

    name: Optional[str] = None
    reference: Optional[str] = None


class Project(BaseModel):
    """Project information for JSON Resume format."""

    name: Optional[str] = None
    startDate: Optional[str] = None
    endDate: Optional[str] = None
    description: Optional[str] = None
    highlights: Optional[List[str]] = None
    url: Optional[str] = None
    technologies: Optional[List[str]] = None
    skills: Optional[List[str]] = None


class BasicsSection(BaseModel):
    """Basics section containing basic information."""

    basics: Optional[Basics] = None


class WorkSection(BaseModel):
    """Work section containing a list of work experiences."""

    work: Optional[List[Work]] = None


class EducationSection(BaseModel):
    """Education section containing a list of education entries."""

    education: Optional[List[Education]] = None


class SkillsSection(BaseModel):
    """Skills section containing a list of skill categories."""

    skills: Optional[List[Skill]] = None


class ProjectsSection(BaseModel):
    """Projects section containing a list of projects."""

    projects: Optional[List[Project]] = None


class AwardsSection(BaseModel):
    """Awards section containing a list of awards."""

    awards: Optional[List[Award]] = None


class JSONResume(BaseModel):
    """Complete JSON Resume format model."""

    basics: Optional[Basics] = None
    work: Optional[List[Work]] = None
    volunteer: Optional[List[Volunteer]] = None
    education: Optional[List[Education]] = None
    awards: Optional[List[Award]] = None
    certificates: Optional[List[Certificate]] = None
    publications: Optional[List[Publication]] = None
    skills: Optional[List[Skill]] = None
    languages: Optional[List[Language]] = None
    interests: Optional[List[Interest]] = None
    references: Optional[List[Reference]] = None
    projects: Optional[List[Project]] = None


class CategoryScore(BaseModel):
    score: float = Field(ge=0, description="Score achieved in this category")
    max: int = Field(gt=0, description="Maximum possible score")
    evidence: str = Field(min_length=1, description="Evidence supporting the score")


class Scores(BaseModel):
    open_source: CategoryScore
    self_projects: CategoryScore
    production: CategoryScore
    technical_skills: CategoryScore


class BonusPoints(BaseModel):
    total: float = Field(ge=0, le=20, description="Total bonus points")
    breakdown: str = Field(description="Breakdown of bonus points")


class Deductions(BaseModel):
    total: float = Field(
        ge=0,
        description="Total deduction points (stored as positive, applied as negative)",
    )
    reasons: str = Field(description="Reasons for deductions")


class EvaluationData(BaseModel):
    scores: Scores
    bonus_points: BonusPoints
    deductions: Deductions
    key_strengths: List[str] = Field(min_items=1, max_items=5)
    areas_for_improvement: List[str] = Field(min_items=1, max_items=5)


class GitHubProfile(BaseModel):
    """Pydantic model for GitHub profile data."""

    username: str
    name: Optional[str] = None
    bio: Optional[str] = None
    location: Optional[str] = None
    company: Optional[str] = None
    public_repos: Optional[int] = None
    followers: Optional[int] = None
    following: Optional[int] = None
    created_at: Optional[str] = None
    updated_at: Optional[str] = None
    avatar_url: Optional[str] = None
    blog: Optional[str] = None
    twitter_username: Optional[str] = None
    hireable: Optional[bool] = None


class OllamaProvider:
    """Ollama LLM provider implementation."""

    def __init__(self):
        import ollama

        self.client = ollama

    def chat(
        self,
        model: str,
        messages: List[Dict[str, str]],
        options: Dict[str, Any] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Send a chat request to Ollama."""

        ollama_options = options.copy() if options else {}

        # remove steam from ollama options
        ollama_options.pop("stream", None)

        # Add num_ctx 32K context window to options
        ollama_options["num_ctx"] = 32768

        # convert to chat params
        chat_params = {
            "model": model,
            "messages": messages,
            "options": ollama_options,
        }

        # add it to top level
        if "stream" in kwargs:
            chat_params["stream"] = kwargs["stream"]

        if "format" in kwargs:
            chat_params["format"] = kwargs["format"]

        return self.client.chat(**chat_params)


class GeminiProvider:
    """Google Gemini API provider implementation."""

    def __init__(self, api_key: str):
        import google.generativeai as genai

        genai.configure(api_key=api_key)
        self.client = genai

    def chat(
        self,
        model: str,
        messages: List[Dict[str, str]],
        options: Dict[str, Any] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Send a chat request to Google Gemini API."""
        import re
        import time
        import random
        from google.api_core.exceptions import ResourceExhausted

        MAX_RETRIES = 5
        BASE_DELAY = 10.0  # seconds — base for exponential backoff
        MAX_DELAY = 120.0  # cap so we never wait more than 2 minutes

        # Map options to Gemini parameters
        generation_config = {}
        if options:
            if "temperature" in options:
                generation_config["temperature"] = options["temperature"]
            if "top_p" in options:
                generation_config["top_p"] = options["top_p"]

        # Create a Gemini model
        gemini_model = self.client.GenerativeModel(
            model_name=model, generation_config=generation_config
        )

        # Convert messages to Gemini format
        gemini_messages = []
        for msg in messages:
            role = "user" if msg["role"] == "user" else "model"
            gemini_messages.append({"role": role, "parts": [msg["content"]]})

        for attempt in range(MAX_RETRIES):
            try:
                # Send the chat request
                response = gemini_model.generate_content(gemini_messages)

                # Convert Gemini response to Ollama-like format for compatibility
                return {"message": {"role": "assistant", "content": response.text}}

            except ResourceExhausted as e:
                if attempt == MAX_RETRIES - 1:
                    # All retries exhausted — re-raise the original exception.
                    # This surfaces unrecoverable quota errors (RPD, TPM, etc.)
                    # instead of silently failing or returning bad data.
                    raise

                # Parse the API-suggested retry delay from the error message
                match = re.search(r"retry[_ ]in\s+([\d.]+)s", str(e), re.IGNORECASE)
                api_hint = float(match.group(1)) if match else None

                # Exponential backoff: BASE_DELAY * 2^attempt, capped at MAX_DELAY
                exp_delay = min(BASE_DELAY * (2 ** attempt), MAX_DELAY)

                # Prefer the API hint when it is shorter than our computed delay
                delay = api_hint if (api_hint and api_hint < exp_delay) else exp_delay

                # Add ±20% randomized jitter to avoid thundering herd
                sleep_time = round(delay * random.uniform(0.8, 1.2), 2)

                print(
                    f"[GeminiProvider] Rate limit hit "
                    f"(attempt {attempt + 1}/{MAX_RETRIES}). "
                    f"Retrying in {sleep_time}s..."
                )
                time.sleep(sleep_time)


class OpenAIProvider:
    """OpenAI-compatible LLM provider implementation."""

    def __init__(self, api_key: str, base_url: str = None):
        import openai

        self.client = openai.OpenAI(api_key=api_key, base_url=base_url)

    def chat(
        self,
        model: str,
        messages: List[Dict[str, str]],
        options: Dict[str, Any] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Send a chat request to OpenAI-compatible API."""
        import time
        import random
        from openai import RateLimitError

        MAX_RETRIES = 5
        BASE_DELAY = 2.0
        MAX_DELAY = 60.0

        params = {"model": model, "messages": messages}
        if options:
            if "temperature" in options:
                params["temperature"] = options["temperature"]
            if "top_p" in options:
                params["top_p"] = options["top_p"]

        for attempt in range(MAX_RETRIES):
            try:
                response = self.client.chat.completions.create(**params)
                return {
                    "message": {
                        "role": "assistant",
                        "content": response.choices[0].message.content,
                    }
                }
            except RateLimitError as e:
                if attempt == MAX_RETRIES - 1:
                    raise
                delay = min(BASE_DELAY * (2**attempt), MAX_DELAY)
                sleep_time = round(delay * random.uniform(0.8, 1.2), 2)
                print(
                    f"[OpenAIProvider] Rate limit hit "
                    f"(attempt {attempt + 1}/{MAX_RETRIES}). "
                    f"Retrying in {sleep_time}s..."
                )
                time.sleep(sleep_time)
            except Exception as e:
                error_str = str(e)
                if "413" in error_str or "tokens per minute" in error_str.lower():
                    print(
                        f"[OpenAIProvider] Token limit exceeded. "
                        f"Please reduce PDF size or upgrade to Dev Tier."
                    )
                raise


class MockProvider:
    """Mock LLM provider for testing without an API key."""

    def chat(
        self,
        model: str,
        messages: List[Dict[str, str]],
        options: Dict[str, Any] = None,
        **kwargs
    ) -> Dict[str, Any]:
        """Return mock JSON responses for testing."""
        import json
        
        content = ""
        msg_str = str(messages).lower()
        if "basics" in msg_str or "basic" in msg_str:
            content = json.dumps({
                "basics": {
                    "name": "John Doe",
                    "email": "john.doe@example.com",
                    "phone": "+1234567890",
                    "summary": "Software engineer with 5 years experience"
                }
            })
        elif "work" in msg_str or "experience" in msg_str:
            content = json.dumps({"work": [{"company": "Tech Corp", "position": "Senior Engineer", "startDate": "2020", "endDate": "2024"}]})
        elif "skills" in msg_str:
            content = json.dumps({"skills": [{"name": "Python", "level": "Expert"}, {"name": "JavaScript", "level": "Intermediate"}]})
        elif "projects" in msg_str:
            content = json.dumps({"projects": [{"name": "Web App", "description": "Full-stack application"}]})
        elif "education" in msg_str:
            content = json.dumps({"education": [{"institution": "University", "degree": "B.S. Computer Science"}]})
        elif "evaluation" in msg_str or "score" in msg_str:
            content = json.dumps({
                "scores": {
                    "open_source": {"score": 20, "max": 35, "evidence": "Several open source contributions found"},
                    "self_projects": {"score": 15, "max": 30, "evidence": "Personal projects demonstrate initiative"},
                    "production": {"score": 20, "max": 25, "evidence": "Production experience noted"},
                    "technical_skills": {"score": 8, "max": 10, "evidence": "Strong technical skills demonstrated"}
                },
                "bonus_points": {"total": 5, "breakdown": "Bonus for diverse skill set"},
                "deductions": {"total": 0, "reasons": ""},
                "key_strengths": ["Strong problem-solving skills", "Experience with modern technologies"],
                "areas_for_improvement": ["More leadership experience would be beneficial"]
            })
        else:
            content = "{}"
        
        return {"message": {"role": "assistant", "content": content}}
