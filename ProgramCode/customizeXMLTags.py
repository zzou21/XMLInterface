import xml.etree.ElementTree as ET, os

'''
TODO: create one function each for file and folder traversal XML tag selection
TODO: consider what layout and interface would be the most suitable to show and interact with a large number of XML tags'''

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
        numberOfUniqueTags = len(allTagsUnique)
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

# if __name__ == "__main__":
#     XMLFilePath = r"C:\Users\zz341\Desktop\XMLInterface\XMLTraversalTest\A10051.P4.xml"
#     XMLFilePath = os.path.normpath(XMLFilePath)
#     XMLFolderPath = ""
#     customizeXMLTagsMachine = XMLTagCustomization()
#     customizeXMLTagsMachine.traverseDisplaySingleFileInterface(XMLFilePath)

