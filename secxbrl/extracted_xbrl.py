import xml.etree.ElementTree as ET
import re
import html

def html_to_text(html_content):
    # First decode HTML entities like &#xA0; to regular characters
    text = html.unescape(html_content)
    
    # Remove all HTML tags with regex
    text = re.sub(r'<[^>]+>', '', text)
    
    # Clean up extra whitespace
    text = re.sub(r'\s+', ' ', text).strip()
    
    return text

def extract_namespace_mapping(content):
    """Extract namespace prefix to URL mapping from root element"""
    xmlns_pattern = r'xmlns:([a-zA-Z0-9_-]+)="([^"]+)"'
    matches = re.findall(xmlns_pattern, content)
    return {url: prefix for prefix, url in matches}

def get_prefixed_name(tag, namespace_map):
    """Convert {namespace_url}element_name to prefix:element_name"""
    if tag.startswith('{'):
        namespace_url, element_name = tag[1:].split('}', 1)
        prefix = namespace_map.get(namespace_url, '')
        return f"{prefix}:{element_name}" if prefix else element_name
    return tag

def content_node_to_dict(node, namespace_map):
    result = {}
    
    text = node.text
    if text:
        result['_val'] = html_to_text(text)

    result['_attributes'] = node.attrib
    result['_attributes']['name'] = get_prefixed_name(node.tag, namespace_map) 

    return result

def context_node_to_dict(node):
    result = {'_contextref': node.get('id')}
    
    def process_element(elem, prefix_path=[]):
        tag_name = elem.tag.split('}')[-1].lower()
        current_path = prefix_path + [tag_name]
        
        if elem.text and elem.text.strip() and len(elem) == 0:
            key = '_'.join(current_path)
            value = elem.text.strip()
            
            # Special handling for entity_segment_explicitmember
            if key == 'entity_segment_explicitmember':
                if key in result:
                    result[key].append(value)
                else:
                    result[key] = [value]
            else:
                result[key] = value
        
        for child in elem:
            process_element(child, current_path)
    
    for child in node:
        process_element(child)
    
    return result
def parse_extracted_xbrl(xml_content, filepath,encoding='utf-8'):
    if filepath:
        with open(filepath,'r',encoding=encoding) as f:
            xml_content = f.read()

    namespace_map = extract_namespace_mapping(xml_content)

    root = ET.fromstring(xml_content)

    context_nodes = []
    content_nodes = []
    for child in root:
        tag_name = child.tag.split('}')[-1]
        if tag_name == 'context':
            context_nodes.append(child)
        elif 'contextRef' in child.attrib:
            content_nodes.append(child)

    content_dicts = []
    context_dicts = []

    for content_node in content_nodes:
        content_dicts.append(content_node_to_dict(content_node, namespace_map))

    for context_node in context_nodes:
        context_dicts.append(context_node_to_dict(context_node))

    context_lookup = {ctx['_contextref']: ctx for ctx in context_dicts}

    for content_dict in content_dicts:
        contextref = content_dict['_attributes']['contextRef']
        if contextref in context_lookup:
            content_dict['_context'] = context_lookup[contextref]
        del content_dict['_attributes']['contextRef']

    return content_dicts