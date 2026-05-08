#!/usr/bin/env python3
import glob
import copy
import xml.etree.ElementTree as ET

# Register namespaces to preserve the original prefixes
ET.register_namespace('', 'urn:oasis:names:tc:xliff:document:1.2')
ET.register_namespace('its', 'http://www.w3.org/2005/11/its')
ET.register_namespace('okp', 'okapi-framework:xliff-extensions')
ET.register_namespace('itsxlf', 'http://www.w3.org/ns/its-xliff/')

def pseudo_translate_text(text):
    """Transform each character:
       - Uppercase -> 'X'
       - Lowercase -> 'x'
       - Digit     -> 'N'
       - All others remain unchanged.
    """
    if text is None:
        return None
    result = ""
    for char in text:
        if char.isupper():
            result += "X"
        elif char.islower():
            result += "x"
        elif char.isdigit():
            result += "N"
        else:
            result += char
    return result

def transform_mrk(mrk_elem):
    """
    Pseudo-translate only the text directly inside a <mrk> element:
      - Transform the element's text.
      - For each child element, transform its tail text.
      - Do NOT transform any text inside nested child elements.
    """
    if mrk_elem.text:
        mrk_elem.text = pseudo_translate_text(mrk_elem.text)
    for child in mrk_elem:
        if child.tail:
            child.tail = pseudo_translate_text(child.tail)
    return mrk_elem

def process_file(filename):
    tree = ET.parse(filename)
    root = tree.getroot()
    ns = {'ns': 'urn:oasis:names:tc:xliff:document:1.2'}

    # For each <trans-unit>...
    for trans_unit in root.findall('.//ns:trans-unit', ns):
        seg_source = trans_unit.find('ns:seg-source', ns)
        target = trans_unit.find('ns:target', ns)
        if seg_source is not None and target is not None:
            target.clear()
            # Copy seg-source's text outside of child elements as-is.
            target.text = seg_source.text
            for child in seg_source:
                # Determine the local tag name (without namespace)
                tag_local = child.tag.split('}')[-1] if '}' in child.tag else child.tag
                new_child = copy.deepcopy(child)
                if tag_local == 'mrk':
                    # Only pseudo-translate text within <mrk> elements.
                    transform_mrk(new_child)
                # For any other tag (or if not <mrk>) we leave its content intact.
                target.append(new_child)
    tree.write(filename, encoding='UTF-8', xml_declaration=True)

def main():
    for filename in glob.glob("*.xlf"):
        process_file(filename)
        print(f"Processed {filename}")

if __name__ == '__main__':
    main()
