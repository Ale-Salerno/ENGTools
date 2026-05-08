#!/usr/bin/env python3
import os
import glob
from lxml import etree

def process_trans_unit(tu, ns):
    """
    For each <trans-unit>:
      - Extract plain text from <seg-source> (ignoring any markup, e.g. <mrk> tags).
      - If a <target> exists, remove all its child nodes and update its text with the plain text.
      - Otherwise, create a new <target> element (with state="translated") immediately after the <source> element.
      - Remove the <seg-source> element.
    """
    seg_source = tu.find('ns:seg-source', namespaces=ns)
    if seg_source is None:
        return

    # Extract plain text from seg-source (ignoring any child markup)
    plain_text = ''.join(seg_source.itertext()).strip()

    # Check for an existing <target> element
    target = tu.find('ns:target', namespaces=ns)
    if target is not None:
        # Remove any children from target without clearing its attributes
        for child in list(target):
            target.remove(child)
        target.text = plain_text
    else:
        # Create a new <target> element with state="translated"
        target = etree.Element(etree.QName(ns['ns'], "target"))
        target.text = plain_text
        target.set("state", "translated")
        # Insert the new target immediately after the <source> element if possible
        source_elem = tu.find('ns:source', namespaces=ns)
        if source_elem is not None:
            source_elem.addnext(target)
        else:
            tu.insert(0, target)

    # Remove the seg-source element
    tu.remove(seg_source)

def process_file(filepath):
    parser = etree.XMLParser(remove_blank_text=True)
    tree = etree.parse(filepath, parser)
    root = tree.getroot()

    # Build namespace mapping.
    # Map the default namespace to "ns".
    ns = {}
    if None in root.nsmap:
        ns['ns'] = root.nsmap[None]
    else:
        for key, uri in root.nsmap.items():
            if key is not None:
                ns['ns'] = uri
                break
    # Also include the "se" namespace if available
    if "se" in root.nsmap:
        ns["se"] = root.nsmap["se"]

    # Process all <trans-unit> elements.
    trans_units = root.xpath(".//ns:trans-unit", namespaces=ns)
    for tu in trans_units:
        process_trans_unit(tu, ns)

    # Get the target-language attribute from the first <file> element.
    file_elems = root.xpath(".//ns:file", namespaces=ns)
    target_lang = file_elems[0].get("target-language", "target") if file_elems else "target"

    base_name = os.path.splitext(os.path.basename(filepath))[0]
    output_filename = f"{base_name}_{target_lang}_out.xlf"

    # Serialize the XML with UTF-8, XML declaration, and pretty printing
    xml_bytes = etree.tostring(
        root,
        encoding='UTF-8',
        xml_declaration=True,
        pretty_print=True
    )

    # Add UTF-8 BOM and convert line endings to Windows CR LF
    xml_bytes = b'\xEF\xBB\xBF' + xml_bytes  # Prepend BOM
    xml_bytes = xml_bytes.replace(b'\n', b'\r\n')  # Convert LF to CR LF

    # Write the final content to the output file
    with open(output_filename, 'wb') as f:
        f.write(xml_bytes)
    
    print(f"Processed '{filepath}' -> '{output_filename}'")

def main():
    xlf_files = glob.glob("*.xlf")
    if not xlf_files:
        print("No .xlf files found in the current directory.")
        return
    for filepath in xlf_files:
        process_file(filepath)

if __name__ == '__main__':
    main()