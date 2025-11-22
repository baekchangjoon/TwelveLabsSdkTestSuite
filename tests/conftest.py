"""
pytest configuration and common fixture definitions
"""

import json
import os

import pytest
from twelvelabs import TwelveLabs
from twelvelabs.core.api_error import ApiError


def _load_env_file():
    """Load environment variables from config.env file."""
    env_file = os.path.join(os.path.dirname(os.path.dirname(__file__)), "config.env")
    if os.path.exists(env_file):
        with open(env_file, "r", encoding="utf-8") as f:
            for line in f:
                line = line.strip()
                # Skip comments and empty lines
                if not line or line.startswith("#"):
                    continue
                # Parse KEY=VALUE format
                if "=" in line:
                    key, value = line.split("=", 1)
                    key = key.strip()
                    value = value.strip()
                    # Set environment variable only if not already set
                    if key and value and key not in os.environ:
                        os.environ[key] = value


# Load environment variables file when pytest starts
_load_env_file()


@pytest.fixture(scope="session")
def api_key():
    """Get API key from environment variable or config.env file."""
    api_key = os.getenv("TL_API_KEY")
    if not api_key:
        raise ValueError(
            "TL_API_KEY environment variable is not set. Please check config.env file or set the environment variable."
        )
    return api_key


@pytest.fixture(scope="function")
def index_id(request):
    """Get index ID from environment variable or config.env file.

    If a fixture name is passed from parametrize, return the value of that fixture.

    Note: scope="function" is set to correctly handle different parameter values
    for each test function when used with indirect=True.
    """
    # If fixture name is passed from parametrize
    if (
        hasattr(request, "param")
        and isinstance(request.param, str)
        and request.param.startswith("index_")
    ):
        return request.getfixturevalue(request.param)

    # Default behavior: get from environment variable
    index_id = os.getenv("TL_INDEX_ID")
    if not index_id:
        raise ValueError(
            "TL_INDEX_ID environment variable is not set. Please check config.env file or set the environment variable."
        )
    return index_id


@pytest.fixture(scope="session")
def index_marengo27():
    """Get Marengo 2.7 index ID from environment variable or config.env file."""
    index_id = os.getenv("TL_INDEX_MARENGO_27")
    if not index_id:
        pytest.skip(
            "TL_INDEX_MARENGO_27 environment variable is not set. Please check config.env file or set the environment variable."
        )
    return index_id


@pytest.fixture(scope="session")
def index_marengo30():
    """Get Marengo 3.0 index ID from environment variable or config.env file."""
    index_id = os.getenv("TL_INDEX_MARENGO_30")
    if not index_id:
        pytest.skip(
            "TL_INDEX_MARENGO_30 environment variable is not set. Please check config.env file or set the environment variable."
        )
    return index_id


@pytest.fixture(scope="session")
def client(api_key):
    """Create a TwelveLabs client instance."""
    return TwelveLabs(api_key=api_key)


def get_index_name(request) -> str:
    """
    Extract the index name used in pytest request.

    Args:
        request: pytest request fixture

    Returns:
        Index name string (e.g., "index_marengo27", "index_marengo30", "default")
    """
    if hasattr(request, "node") and hasattr(request.node, "callspec"):
        return request.node.callspec.params.get("index_id", "default")
    return "default"


def is_marengo30(index_name: str) -> bool:
    """
    Determine Marengo version by index name.

    Args:
        index_name: Index name (e.g., "index_marengo27", "index_marengo30")

    Returns:
        True if Marengo 3.0, False if Marengo 2.7
    """
    return index_name == "index_marengo30"


def get_error_code(api_error: ApiError) -> str:
    """
    Extract error code from ApiError.

    Args:
        api_error: ApiError instance

    Returns:
        Error code string, empty string if extraction fails
    """
    if not api_error.body:
        return ""

    # Try JSON parsing if body is a string
    if isinstance(api_error.body, str):
        try:
            body_dict = json.loads(api_error.body)
        except (json.JSONDecodeError, TypeError):
            return ""
    else:
        body_dict = api_error.body

    # ErrorResponse format: {"error": {"code": "...", "message": "..."}}
    if isinstance(body_dict, dict):
        if "error" in body_dict and isinstance(body_dict["error"], dict):
            return body_dict["error"].get("code", "")
        # BadRequestErrorBody format: {"code": "...", "message": "..."}
        elif "code" in body_dict:
            return body_dict.get("code", "")

    return ""


def validate_marengo_fields(item, index_name: str = None, request=None):
    """
    Validate that important fields exist according to Marengo version.

    Marengo 2.7: start, end, score, confidence
    Marengo 3.0: start, end, video_id, rank, transcription

    Args:
        item: SearchItem instance
        index_name: Index name (optional)
        request: pytest request (optional, used when index_name is not provided)
    """
    if not index_name and request:
        index_name = get_index_name(request)
    elif not index_name:
        index_name = "default"

    is_30 = is_marengo30(index_name)

    # Common fields
    assert item.start is not None, f"start is required (index: {index_name})"
    assert item.end is not None, f"end is required (index: {index_name})"
    assert item.start < item.end, f"start must be less than end (index: {index_name})"

    if is_30:
        # Marengo 3.0 fields
        assert (
            item.video_id is not None
        ), f"video_id is required (Marengo 3.0, index: {index_name})"
        assert (
            item.rank is not None
        ), f"rank is required (Marengo 3.0, index: {index_name})"
        assert isinstance(
            item.rank, int
        ), f"rank must be an integer (Marengo 3.0, index: {index_name})"
        assert (
            item.rank > 0
        ), f"rank must be greater than or equal to 1 (Marengo 3.0, index: {index_name})"
        # transcription is optional, so it can be None
    else:
        # Marengo 2.7 fields
        assert (
            item.score is not None
        ), f"score is required (Marengo 2.7, index: {index_name})"
        assert (
            item.confidence is not None
        ), f"confidence is required (Marengo 2.7, index: {index_name})"
        assert isinstance(
            item.score, (int, float)
        ), f"score must be a number (Marengo 2.7, index: {index_name})"
        assert item.confidence in [
            "high",
            "medium",
            "low",
        ], f"confidence must be one of 'high', 'medium', 'low' (Marengo 2.7, index: {index_name})"
