from code_to_html import CodeConverter

f = open('keywords/cs_keywords.txt', 'r')
keywords = f.read().split('\n')
f.close()

f = open('code_snippets/snippet1.cs')
code = f.read()
f.close()

c = CodeConverter(keywords)
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