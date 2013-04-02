import re

class CommentStyle:
	SCRIPT, C = range(2)

class CodeConverter:
	"""Convert code to HTML markup"""

	def keyword_class():
	    doc = "The CSS class of language keywords."
	    def fget(self):
	        return self._keyword_class
	    def fset(self, value):
	        self._keyword_class = value
	    return locals()
	keyword_class = property(**keyword_class())

	def string_class():
	    doc = "The CSS class of string and character literals."
	    def fget(self):
	        return self._string_class
	    def fset(self, value):
	        self._string_class = value
	    return locals()
	string_class = property(**string_class())

	def comment_class():
	    doc = "The CSS class for comments."
	    def fget(self):
	        return self._comment_class
	    def fset(self, value):
	        self._comment_class = value
	    return locals()
	comment_class = property(**comment_class())

	def line_number_class():
	    doc = "The CSS class for line numbers."
	    def fget(self):
	        return self._line_number_class
	    def fset(self, value):
	        self._line_number_class = value
	    return locals()
	line_number_class = property(**line_number_class())
	
	def spaces_for_tabs():
	    doc = "The number of spaces to use for tabs."
	    def fget(self):
	        return self._spaces_for_tabs
	    def fset(self, value):
	        self._spaces_for_tabs = value
	    return locals()
	spaces_for_tabs = property(**spaces_for_tabs())

	def show_line_numbers():
	    doc = "Show or hide line numbers."
	    def fget(self):
	        return self._show_line_numbers
	    def fset(self, value):
	        self._show_line_numbers = value
	    return locals()
	show_line_numbers = property(**show_line_numbers())

	def comment_style():
	    doc = "Set language comment style (c or script)"
	    def fget(self):
	        return self._comment_style
	    def fset(self, value):
	        self._comment_style = value
	    return locals()
	comment_style = property(**comment_style())

	def __init__(self, keyword_list, single_line_comment = "//", multi_line_comment="(/\*|\*/)"):
		self.re_word = re.compile(r'[a-zA-Z0-9_]+')
		self.re_keyword = re.compile('(' + '|'.join(keyword_list) + ')')
		self.keyword_class = 'keyword'
		self.string_class = 'string'
		self.comment_class = 'comment'
		self.spaces_for_tabs = 4
		self.show_line_numbers = True
		self.line_number_class = 'line-number'
		self.comment_style = CommentStyle.C

	def __check_token(self, token):
		if token == ' ':
			return '&nbsp;'
		elif token == '\t':
			return '&nbsp;' * self.spaces_for_tabs
		elif token == '<':
			return '&lt;'
		elif token == '>':
			return '&gt;'
		return token

	def __check_word(self, word):
		if self.re_keyword.match(word):
			return '<span class="' + self.keyword_class + '">' + word + '</span>'
		return word

	def __is_start_comment(self, t, prev_t):
		return (prev_t == '/' and t in ['/', '*'] and self.comment_style == CommentStyle.C) or (t == '#' and self.comment_style == CommentStyle.SCRIPT)

	def __is_end_comment(self, t, prev_t):
		return t == '/' and prev_t == '*' and self.comment_style == CommentStyle.C

	def __is_single_line_comment(self, t):
		return (t == '/' and self.comment_style == CommentStyle.C) or (t == '#' and self.comment_style == CommentStyle.SCRIPT)

	def __is_comment_character(self, t):
		return (t in ['/', '*'] and self.comment_style == CommentStyle.C) or (t == '#' and self.comment_style == CommentStyle.SCRIPT)

	def __is_comment_symbol(self, prev_t, t):
		if t == '#' and self.comment_style == CommentStyle.SCRIPT:
			return True

		symbol = prev_t + t
		return symbol in ['/*', '*/', '//']

	def __parse_codeline(self, line, in_comment):
		tokens = list(line)
		word = list()
		html = list()
		in_string = False
		string_starter = ''
		prev_t = ''
		single_line_comment = False

		if in_comment:
			html.append('<span class="' + self.comment_class + '">')

		for t in tokens:
			match = self.re_word.match(t)
			if match:
				word.append(t)
			else:

				if word:	# end of a new word
					new_word = ''.join(word)
					if not (in_string or in_comment):
						new_word = self.__check_word(new_word)	# is the word a keyword?
					html.append(new_word)
					word = list()

				if t in ['"', "'"] and not in_comment:
					if in_string:
						if string_starter != t:
							html.append(t)
						elif string_starter == t and prev_t == '\\':	# escaped quote
							html.append(t)
						elif string_starter == t:	# end of string
							html.append(t + '</span>')
							in_string = False
					else:	# start of string
						html.append('<span class="' + self.string_class + '">' + t)
						string_starter = t
						in_string = True 

				elif self.__is_comment_character(t):
					if self.__is_start_comment(t, prev_t):
						in_comment = True
					elif self.__is_end_comment(t, prev_t):
						in_comment = False
						html.append(t + '</span>')

					if in_comment:
						html.append('<span class="' + self.comment_class + '">' + prev_t + t)
						single_line_comment = self.__is_single_line_comment(t)

				# this handles a comment character that wasn't used for a comment (gets skipped on previous iteration)
				elif self.__is_comment_character(prev_t) and not in_comment and not self.__is_comment_symbol(prev_t, t):
					new_token = self.__check_token(prev_t) + self.__check_token(t)
					html.append(new_token)

				else:
					new_token = self.__check_token(t)
					html.append(new_token)
			
			prev_t = t

		# check word one last time because end of line token isn't picked up
		if word:
			html.append( self.__check_word( "".join(word) ) )

		if in_comment:
			html.append('</span>')
			in_comment = not single_line_comment

		return in_comment, "".join(html)

	def convert_to_html(self, code):
		"""Convert code to HTML markup and return as string."""
		html = '<table class="code"><tbody>'
		in_comment = False
		for line_number,line in enumerate(code.split('\n')):
			html += '<tr>'
			if self.show_line_numbers:
				html += '<td class="' + self.line_number_class + '">' + str(line_number) + '</td>'
			html += '<td class="code">'
			in_comment, html_line = self.__parse_codeline(line, in_comment)
			html += html_line + '</td>'
			html += '</tr>'
		html += '</tbody></table>'
		return html
