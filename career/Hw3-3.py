def is_subsequence(s, t):
	if len(s) == 0 and len(t) == 0:
		return True
	if len(s) == 0 or len(t) == 0:
		return False
	i = 0
	for letter in range(len(s)):
		while t[i] != s[letter] and i < len(t):
			i += 1
			if i == len(t):
				return False
	return True

print(is_subsequence('ab', 'a'))