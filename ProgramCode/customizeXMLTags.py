import xml.etree.ElementTree as ET, os

'''
TODO: create one function each for file and folder traversal XML tag selection
TODO: consider what layout and interface would be the most suitable to show and interact with a large number of XML tags'''

class XMLTagCustomization:
    def traverseDisplaySingleFileInterface(self, XMLFilePath):
        tree = ET.parse(XMLFilePath)
        root = tree.getroot()
        allTagsUnique = []
        
        for elem in root.findall(".//"):
            if elem.tag not in allTagsUnique:
                allTagsUnique.append(elem.tag)
        print(allTagsUnique)
        print(len(allTagsUnique))
        numberOfUniqueTags = len(allTagsUnique)
        return allTagsUnique
    
if __name__ == "__main__":
    XMLFilePath = r"C:\Users\zz341\Desktop\XMLInterface\XMLTraversalTest\A10051.P4.xml"
    XMLFilePath = os.path.normpath(XMLFilePath)
    XMLFolderPath = ""
    customizeXMLTagsMachine = XMLTagCustomization()
    customizeXMLTagsMachine.traverseDisplaySingleFileInterface(XMLFilePath)

