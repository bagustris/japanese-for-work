#!/usr/bin/env python3
"""
Script to split the Japanese for Work ODT content into individual markdown files
"""

import re
import os

def clean_content(text):
    """Remove metadata lines and clean up the text"""
    lines = text.split('\n')
    cleaned_lines = []
    skip_patterns = [
        r'Bagus Tris Atmaja',
        r'Unknown Author',
        r'^\d{4}-\d{2}-\d{2}T\d{2}:\d{2}:\d{2}',
        r'^　$',
    ]
    
    for line in lines:
        # Skip lines matching metadata patterns
        should_skip = any(re.match(pattern, line.strip()) for pattern in skip_patterns)
        if not should_skip and line.strip():
            cleaned_lines.append(line)
    
    return '\n'.join(cleaned_lines)

def split_into_lessons(content):
    """Split content into individual lessons"""
    # Find all lesson markers
    lesson_pattern = r'^#(\d+)'
    
    lessons = {}
    current_lesson = None
    current_content = []
    
    lines = content.split('\n')
    for line in lines:
        match = re.match(lesson_pattern, line.strip())
        if match:
            # Save previous lesson if exists
            if current_lesson and current_content:
                lessons[current_lesson] = '\n'.join(current_content)
            
            # Start new lesson
            current_lesson = int(match.group(1))
            current_content = [line]
        elif current_lesson:
            current_content.append(line)
    
    # Save last lesson
    if current_lesson and current_content:
        lessons[current_lesson] = '\n'.join(current_content)
    
    return lessons

def extract_lesson_title(content):
    """Extract the lesson title from content"""
    lines = content.split('\n')
    # Look for the title in the first few lines after the #N marker
    for i, line in enumerate(lines[1:10], 1):
        # Japanese titles often contain these patterns
        if any(char in line for char in ['　', 'を', 'に', 'の', 'で', 'が', 'と']):
            if len(line.strip()) > 10 and len(line.strip()) < 100:
                return line.strip()
    return None

# Read the extracted content
with open('extracted_content.txt', 'r', encoding='utf-8') as f:
    content = f.read()

# Clean the content
cleaned_content = clean_content(content)

# Split into lessons
lessons = split_into_lessons(cleaned_content)

# Create lessons directory
os.makedirs('lessons', exist_ok=True)

# Save each lesson to a separate markdown file
for lesson_num in sorted(lessons.keys()):
    if lesson_num <= 33:  # Only process existing lessons
        lesson_content = lessons[lesson_num]
        title = extract_lesson_title(lesson_content)
        
        filename = f"lessons/lesson_{lesson_num:02d}.md"
        
        with open(filename, 'w', encoding='utf-8') as f:
            f.write(f"# Lesson {lesson_num}")
            if title:
                f.write(f": {title}")
            f.write("\n\n")
            f.write(lesson_content)
        
        print(f"Created {filename}")

print(f"\nTotal lessons extracted: {len([k for k in lessons.keys() if k <= 33])}")
