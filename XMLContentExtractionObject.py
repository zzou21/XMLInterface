import xml.etree.ElementTree as ET

class XMLContentExtraction:
    def __init__ (self, XMLSourcePath, XMLCustomizedTagsList):
        self.XMLSourcePath = XMLSourcePath
        self.XMLCustomizedTagsList = XMLCustomizedTagsList

    def traverseXML(self):
        tree = ET.parse(self.XMLSourcePath)
        root = tree.getroot()
        for elem in root.findall(".//*"):
            print(elem.tag, elem.text)
            

if __name__ == "__main__":
    XMLSourcePath = "/Users/Jerry/Desktop/DH proj-reading/XMLInterface/A67213.P4 copy.xml"
    XMLCustomizedTagsList = []
    XMLParsingTool = XMLContentExtraction(XMLSourcePath, XMLCustomizedTagsList)
    XMLParsingTool.traverseXML()