import os
import re
import json

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

def renumber_section_content(content, new_number):
    """Renumber a section's content with a new section number."""
    # Pattern to match section headers (both ## N. and # N.)
    section_pattern = r'^(#{1,2})\s+\d+\.'
    
    lines = content.split('\n')
    new_lines = []
    
    for line in lines:
        # Check if this is a section header
        match = re.match(section_pattern, line)
        if match:
            # Replace the old number with the new one
            hashes = match.group(1)
            new_line = re.sub(r'^#{1,2}\s+\d+\.', f'{hashes} {new_number}.', line)
            new_lines.append(new_line)
        else:
            # Also update any subsection references like "### 1.1" to match new number
            subsection_match = re.match(r'^(#{3,})\s+\d+\.(\d+)', line)
            if subsection_match:
                hashes = subsection_match.group(1)
                subsection = subsection_match.group(2)
                new_line = re.sub(r'^#{3,}\s+\d+\.\d+', f'{hashes} {new_number}.{subsection}', line)
                new_lines.append(new_line)
            else:
                new_lines.append(line)
    
    return '\n'.join(new_lines)

def save_section_file(section_num, content, output_dir, new_number=None):
    """Save a section to an individual file with optional renumbering."""
    if new_number is not None:
        content = renumber_section_content(content, new_number)
        filename = f'section_{str(new_number).zfill(2)}.md'
    else:
        filename = f'section_{str(section_num).zfill(2)}.md'
    
    filepath = os.path.join(output_dir, filename)
    
    with open(filepath, 'w', encoding='utf-8') as f:
        f.write(content)
    
    return filename

def load_section_groups(config_file='section_groups.json'):
    """Load section grouping configuration from a JSON file."""
    if os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def create_section_groups(sections, section_groups, output_dir):
    """Create grouped files based on configuration with sequential numbering within groups."""
    if not section_groups:
        return
        
    for group_name, group_info in section_groups.items():
        content = [group_info.get('header', f'# {group_name}\n\n')]
        section_list = group_info.get('sections', [])
        
        # Add sections with renumbered content
        for new_num, old_num in enumerate(section_list, 1):
            if old_num in sections:
                section_content = renumber_section_content(sections[old_num], new_num)
                content.append(section_content)
        
        # Write the group file
        output_file = os.path.join(output_dir, f'{group_name}.md')
        with open(output_file, 'w', encoding='utf-8') as f:
            f.write('\n'.join(content))

def main():
    # Create output directory
    output_dir = 'split_tutorial'
    ensure_dir(output_dir)
    
    # Read the original tutorial
    with open('cursor_tutorial.md', 'r', encoding='utf-8') as f:
        content = f.read()
    
    # First extract all sections
    sections = extract_sections(content)
    
    # Save each section as a separate file with sequential numbering
    sorted_sections = sorted(sections.keys())
    for new_num, old_num in enumerate(sorted_sections, 1):
        filename = save_section_file(old_num, sections[old_num], output_dir, new_num)
        print(f"Created section file: {filename} (original section {old_num})")
    
    # Load section groups configuration if exists
    section_groups = load_section_groups()
    if section_groups:
        create_section_groups(sections, section_groups, output_dir)
        print("Created section group files according to configuration with renumbered sections")
    
    # Print found sections for verification
    print("Found sections:", sorted_sections)
    print("Tutorial has been successfully split into individual section files with sequential numbering!")

if __name__ == "__main__":
    main() 