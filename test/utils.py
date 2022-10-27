"""Collection of helper functions to support testing."""
import json
from test import TEST_DATA
from typing import Any, Dict

TEST_URL = "https://www.youtube.com/watch?v=_Rl82OQDoOc"


def load_config() -> Dict[str, Any]:
    """Load config dict from a file."""
    return json.load((TEST_DATA / "config.json").open())
