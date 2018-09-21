from .render_html import HTMLRenderer
from .render_pdf import PDFRenderer
from .render_utf8 import UTF8Renderer
from .render_html_jinja2 import Jinja2HTMLRenderer

ALL_RENDERERS = {
    "html": HTMLRenderer(),
    "html_jinja2": Jinja2HTMLRenderer(["../templates/html/jinja2"]),
    "pdf": PDFRenderer(),
    "utf8": UTF8Renderer(),
}
