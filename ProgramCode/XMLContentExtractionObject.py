import xml.etree.ElementTree as ET, os

class XMLContentExtraction:
    def __init__ (self, XMLSourcePath, XMLCustomizedTagsList, outputName):
        self.XMLSourcePath = XMLSourcePath
        self.XMLCustomizedTagsList = XMLCustomizedTagsList
        self.outputName = outputName

    def traverseXML(self):
        tree = ET.parse(self.XMLSourcePath)
        root = tree.getroot()
        allTags = []
        allContent = []

        for elem in root.findall(".//"):
            if elem.tag not in allTags:
                allTags.append(elem.tag)
            if elem.tag in self.XMLCustomizedTagsList:
                allContent.append(elem.text)
        
        filteredAllContent = [item for item in allContent if item is not None]

        with open(self.outputName, "w") as testFile:
            testFile.write("".join(filteredAllContent))

# if __name__ == "__main__":
#     XMLSourcePath = "/Users/Jerry/Desktop/DH proj-reading/XMLInterface/XMLTraversalTest/A16864.P4.xml"
#     XMLCustomizedTagsList = ['TITLESTMT', 'TITLE', 'AUTHOR', 'EXTENT', 'PUBLICATIONSTMT']
#     XMLParsingTool = XMLContentExtraction(XMLSourcePath, XMLCustomizedTagsList)
#     XMLParsingTool.traverseXML()