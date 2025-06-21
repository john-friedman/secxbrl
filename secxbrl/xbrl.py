from selectolax.parser import HTMLParser

# <xbrli:context id="c-1">
#     <xbrli:entity>
#         <xbrli:identifier scheme="http://www.sec.gov/CIK">0001703056</xbrli:identifier>
#     </xbrli:entity>
#     <xbrli:period>
#         <xbrli:startDate>2025-01-01</xbrli:startDate>
#         <xbrli:endDate>2025-03-31</xbrli:endDate>
#     </xbrli:period>
# </xbrli:context>

def xbrl_node_to_dict(node):
    if node is None:
        return None
    
    result = {}
    prefix_stack = []
    for child in node.traverse():
        text_content = child.text_content
        if text_content is None:
            prefix.append()

    return result



def ix_node_to_dict(node):
    if node is None:
        return None
    
    result = {}
    
    text = node.text(deep=True, strip=True,separator ='\n')
    if text:
        result['_val'] = text

    result['_attributes'] = node.attributes
    
    return result


def parse_inline_xbrl(html_content):
    parser = HTMLParser(html_content)
    
    ix_nodes = []
    xbrl_nodes = []

    # for ix nodes lets just convert to dict
    
    # Get all elements and filter by tag name
    for node in parser.root.traverse():
        tag = node.tag.lower()
        if tag and tag in ['ix:nonfraction','ix:nonnumeric']:
            ix_nodes.append(ix_node_to_dict(node))
        elif tag and tag == 'xbrli:context':
            xbrl_nodes.append(xbrl_node_to_dict(node))
    
    return ix_nodes,xbrl_nodes