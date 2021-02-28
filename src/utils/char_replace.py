# Function replaces characters. Use here to remove non-unicode chars
translation_table = dict.fromkeys(map(ord, 'Ã\x9f'), None)

def CharReplace(stuff):
	for slist, item in enumerate(stuff):
		if isinstance(item, list):
			CharReplace(item)
		elif 'Ã\x9f' in item:
			stuff[slist] = item.translate(translation_table)
	return stuff