from render_html import HTMLRenderer
from render_pdf import PDFRenderer
from render_utf8 import UTF8Renderer

ALL_RENDERERS = {
    "html": HTMLRenderer()
    "pdf": PDFRenderer()
    "utf8": UTF8Renderer()
}
