import re
import gzip
from os import listdir
from collections import Counter
from itertools import chain
from fnmatch import fnmatch

# pattern definition
patterns = [re.compile(pattern) for pattern in (
    # siempre buscamos requests de tipo GET
    # puede venir un pedido a los archive
    r'Started GET "/([\w-]+/[\w-]+)/repository/archive\.',
    # o un clone por HTTP
    r'Started GET "/([\w-]+/[\w-]+)(?:\.git)?/info/refs\?service=git-upload-pack"',
    # o un clone por SSH
    r'Started GET "//api/v3/internal/allowed\?key_id=\d+&action=git-upload-pack&ref=_any&project=([\w-]+/[\w-]+)"'
)]

results = []

# compressed logs
for f in listdir('.'):
    if fnmatch(f, 'production.log.*.gz'):
	contents = gzip.open(f).read()
        results += chain.from_iterable(re.findall(pattern, contents) for pattern in patterns)

# non compressed logs
for f in ('production.log', 'production.log.1'):
    contents = open(f).read()
    results += chain.from_iterable(re.findall(pattern, contents) for pattern in patterns)

# print results
print('Namespace/Project\tDownloads')
for project, count in Counter(results).most_common():
    print('%s\t%d' % (project, count))
