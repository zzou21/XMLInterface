import xml.etree.ElementTree as ET, os, re
'''
Class objects contained in this file: "XMLContentExtraction"
Purpose: an auxiliary function called on by the interface (in the file "ToolInterface.py") to generate the output TXT or folder of TXTs.
Parameters: file path to one XML file, a list of XML tags that we are NOT exporting, file path of the output TXT product.

NOTE: This class object does not handle a folder, only single XMLs, as the interface will break down a folder of XMLs and call on the functions inside "XMLContentExtraction" when iterating through each XML file.
'''
class XMLContentExtraction:
    def __init__ (self, XMLSourcePath, XMLCustomizedTagsList, outputName):
        self.XMLSourcePath = XMLSourcePath
        self.XMLCustomizedTagsList = set(XMLCustomizedTagsList)
        self.outputName = outputName

    def traverseAndOutputXML(self):
        tree = ET.parse(self.XMLSourcePath)
        root = tree.getroot()

        def extractContent(element):
            textContent = ""
            tag = element.tag.split("}")[-1]
            if tag not in self.XMLCustomizedTagsList:
                if element.text:
                    textContent += element.text.strip() + " "
                for child in element:
                    textContent += extractContent(child)
                if element.tail:
                    textContent += element.tail.strip() + " "
            return textContent

        outputText = extractContent(root)
        return outputText
    
    def writeToTXT(self):
        textToTXT = self.traverseAndOutputXML()
        with open(self.outputName, "w", encoding = "utf-8") as finalTXT:
            finalTXT.write(textToTXT)

# Commented code chunk below is for testing purposes only:

# if __name__ == "__main__":
#     XMLSourcePath = "/Users/Jerry/Desktop/DH proj-reading/XMLInterface/XMLTraversalTest/A16864.P4.xml"
#     XMLCustomizedTagsList = ["HEADER", "AVAILABILITY", "ENCODINGDESC", "EDITORIALDECL", "VID", "BIBNO", "IDNO", "SERIESSTMT", "NOTESSTMT", "NOTE", "PROJECTDESC", "LANGUSAGE", "LANGUAGE" ,"REVISIONDESC", "CHANGE" ,"RESPSTMT" ,"RESP", "IDG", "STC", "EXTENT", "TERM"]
#     outputFile = "/Users/Jerry/Desktop/DH proj-reading/XMLInterface/testOutput2.txt"
#     XMLParsingTool = XMLContentExtraction(XMLSourcePath, XMLCustomizedTagsList, outputFile)
#     XMLParsingTool.writeToTXT()
