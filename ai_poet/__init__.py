"""
ai_poet – tiny SDK and CLI for the euron.one chat-completion API.
"""
from importlib.metadata import PackageNotFoundError, version

try:
    __version__ = version(__name__)
except PackageNotFoundError:          # package not yet installed
    __version__ = "0.0.0-dev"

from .generator import generate_poem

__all__ = ["generate_poem", "__version__"]