import os
import glob
from lxml import html

def parse_glossary_file(file_path):
    try:
        # Try to parse with lxml's auto-detection
        tree = html.parse(file_path)
    except (IOError, html.etree.XMLSyntaxError):
        # If auto-detection fails, try with big5
        try:
            parser = html.HTMLParser(encoding='big5')
            tree = html.parse(file_path, parser=parser)
        except (IOError, html.etree.XMLSyntaxError, UnicodeDecodeError) as e:
            print(f"Could not parse {file_path} with lxml and big5: {e}")
            return []

    entries = []
    tables = tree.xpath('//table[@border="0" and @cellspacing="2"]')
    for table in tables:
        term_tag = table.xpath('.//font[@size="+1" and @color="#006600"]')
        if not term_tag:
            continue

        term_text = term_tag[0].text_content().strip()
        if not term_text:
            continue
            
        entry_data = {'term': term_text}

        rows = table.xpath('.//tr')
        for row in rows:
            cells = row.xpath('.//td')
            if len(cells) >= 2:
                field_name_tag = cells[0].find('.//font')
                if field_name_tag is not None:
                    field_name = field_name_tag.text_content().strip()
                    field_value_tag = cells[1].find('.//font')
                    if field_value_tag is not None:
                        field_value = field_value_tag.text_content().strip()
                        entry_data[field_name] = field_value

        entries.append(entry_data)

    return entries

def main():
    all_entries = []
    processed_terms = set()
    for file_path in glob.glob('C*.HTML') + glob.glob('C*.html'):
        entries = parse_glossary_file(file_path)
        for entry in entries:
            term = entry.get('term')
            if term and term not in processed_terms:
                all_entries.append(entry)
                processed_terms.add(term)

    with open('glossary.md', 'w', encoding='utf-8') as f:
        for entry in sorted(all_entries, key=lambda x: x.get('term', '')):
            f.write(f"## {entry.get('term', 'N/A')}\n\n")
            for key, value in entry.items():
                if key != 'term':
                    f.write(f"**{key}:** {value}\n\n")
            f.write('---\n\n')

if __name__ == '__main__':
    main()
