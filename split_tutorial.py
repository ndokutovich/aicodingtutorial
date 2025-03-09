import os
import re

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def extract_sections(content):
    # Pattern to match section headers (both ## N. and # N.)
    section_pattern = r'^#{1,2}\s+(\d+)\.\s+'
    
    lines = content.split('\n')
    sections = {}
    current_section = None
    current_content = []
    
    for line in lines:
        # Check if this is a section header
        match = re.match(section_pattern, line)
        if match:
            # If we were collecting a section, save it
            if current_section is not None:
                sections[current_section] = '\n'.join(current_content)
            
            # Start new section
            current_section = int(match.group(1))
            current_content = [line]
        elif current_section is not None:
            current_content.append(line)
    
    # Don't forget to save the last section
    if current_section is not None and current_content:
        sections[current_section] = '\n'.join(current_content)
    
    return sections

def combine_sections_by_list(sections, section_list, header):
    content = [header]
    for section_num in section_list:
        if section_num in sections:
            content.append(sections[section_num])
    return '\n'.join(content)

def main():
    # Create output directory
    output_dir = 'split_tutorial'
    ensure_dir(output_dir)
    
    # Read the original tutorial
    with open('cursor_tutorial.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # First extract all sections
    sections = extract_sections(content)
    
    # Define the parts and their sections according to the table of contents
    parts = {
        'part1_cursor_basics': {
            'header': '# Часть 1: Основы работы с Cursor IDE\n\n',
            'sections': [1, 2, 3, 4, 7, 8, 16, 18, 19, 20]
        },
        'part2_ai_features': {
            'header': '# Часть 2: Работа с AI в Cursor\n\n',
            'sections': [5, 6, 10, 12, 13]
        },
        'part3_tech_integration': {
            'header': '# Часть 3: Технологии и интеграции\n\n',
            'sections': [11, 14, 15, 17]
        }
    }
    
    # Create each part by combining appropriate sections
    for filename, part_info in parts.items():
        content = combine_sections_by_list(
            sections,
            part_info['sections'],
            part_info['header']
        )
        
        # Write the part to a file
        output_file = os.path.join(output_dir, f'{filename}.md')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write(content)
    
    # Print found sections for verification
    print("Found sections:", sorted(sections.keys()))
    print("Tutorial has been successfully split into three parts!")

if __name__ == "__main__":
    main() 