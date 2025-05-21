import re

def escape_markdown(text, version=1):
    """Escape markdown characters in a string.
    
    Parameters:
        text (``str``):
            The text to escape.
            
        version (``int``, optional):
            The Markdown version (1 or 2). Defaults to 1.
            
    Returns:
        ``str``: The escaped text.
        
    Example:
        .. code-block:: python
        
            # Escape Markdown v1
            escaped_text = escape_markdown("*bold* _italic_")
            
            # Escape Markdown v2
            escaped_text = escape_markdown("**bold** __italic__", version=2)
    """
    if version == 1:
        # Markdown v1 escape characters: _ * [ ] ( )
        return re.sub(r"([_*\[\]()~`>#\+\-=|{}.!])", r"\\\1", str(text))
    else:
        # Markdown v2 escape characters: _ * [ ] ( ) ~ ` > # + - = | { } . !
        escape_chars = r"\_\*\[\]\(\)~`>#\+\-=\|{}.!"
        return re.sub(f"([{re.escape(escape_chars)}])", r"\\\1", str(text))


def escape_html(text):
    """Escape HTML characters in a string.
    
    Parameters:
        text (``str``):
            The text to escape.
            
    Returns:
        ``str``: The escaped text.
        
    Example:
        .. code-block:: python
        
            escaped_text = escape_html("<b>bold text</b>")
    """
    return text.replace("&", "&amp;").replace("<", "&lt;").replace(">", "&gt;") 