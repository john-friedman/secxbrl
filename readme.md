# SEC XBRL

A python package to parse sec xbrl. Supports the [datamule](https://github.com/john-friedman/datamule-python) project.

Intended to be fast & lightweight for SEC inline XBRL. 

Other XBRL Packages may be better for your use-case:
* [tidyxbrl](https://github.com/cowboycodeman/tidyxbrl/)
* [brel](https://github.com/BrelLibrary/brel)
* [py-xbrl](https://github.com/manusimidt/py-xbrl/tree/main)
* [python-xbrl](https://github.com/greedo/python-xbrl)

## Installation
```
pip install secxbrl
```

## `parse_inline_xbrl`
```
parse_inline_xbrl(content=None,filepath=None,encoding='utf-8',file_type='inline')
```

Takes content or filepath, and returns parsed xbrl. File type can be 'inline', e.g. from an inline xbrl html or htm document, or 'extracted_inline' from the xbrl file extracted from the html or htm document. This is usually named something like: tsla-20211231_htm.xml.

## Example
```
from secxbrl import parse_inline_xbrl

# load data
path = '../samples/000095017022000796/tsla-20211231.htm'
with open(path,'rb') as f:
    content = f.read()

# parse data
ix = parse_inline_xbrl(content)
with open('test.txt','w', encoding='utf-8') as f:
    f.writelines([str(item)+'\n\n' for item in ix])

# get all EarningsPerShareBasic
basic = [{'val':item['_val'],'date':item['_context']['context_period_enddate']} for item in ix if item['_attributes']['name']=='us-gaap:EarningsPerShareBasic']
print(basic)
```
