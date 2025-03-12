import os
import re
import argparse
import unicodedata

def slugify(text):
    """Convert text to a format suitable for use in URLs and anchors."""
    # Normalize unicode characters
    text = unicodedata.normalize('NFKD', text)
    # Convert to ASCII, ignore non-ASCII characters
    ascii_text = ''.join(c for c in text if not unicodedata.combining(c) and ord(c) < 128)
    # Convert to lowercase
    ascii_text = ascii_text.lower()
    # Replace spaces with hyphens
    ascii_text = ascii_text.replace(' ', '-')
    # Remove non-alphanumeric characters
    ascii_text = re.sub(r'[^a-z0-9\-]', '', ascii_text)
    # Replace multiple hyphens with a single hyphen
    ascii_text = re.sub(r'-+', '-', ascii_text)
    # Remove leading and trailing hyphens
    ascii_text = ascii_text.strip('-')
    
    # If we have only numbers after processing, add a prefix
    if re.match(r'^\d+$', ascii_text):
        ascii_text = f"section-{ascii_text}"
        
    return ascii_text

def parse_document(content):
    """Parse the document and identify all sections and subsections up to 4 levels deep."""
    # Split content into lines
    lines = content.split('\n')
    
    # Initialize section tracking
    sections = []
    current_section = None
    current_subsection = None
    current_subsubsection = None
    toc_lines = []
    toc_start = -1
    toc_end = -1
    
    # Debug counters
    debug_patterns = {
        'section_matches': 0,
        'subsection_matches': 0,
        'subsubsection_matches': 0,
        'unmatched_headers': []
    }
    
    # Find TOC boundaries and sections
    in_toc = False
    for i, line in enumerate(lines):
        # Look for TOC start
        if re.match(r'^#+\s+Содержание', line) or re.match(r'^#+\s+Оглавление', line):
            toc_start = i
            in_toc = True
            toc_lines.append(line)
            continue
            
        # If we're in TOC, collect lines until we hit a non-TOC section
        if in_toc:
            if re.match(r'^#+\s+', line) and not re.match(r'^###\s+', line):  # Major header, not a TOC subsection
                toc_end = i - 1
                in_toc = False
            else:
                toc_lines.append(line)
                continue
        
        # Process main section headers (level 1-2)
        section_match = re.match(r'^(#{1,2})\s+(\d+)\.(\s+.+)$', line)
        if section_match:
            hashes = section_match.group(1)
            section_title = section_match.group(3)
            
            # Record section
            section_info = {
                'index': i,
                'level': len(hashes),
                'title': section_title.strip(),
                'line': line,
                'subsections': []
            }
            sections.append(section_info)
            current_section = section_info
            current_subsection = None
            current_subsubsection = None
            debug_patterns['section_matches'] += 1
            continue
            
        # Process level 3 headers (subsections) - try multiple patterns
        if current_section:
            # Try pattern 1: ### N.M Title
            subsection_match = re.match(r'^(#{3})\s+(\d+)\.(\d+)(\s+.+)$', line)
            
            # Try pattern 2: ### N.M. Title (note the extra dot)
            if not subsection_match:
                alt_match = re.match(r'^(#{3})\s+(\d+)\.(\d+)\.(\s+.+)$', line)
                if alt_match:
                    subsection_match = alt_match
                    # Adjust groups to match the expected format from pattern 1
                    subsection_match = re.match(r'^(#{3})\s+(\d+)\.(\d+)(\..+)$', line)
            
            # Try pattern 3: ###N.M Title (no space after ###)
            if not subsection_match:
                alt_match = re.match(r'^(#{3})(\d+)\.(\d+)(\s+.+)$', line)
                if alt_match:
                    subsection_match = alt_match
            
            if subsection_match:
                hashes = subsection_match.group(1)
                section_num = subsection_match.group(2)
                subsection_num = subsection_match.group(3)
                subsection_title = subsection_match.group(4)
                
                # Record subsection
                subsection_info = {
                    'index': i,
                    'level': len(hashes),
                    'section_num': section_num,
                    'number': subsection_num,
                    'title': subsection_title.strip(),
                    'line': line,
                    'subsubsections': []
                }
                current_section['subsections'].append(subsection_info)
                current_subsection = subsection_info
                current_subsubsection = None
                debug_patterns['subsection_matches'] += 1
                continue
        
        # Process level 4 headers (sub-subsections) - try multiple patterns
        if current_subsection:
            # Try pattern 1: #### N.M.K Title
            subsubsection_match = re.match(r'^(#{4})\s+(\d+)\.(\d+)\.(\d+)(\s+.+)$', line)
            
            # Try pattern 2: #### N.M.K. Title (note the extra dot)
            if not subsubsection_match:
                alt_match = re.match(r'^(#{4})\s+(\d+)\.(\d+)\.(\d+)\.(\s+.+)$', line)
                if alt_match:
                    subsubsection_match = alt_match
                    # Adjust groups to match expected format
                    subsubsection_match = re.match(r'^(#{4})\s+(\d+)\.(\d+)\.(\d+)(\..+)$', line)
            
            if subsubsection_match:
                hashes = subsubsection_match.group(1)
                section_num = subsubsection_match.group(2)
                subsection_num = subsubsection_match.group(3)
                subsubsection_num = subsubsection_match.group(4)
                subsubsection_title = subsubsection_match.group(5)
                
                # Record sub-subsection
                subsubsection_info = {
                    'index': i,
                    'level': len(hashes),
                    'section_num': section_num,
                    'subsection_num': subsection_num,
                    'number': subsubsection_num,
                    'title': subsubsection_title.strip(),
                    'line': line
                }
                current_subsection['subsubsections'].append(subsubsection_info)
                current_subsubsection = subsubsection_info
                debug_patterns['subsubsection_matches'] += 1
                continue
        
        # Log any header-like lines that weren't matched
        if not in_toc and re.match(r'^#{1,4}\s+.+$', line):
            debug_patterns['unmatched_headers'].append((i+1, line))
    
    # If TOC end wasn't found, set it to last TOC line
    if toc_end == -1 and toc_start != -1 and len(toc_lines) > 1:
        toc_end = toc_start + len(toc_lines) - 1
    
    return {
        'lines': lines,
        'sections': sections,
        'toc': {
            'start': toc_start,
            'end': toc_end,
            'lines': toc_lines
        },
        'debug': debug_patterns
    }

def generate_toc(sections):
    """Generate a table of contents from sections with up to 4 levels of depth."""
    toc = ["# Содержание\n"]
    
    for i, section in enumerate(sections, 1):
        # Generate a proper heading ID
        section_text = f"{i}. {section['title']}"
        section_slug = slugify(section_text)
        
        # For sections, we'll use a simple, reliable format
        section_id = f"section-{i}"
        
        # Add section to TOC
        indent = "  " * (section['level'] - 1)
        toc.append(f"{indent}- [{section_text}](#{section_id})")
        
        # Add subsections to TOC if present
        for j, subsection in enumerate(section['subsections'], 1):
            # Generate a proper heading ID for subsection
            subsection_text = f"{i}.{j} {subsection['title']}"
            subsection_id = f"section-{i}-{j}"
            
            sub_indent = "  " * subsection['level']
            toc.append(f"{sub_indent}- [{subsection_text}](#{subsection_id})")
            
            # Add sub-subsections to TOC if present
            for k, subsubsection in enumerate(subsection.get('subsubsections', []), 1):
                # Generate a proper heading ID for sub-subsection
                subsubsection_text = f"{i}.{j}.{k} {subsubsection['title']}"
                subsubsection_id = f"section-{i}-{j}-{k}"
                
                subsub_indent = "  " * subsubsection['level']
                toc.append(f"{subsub_indent}- [{subsubsection_text}](#{subsubsection_id})")
    
    return toc

def renumber_document(doc_info):
    """Renumber all sections and subsections in the document up to 4 levels deep."""
    lines = doc_info['lines'].copy()
    sections = doc_info['sections']
    
    # Generate new TOC
    new_toc = generate_toc(sections)
    
    # Replace old TOC
    toc_start = doc_info['toc']['start']
    toc_end = doc_info['toc']['end']
    
    if toc_start >= 0 and toc_end >= toc_start:
        # Remove old TOC
        lines = lines[:toc_start] + lines[toc_end+1:]
        
        # Insert new TOC
        lines = lines[:toc_start] + new_toc + lines[toc_start:]
        
        # Adjust section indices for the TOC change
        toc_diff = len(new_toc) - (toc_end - toc_start + 1)
        for section in sections:
            if section['index'] > toc_end:
                section['index'] += toc_diff
            for subsection in section['subsections']:
                if subsection['index'] > toc_end:
                    subsection['index'] += toc_diff
                for subsubsection in subsection.get('subsubsections', []):
                    if subsubsection['index'] > toc_end:
                        subsubsection['index'] += toc_diff
    
    # Renumber sections and subsections and add HTML anchors
    for i, section in enumerate(sections, 1):
        old_index = section['index']
        # Add HTML anchor before the section header
        section_id = f"section-{i}"
        lines[old_index] = f'<a id="{section_id}"></a>\n' + re.sub(r'^(#{1,2})\s+\d+\.', f"\\1 {i}.", lines[old_index])
        
        # Renumber subsections
        for j, subsection in enumerate(section['subsections'], 1):
            sub_index = subsection['index']
            # Add HTML anchor
            subsection_id = f"section-{i}-{j}"
            
            # Handle both patterns (with and without trailing dot)
            if '.' in lines[sub_index].split()[1] and lines[sub_index].split()[1].endswith('.'):
                lines[sub_index] = f'<a id="{subsection_id}"></a>\n' + re.sub(r'^(#{3})\s+\d+\.\d+\.', f"\\1 {i}.{j}.", lines[sub_index])
            else:
                lines[sub_index] = f'<a id="{subsection_id}"></a>\n' + re.sub(r'^(#{3})\s+\d+\.\d+', f"\\1 {i}.{j}", lines[sub_index])
            
            # Renumber sub-subsections
            for k, subsubsection in enumerate(subsection.get('subsubsections', []), 1):
                subsub_index = subsubsection['index']
                # Add HTML anchor
                subsubsection_id = f"section-{i}-{j}-{k}"
                
                # Handle both patterns (with and without trailing dot)
                if '.' in lines[subsub_index].split()[1] and lines[subsub_index].split()[1].endswith('.'):
                    lines[subsub_index] = f'<a id="{subsubsection_id}"></a>\n' + re.sub(r'^(#{4})\s+\d+\.\d+\.\d+\.', 
                                               f"\\1 {i}.{j}.{k}.", lines[subsub_index])
                else:
                    lines[subsub_index] = f'<a id="{subsubsection_id}"></a>\n' + re.sub(r'^(#{4})\s+\d+\.\d+\.\d+', 
                                               f"\\1 {i}.{j}.{k}", lines[subsub_index])
    
    return '\n'.join(lines)

def print_unmatched_headers(doc_info):
    """Print information about headers that couldn't be matched."""
    unmatched = doc_info['debug']['unmatched_headers']
    if unmatched:
        print("\nUnmatched headers (couldn't parse format):")
        for line_num, line in unmatched:
            print(f"Line {line_num}: {line}")
        print("\nCheck if these headers match the expected format patterns.")
        print("For sections: '# N. Title' or '## N. Title'")
        print("For subsections: '### N.M Title'")
        print("For sub-subsections: '#### N.M.K Title'")

def main():
    parser = argparse.ArgumentParser(description='Renumber sections and update table of contents in a Markdown file.')
    parser.add_argument('input_file', help='Path to the input Markdown file')
    parser.add_argument('--output', '-o', help='Path to the output file (default: input_file with _renumbered suffix)')
    parser.add_argument('--debug', '-d', action='store_true', help='Enable debug mode to see more information')
    args = parser.parse_args()
    
    # Set default output file if not specified
    input_file = args.input_file
    if args.output:
        output_file = args.output
    else:
        name, ext = os.path.splitext(input_file)
        output_file = f"{name}_renumbered{ext}"
    
    # Read input file
    with open(input_file, 'r', encoding='utf-8') as f:
        content = f.read()
    
    # Parse and process the document
    doc_info = parse_document(content)
    
    # Print debug info
    if args.debug or doc_info['debug']['subsection_matches'] == 0:
        print("\nHeader pattern matching:")
        print(f"Main section headers found: {doc_info['debug']['section_matches']}")
        print(f"Subsection headers found: {doc_info['debug']['subsection_matches']}")
        print(f"Sub-subsection headers found: {doc_info['debug']['subsubsection_matches']}")
        
        # Check first 20 lines to see formats
        print("\nSample of document lines (first 20):")
        for i, line in enumerate(doc_info['lines'][:20]):
            if re.match(r'^#{1,5}\s+', line):
                print(f"Line {i+1}: {line}")
        
        print_unmatched_headers(doc_info)
    
    # Update the document
    updated_content = renumber_document(doc_info)
    
    # Write output file
    with open(output_file, 'w', encoding='utf-8') as f:
        f.write(updated_content)
    
    print(f"\nSuccessfully renumbered sections in {input_file}")
    print(f"Updated document saved to {output_file}")
    
    # Count all sections and subsections
    subsection_count = sum(len(s['subsections']) for s in doc_info['sections'])
    subsubsection_count = sum(sum(len(ss.get('subsubsections', [])) for ss in s['subsections']) for s in doc_info['sections'])
    print(f"Found {len(doc_info['sections'])} sections, {subsection_count} subsections, and {subsubsection_count} sub-subsections")

if __name__ == "__main__":
    main() 