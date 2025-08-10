from .inline_xbrl import parse_inline_xbrl as parse_inline
from .extracted_xbrl import parse_extracted_xbrl as parse_extracted

def parse_inline_xbrl(content=None, filepath=None, encoding='utf-8', file_type='inline'):
    # Check if content is bytes and decode it
    if content is not None and isinstance(content, bytes):
        content = content.decode(encoding)
    
    if file_type == 'inline':
        return parse_inline(content, filepath, encoding)
    elif file_type == 'extracted_inline':
        return parse_extracted(content, filepath, encoding)