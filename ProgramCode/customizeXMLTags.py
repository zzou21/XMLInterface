import xml.etree.ElementTree as ET, os
'''
Class objects contained in this file: "XMLTagCustomization"
Purpose: an auxiliary function called on by the interface (in the file "ToolInterface.py") to generate a list of all XML tags in the XML file or folder of XML files that the user selects.
Parameters: none, but each of the two functions in this class object takes in either a single XML file path or a directory path of a folder of XML files, depending on the user selection.

NOTE: the two functions both return a list of unique XML tags. For "traverseDisplaySingleFileInterface" function, it returns a list of unique XML tags in the single XML file that the user selected. For "traverseDisplayFolderInterface", it returns a list of unique XML tags from all XML files in the directory selected by the user.
'''

class XMLTagCustomization:
    def __init__(self):
        pass

    def traverseDisplaySingleFileInterface(self, XMLFilePath):
        print(f"Method called with: {XMLFilePath}")

        tree = ET.parse(XMLFilePath)
        root = tree.getroot()
        allTagsUnique = set()
        
        for elem in root.findall(".//"):
            allTagsUnique.add(elem.tag)
        return list(allTagsUnique)

    def traverseDisplayFolderInterface(self, XMLFolderPath):
        allTagsUnique = set()
        for oneXMLFile in os.listdir(XMLFolderPath):
            if oneXMLFile.endswith(".xml"):
                tree = ET.parse(os.path.join(XMLFolderPath, oneXMLFile))
                root = tree.getroot()
                for elem in root.findall(".//"):
                    allTagsUnique.add(elem.tag)
        return list(allTagsUnique)

# Commented code below is for testing purposes only
'''
if __name__ == "__main__":
    XMLFilePath = r"C:\Users\zz341\Desktop\XMLInterface\XMLTraversalTest\A10051.P4.xml"
    XMLFilePath = os.path.normpath(XMLFilePath)
    XMLFolderPath = ""
    customizeXMLTagsMachine = XMLTagCustomization()
    customizeXMLTagsMachine.traverseDisplaySingleFileInterface(XMLFilePath)
'''
