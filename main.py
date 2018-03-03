import sqlite3
import os
import operator
from collections import OrderedDict
import pylab as plt


def parse(url):
	try:
		parsed_url_components = url.split('//')
		sublevel_split = parsed_url_components[1].split('/', 1)
		domain = sublevel_split[0].replace("www.", "")
		return domain
	except IndexError:
		print ("Error reading URL")	# print "" syntax no longer works for python v3.x

# \\ used instead of \ due to :
# Typical error on Windows because the default user directory is C:\user\<your_user>,
# so when you want to use this path as an string parameter into a Python function,
# you get a Unicode error, just because the \u is a Unicode escape. Any character not numeric after this produces an error.

data_path = os.path.expanduser('~')+"\\AppData\\Local\\Google\\Chrome\\User Data\\Default" #path to user's history database (Chrome)
files = os.listdir(data_path)

history_db = os.path.join(data_path, 'history')


#db querying
c = sqlite3.connect(history_db)
cursor = c.cursor()
select_statement = "SELECT urls.url, urls.visit_count FROM urls, visits WHERE urls.id = visits.url;"
cursor.execute(select_statement)

results = cursor.fetchall() #tuple

sites_count = {} #dict

for url, count in results:
	url = parse(url)
	if url in sites_count:
		sites_count[url] += 1
	else:
		sites_count[url] = 1

sites_count_sorted = OrderedDict(sorted(sites_count.items(), key=operator.itemgetter(1), reverse=True))

index = []	# Don't hardcode the indices. Append indices later depending on count length(max 10).

count = list(sites_count_sorted.values())[:10]	# Whatever the no. of sites are, limit it to <= 10.

# Making sure len(count) = len(index)
l = len(count)
for i in range (0, l):
	index.append(i)

LABELS = list(sites_count_sorted.items())[:10]

plt.bar(index, count, align='center')	# length of index & count list must be same, otherwise will throw shape mismatch error.
plt.xticks(index, LABELS, rotation = 14)	# default rotation = 0
plt.show()

# The program doesn't run while chrome is running (throws database lock error).
# index & count length automated.
# The labels appear congested, so rotation = 14 is applied.
