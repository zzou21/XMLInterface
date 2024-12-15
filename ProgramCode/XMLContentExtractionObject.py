import xml.etree.ElementTree as ET, os

class XMLContentExtraction:
    def __init__ (self, XMLSourcePath, XMLCustomizedTagsList, outputName):
        self.XMLSourcePath = XMLSourcePath
        self.XMLCustomizedTagsList = XMLCustomizedTagsList
        self.outputName = outputName

    def traverseAndOutputXML(self):
        tree = ET.parse(self.XMLSourcePath)
        root = tree.getroot()

        allContent = self.extractContent(root)

        with open(self.outputName, "w", encoding = "utf-8") as testFile:
            testFile.write("".join(allContent))
    
    def extractContent(self, element, level = 0):
        extractedText = []
        if element.tag in self.XMLCustomizedTagsList:
            if element.text and element.text.strip():
                extractedText.append("  " * level + element.text.strip())
        for child in element:
            extractedText.extend(self.extractContent(child, level + 1))
        return extractedText

# if __name__ == "__main__":
#     XMLSourcePath = "/Users/Jerry/Desktop/DH proj-reading/XMLInterface/XMLTraversalTest/A16864.P4.xml"
#     XMLCustomizedTagsList = ['TITLESTMT', 'TITLE', 'AUTHOR', 'EXTENT', 'PUBLICATIONSTMT']
#     XMLParsingTool = XMLContentExtraction(XMLSourcePath, XMLCustomizedTagsList)
#     XMLParsingTool.traverseXML()