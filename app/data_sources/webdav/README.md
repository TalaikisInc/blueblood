# easywebdav3

This is a quick port/ fix to Python 3. Tested for text download, nothing else.

Original: https://github.com/amnong/easywebdav

## Code example

```python
from os.path import join, dirname

from easywebdav3 import easywebdav


webdav = easywebdav.Client(host=HOST, port=PORT, username=USERNAME, password=PASSWORD)
for item in  webdav.ls():
    f = open(join(dirname(__file__), item[0]), 'w')
    webdav.download(from_filename, f)
    f.close()```
