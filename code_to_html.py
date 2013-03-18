import re

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

	def __init__(self, keyword_list, single_line_comment = "//", multi_line_comment="(/\*|\*/)"):
		self.re_word = re.compile(r'[a-zA-Z0-9_]+')
		self.re_keyword = re.compile('(' + '|'.join(keyword_list) + ')')
		self.keyword_class = 'keyword'

	def __check_token(self, token):
		if token == ' ':
			return '&nbsp;'
		elif token == '\t':
			return '&nbsp;&nbsp;&nbsp;&nbsp;'
		elif token == '<':
			return '&lt;'
		elif token == '>':
			return '&gt;'
		return token

	def __check_word(self, word):
		if self.re_keyword.match(word):
			return '<span class="' + self.keyword_class + '">' + word + '</span>'
		return word

	def __parse_codeline(self, line, in_comment):
		tokens = list(line)
		word = list()
		html = list()
		in_string = False
		string_starter = ''
		prev_t = ''
		single_line_comment = False

		if in_comment:
			html.append('<span class="comment">')

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
						html.append('<span class="string">' + t)
						string_starter = t
						in_string = True
				elif t in ['/', '*']: 
					if prev_t == '/':
						in_comment = True
					elif t == '/' and prev_t == '*':
						in_comment = False
						html.append(t + '</span>')
					if in_comment:
						html.append('<span class="comment">' + prev_t + t)
						single_line_comment = (t == '/')
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
		html = '<table class="code"><tbody>'
		in_comment = False
		for line_number,line in enumerate(code.split('\n')):
			html += '<tr>'
			html += '<td class="line-number">' + str(line_number) + '</td>'
			html += '<td class="code">'
			in_comment, html_line = self.__parse_codeline(line, in_comment)
			html += html_line + '</td>'
			html += '</tr>'
		html += '</tbody></table>'
		return html
