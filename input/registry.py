# - scripts/load/registry.py

from input.parse_html import parse_html
from input.parse_pdf import parse_pdf
from input.parse_text import parse_text

PARSER_REGISTRY = {
    ".html": parse_html,
    ".txt": parse_text,
    ".pdf": parse_pdf,
}
