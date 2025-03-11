import os
import json
import re

def ensure_dir(directory):
    if not os.path.exists(directory):
        os.makedirs(directory)

def load_section_groups(config_file='section_groups.json'):
    """Load section grouping configuration from a JSON file."""
    if os.path.exists(config_file):
        with open(config_file, 'r', encoding='utf-8') as f:
            return json.load(f)
    return None

def read_section_file(section_num, input_dir):
    """Read a section file from the input directory."""
    filename = f'section_{str(section_num).zfill(2)}.md'
    filepath = os.path.join(input_dir, filename)
    
    if not os.path.exists(filepath):
        print(f"Warning: Section file {filename} not found")
        return None
        
    with open(filepath, 'r', encoding='utf-8') as f:
        return f.read()

def extract_section_caption(content):
    """Extract the section caption from the content."""
    if not content:
        return None
    
    # Try to find the first header line
    lines = content.split('\n')
    for line in lines:
        # Match any level header with a number (e.g., "# 1. Some Caption" or "## 15. Some Caption")
        match = re.match(r'^#{1,2}\s+\d+\.\s+(.+)$', line)
        if match:
            return match.group(1)
    return None

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

def create_table_of_contents(section_groups, input_dir):
    """Create a table of contents based on the section groups."""
    toc = ["# Руководство по использованию Cursor IDE\n\n## Содержание\n"]
    current_section = 1
    
    for group_name, group_info in section_groups.items():
        # Add group header
        group_header = group_info['header'].split('\n')[0].replace('# ', '')
        toc.append(f"\n### {group_header}")
        
        # Add sections in this group to TOC
        for old_section_num in group_info.get('sections', []):
            # Read section content to get its caption
            section_content = read_section_file(old_section_num, input_dir)
            caption = extract_section_caption(section_content)
            
            if caption:
                toc.append(f"- [{current_section}. {caption}](#section-{current_section})")
            else:
                toc.append(f"- [{current_section}. Раздел {old_section_num}](#section-{current_section})")
            current_section += 1
    
    return '\n'.join(toc)

def merge_sections(input_dir, output_file, section_groups):
    """Merge sections according to configuration and create a single file."""
    # Start with table of contents
    content = [create_table_of_contents(section_groups, input_dir)]
    current_section = 1
    
    # Add each group and its sections
    for group_name, group_info in section_groups.items():
        # Add group header
        content.append(f"\n\n{group_info['header']}")
        
        # Add sections in this group
        for old_section_num in group_info.get('sections', []):
            section_content = read_section_file(old_section_num, input_dir)
            if section_content:
                # Renumber the section
                numbered_content = renumber_section_content(section_content, current_section)
                content.append(numbered_content)
                current_section += 1
        
        # Add separator between groups
        content.append("\n---\n")
    
    # Write the merged content
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write('\n'.join(content))

def main():
    input_dir = 'split_tutorial'
    output_file = 'cursor_tutorial_merged.md'
    
    # Load section groups configuration
    section_groups = load_section_groups()
    if not section_groups:
        print("Error: Could not load section groups configuration")
        return
    
    # Merge sections and create the output file
    merge_sections(input_dir, output_file, section_groups)
    print(f"Successfully merged sections into {output_file}")
    print("Sections have been renumbered according to their order in the configuration")

if __name__ == "__main__":
    main() 