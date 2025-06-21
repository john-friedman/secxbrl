from secxbrl import parse_inline_xbrl
from time import time

s = time()
with open('000095017022000796/tsla-20211231.htm','rb') as f:
    content = f.read()

ix = parse_inline_xbrl(content)
with open('test.txt','w', encoding='utf-8') as f:
    f.writelines([str(item)+'\n\n' for item in ix])



    