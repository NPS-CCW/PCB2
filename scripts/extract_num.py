s = 'hello X42 I\'m a Y-32.35 string Z30'
xy = ("X", "Y")
num_char = (".", "+", "-")

l = []

tokens = s.split()
for token in tokens:
	
	#Track maximum dims
	if token.startswith(xy):
		num = ""
		for char in token:
			# print(char)
			if char.isdigit() or (char in num_char):
				num = num + char
		
		try:
			l.append(float(num))
		except ValueError:
			pass

print(l)