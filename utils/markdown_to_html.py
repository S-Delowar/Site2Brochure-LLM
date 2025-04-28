import re
import markdown
from markdown.extensions.extra import ExtraExtension


def markdown_to_html(markdown_text):
    """Converts markdown text to HTML."""
    return markdown.markdown(markdown_text, extensions=[ExtraExtension()])