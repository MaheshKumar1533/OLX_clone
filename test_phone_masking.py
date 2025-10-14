#!/usr/bin/env python
"""
Test script to demonstrate phone number masking functionality
"""

import re

def mask_phone_numbers(text):
    """Mask phone numbers in text with asterisks."""
    if not text:
        return text
    
    patterns = [
        r'\+91[\s-]?\d{5}[\s-]?\d{5}',
        r'\+91[\s-]?\d{10}',
        r'\b0\d{10}\b',
        r'\b[6-9]\d{9}\b',
        r'\b\d{3}[\s.-]\d{3}[\s.-]\d{4}\b',
        r'\b\d{5}[\s.-]\d{5}\b',
        r'\(\d{3}\)[\s.-]?\d{3}[\s.-]?\d{4}',
        r'\+\d{1,3}[\s.-]?\d{3,4}[\s.-]?\d{3,4}[\s.-]?\d{3,4}',
        r'\+\d{1,3}[\s.-]?\d{10,12}',
    ]
    
    masked_text = text
    
    for pattern in patterns:
        matches = re.finditer(pattern, masked_text)
        for match in matches:
            original = match.group()
            masked = re.sub(r'\d', '*', original)
            masked_text = masked_text.replace(original, masked)
    
    return masked_text


# Test cases
test_messages = [
    "Hi! Call me at 9876543210",
    "My number is +91 98765 43210",
    "Contact: +919876543210",
    "Reach me on 987-654-3210",
    "Phone: (987) 654-3210",
    "Call 9876543210 or email me",
    "My WhatsApp is +91-98765-43210",
    "Multiple numbers: 9876543210 and 8765432109",
    "Regular text without numbers should not change",
    "Small numbers like 123 or 45678 should not be masked"
]

print("=" * 60)
print("PHONE NUMBER MASKING TEST")
print("=" * 60)
print()

for i, message in enumerate(test_messages, 1):
    masked = mask_phone_numbers(message)
    print(f"Test {i}:")
    print(f"  Original: {message}")
    print(f"  Masked:   {masked}")
    print()

print("=" * 60)
print("All phone numbers should be replaced with asterisks!")
print("=" * 60)
