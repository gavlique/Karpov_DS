# function for merging sorted arrays
def merge(a, b):
	i, j = 0, 0
	sorted = [] 
	while i<len(a) and j<len(b):
		if a[i] < b[j]:
			sorted.append(a[i])
			i += 1
		else:
			sorted.append(b[j])
			j += 1
	while i<len(a):
		sorted.append(a[i])
		i += 1
	while j<len(b):
		sorted.append(b[j])
		j += 1
	return sorted
	