import xml.etree.ElementTree as ET, os

def parse_xml_to_text(file_path, target_tags):
    # Parse the XML file
    tree = ET.parse(file_path)
    root = tree.getroot()
    
    # Define a recursive function to extract text from specific tags
    def extract_text(element):
        text_content = ""
        if element.tag not in target_tags and element.text:
            text_content += element.text.strip() + " "
        for child in element:
            text_content += extract_text(child)
        if element.tail:
            text_content += element.tail.strip() + " "
        return text_content
    
    # Extract text from the entire XML structure
    readable_text = extract_text(root)
    return readable_text


# Specify the path to the XML file
# file_path = r'C:\Users\zz341\Desktop\XMLInterface\XMLTraversalTest\A19313.P4.xml'
file_path = "/Users/Jerry/Desktop/DH proj-reading/XMLInterface/XMLTraversalTest/A19313.P4.xml"
file_path = os.path.normpath(file_path)
tags = {"P", "HI", "NOTE"}
# Convert the XML content to readable text
readable_text = parse_xml_to_text(file_path, tags)

# Save or display the output
output_path = 'output_readable_text.txt'
with open(output_path, 'w', encoding='utf-8') as f:
    f.write(readable_text)

print(f"Readable text has been saved to {output_path}.")
