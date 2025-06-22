from secxbrl import parse_inline_xbrl

path = '../samples/000095017022000796/tsla-20211231.htm'
with open(path,'rb') as f:
    content = f.read()

ix = parse_inline_xbrl(content)
with open('test.txt','w', encoding='utf-8') as f:
    f.writelines([str(item)+'\n\n' for item in ix])

# get all EarningsPerShareBasic
basic = [{'val':item['_val'],'date':item['_context']['context_period_enddate']} for item in ix if item['_attributes']['name']=='us-gaap:EarningsPerShareBasic']
print(basic)