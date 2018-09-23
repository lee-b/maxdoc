# MaxDoc

This is an early, highly pluggable, flexible AST-based typesetting
engine for single-sourcing documents.

## Overview

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

* Has a modern, lightweight, but formal syntax without the adhoc mess that
  is markdown, ReST, etc., nor the unwieldy IDE-assisted mess that is
  bookbook etc. Final syntax will probably look something like \em{
  emphasised text here}.

Most of the above currently works, for at least one proof-of-concept
source/format/output. The main feature missing is the input parser -
currently the only "input" is in the form a intermediate AST yaml dump
files.

## Features

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
documents and 


## To Do

* Decide on the input format and add a parser for it.
* Genericise the HTML5 jinja2 renderer into a jinja2 rendering base class plus
  a jinja2-based html5 renderer.
* Add Markdown support, and then generate these docs with maxdoc itself
* Separate the config-context into two distinct objects.
* Split context further into loading context, transformation context, and
  rendering context?
* Move the db support into the context
* Make the pluggable features more formally separate plugins, and auto-load them
  from paths.
* Add support for multiple dbs
* Add support for non-DB datasources (such as an interface to directly load
  content from wikipedia -- with heading level truncation / tag selection,
  this could insert summaries of a given subject).


## Author

* Lee Braiden <mailto:leebraid@gmail.com>
