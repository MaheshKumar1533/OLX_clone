import re
from django import template
from django.utils.safestring import mark_safe

register = template.Library()


@register.filter(name='mask_phone_numbers')
def mask_phone_numbers(text):
    """
    Mask phone numbers in text with asterisks.
    Supports various formats:
    - 10-digit numbers: 9876543210
    - With country code: +919876543210, +91 9876543210
    - With separators: 987-654-3210, 987.654.3210, (987) 654-3210
    - International formats
    """
    if not text:
        return text
    
    # Pattern to match phone numbers with various formats
    patterns = [
        # Indian numbers with +91 country code (with or without spaces/hyphens)
        r'\+91[\s-]?\d{5}[\s-]?\d{5}',
        r'\+91[\s-]?\d{10}',
        
        # Indian numbers with 0 prefix
        r'\b0\d{10}\b',
        
        # 10-digit numbers (most common)
        r'\b[6-9]\d{9}\b',
        
        # Numbers with spaces/hyphens/dots (10 digits total)
        r'\b\d{3}[\s.-]\d{3}[\s.-]\d{4}\b',
        r'\b\d{5}[\s.-]\d{5}\b',
        
        # Numbers with parentheses like (123) 456-7890
        r'\(\d{3}\)[\s.-]?\d{3}[\s.-]?\d{4}',
        
        # International format with country code
        r'\+\d{1,3}[\s.-]?\d{3,4}[\s.-]?\d{3,4}[\s.-]?\d{3,4}',
        r'\+\d{1,3}[\s.-]?\d{10,12}',
    ]
    
    masked_text = text
    
    for pattern in patterns:
        # Find all matches
        matches = re.finditer(pattern, masked_text)
        for match in matches:
            # Replace each match with asterisks
            original = match.group()
            # Keep the format (spaces, hyphens, etc) but replace digits with *
            masked = re.sub(r'\d', '*', original)
            masked_text = masked_text.replace(original, masked)
    
    return masked_text


@register.filter(name='mask_phone_numbers_html')
def mask_phone_numbers_html(text):
    """
    Mask phone numbers and return as safe HTML (for use with linebreaks filter)
    """
    masked = mask_phone_numbers(text)
    return mark_safe(masked)
