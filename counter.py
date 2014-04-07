import re
import gzip
from os import listdir
from os import path
from collections import Counter
from itertools import chain
from fnmatch import fnmatch
from datetime import datetime

try:
    from local_settings import GITLAB_LOG_PATH
except ImportError:
    GITLAB_LOG_PATH = '/home/git/gitlab/log/'


# pattern definition
patterns = [re.compile(pattern) for pattern in (
    # siempre buscamos requests de tipo GET
    # puede venir un pedido a los archive
    r'Started GET "/([\w-]+/[\w-]+)/repository/archive\..*at (\d{4}-\d{2}-\d{2})',
    # o un clone por HTTP
    r'Started GET "/([\w-]+/[\w-]+)(?:\.git)?/info/refs\?service=git-upload-pack".*at (\d{4}-\d{2}-\d{2})',
    # o un clone por SSH
    r'Started GET "//api/v3/internal/allowed\?key_id=\d+&action=git-upload-pack&ref=_any&project=([\w-]+/[\w-]+)".*at (\d{4}-\d{2}-\d{2})'
)]

results = []

# compressed logs
for f in listdir(GITLAB_LOG_PATH):
    if fnmatch(f, 'production.log.*.gz'):
        contents = gzip.open(path.join(GITLAB_LOG_PATH, f)).read()
        results += chain.from_iterable(re.findall(pattern, contents) for \
            pattern in patterns)

# non compressed logs
for f in ('production.log', 'production.log.1'):
    contents = open(path.join(GITLAB_LOG_PATH, f)).read()
    results += chain.from_iterable(re.findall(pattern, contents) for \
        pattern in patterns)

# print results
print('Namespace/Project\tDownloads\tLast activity')
for project, count in Counter(x[0] for x in results).most_common():
    print('%s\t%d\t%s' % (project, count, max(datetime.strptime(x[1],
        '%Y-%m-%d').date() for x in results if x[0]==project)))
