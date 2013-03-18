code_to_html
============

Author: Sahil Grover

Date:   2013-02-18

A python module for converting code snippets to HTML markup.

*Currently only supports c-like languages.

Documentation
-------------

### Overview

Import the code_to_html python module:

    import code_to_html

Create an instance of the CodeConverter class (it accepts a list of language keywords):

    c = CodeConverter(keywords)

Pass the code (as a string) to the convert_to_html method:

    c.convert_to_html(code)

### Properties

*	keyword_class

	 The CSS class of language keywords.

*	string_class

	 The CSS class of string and character literals.

*	comment_class

	 The CSS class for comments.

*	line_number_class

	 The CSS class for line numbers.

*	spaces_for_tabs

	 The number of spaces to use for tabs.

*	show_line_numbers

	 Show or hide line numbers.