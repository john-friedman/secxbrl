from selectolax.parser import HTMLParser
import re

# cribbed from doc2dict
def walk(node):
    yield ("start",node)
    for child in node.iter(include_text=True):
        yield from walk(child)

    yield ("end",node)


def xbrl_node_to_dict(node):
    if node is None:
        return None
    
    result = {'_contextref':node.id}
    prefix_stack = []

    for signal, node in walk(node):
        if signal == 'start':
            text_content = node.text_content
            text_content = text_content.strip() if text_content else None

            if text_content is None or text_content == '':
                prefix_stack.append(node.tag.split(':')[-1])
            else:
                key = '_'.join(prefix_stack)
                
                # Special handling for context_entity_segment_explicitmember
                if key == 'entity_segment_explicitmember':
                    if key in result:
                        result[key].append(text_content)
                    else:
                        result[key] = [text_content]
                else:
                    result[key] = text_content
        else:
            prefix = node.tag.split(':')[-1]
            if len(prefix_stack) > 0:
                if prefix == prefix_stack[-1]:
                    prefix_stack = prefix_stack[:-1]

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

def parse_inline_xbrl(html_content=None,filepath=None,encoding='utf-8'):
    if filepath:
        with open(filepath,'r',encoding=encoding) as f:
            html_content = f.read()

    parser = HTMLParser(html_content)
    ix_nodes = []
    xbrl_nodes = []

    # First pass: collect all nodes
    count = 0
    for node in parser.body.traverse():
        # return if not inline xbrl
        if count == 1:
            style = node.attributes.get('style', '').lower()
            if not re.search(r'display\s*:\s*none', style):
                return ix_nodes
            
        tag = node.tag.lower()
        if tag and tag in ['ix:nonfraction', 'ix:nonnumeric']:
            ix_nodes.append(ix_node_to_dict(node))
        elif tag and tag == 'xbrli:context':
            xbrl_nodes.append(xbrl_node_to_dict(node))
        count += 1
    

    # Create context lookup dictionary
    context_lookup = {ctx['_contextref']: ctx for ctx in xbrl_nodes}
    
    # Second pass: link contexts to ix nodes and clean up attributes
    for ix_node in ix_nodes:
        if '_attributes' in ix_node and 'contextref' in ix_node['_attributes']:
            contextref = ix_node['_attributes']['contextref']
            
            # Add context information
            if contextref in context_lookup:
                ix_node['_context'] = context_lookup[contextref]
            
            # Remove contextref from attributes
            del ix_node['_attributes']['contextref']
    
    return ix_nodes