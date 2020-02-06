import json
# Clean data from a csv of messages
# Data has to be cleaned before training
""" 
Known errors:
	* empty text message
	* out Of range index (perfection on delimiter of new     CSV )
"""

clean = []
with open('text.csv') as t:
	raw = t.read()
	lines = raw.split(';')
	msgs = (line.split('~') for line in lines)
	for i in msgs:
		try:
			if not i[2] or i[2]!= '':
				clean.append(i[2])
		except:
			continue

with open('clean_messages.json', 'w') as t:
	clean.reverse()
	json.dump(clean, t)