# MaxDoc

This is an early, highly pluggable, flexible AST-based typesetting
engine for single-sourcing documents.

The intent is to create a single documentation system that:

* Can include sub-documents (summaries of a topic, for instance) and
  reorganise headers etc. accordingly.

* Can limit included content by depth or other characteristics (such
  as tags), to give control over the level of detail included, whilst
  still having a single source of information on a topic.

* Supports pluggable data sources and datatypes, to gather content
  form (text, bibliographies, mail merge data, etc.) from various
  sources, and render them into one OR MORE output documents.

* Supports pluggable backend renderers / output document formats, for
  everything from producing reports and training materials to books,
  audiobooks, and presentations.


Features:

* Powerful AST-based engine, with pluggable AST nodes for adding new
  types of content and new typesetting concepts.
* Pluggable AST transformations. Currently included transformations are:
  - Include files
  - Heading depth limitation (include a file but truncate below heading
    level 2, for example, to limit document size / complexity).
* Built-in database support, with pluggable models and minimal boilerplate,
  for adding features such as bibliographies, authors, addresses, mailmerge
  data, wikipedia data, and so on.
* Pluggable renderers, including a currently implemented template-based
  (jinja2) HTML5 renderer.

These features make MaxDoc an incredibly powerful tool for quickly manipulating 


## To Do

* Add Markdown support, and then generate these docs with maxdoc itself


## Author

* Lee Braiden <mailto:leebraid@gmail.com>
