from code_to_html import CodeConverter, CommentStyle
import keyword

keywords = keyword.kwlist

f = open('code_snippets/snippet2.py')
code = f.read()
f.close()

c = CodeConverter(keywords)
c.comment_style = CommentStyle.SCRIPT
html = c.convert_to_html(code)
f = open('output.html', 'w+')
f.write("""
	<!DOCTYPE html>
	<html>
		<head>
			<title>Sample Code</title>
			<link href="code.css" rel="stylesheet" />
		</head>
		<body>
		</body>
		"""
		+ html +
		"""
	</html>
	""")
f.close()