import xml.etree.ElementTree as ET, os, re

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
        textToTXT = textToTXT.replace("To the extent possible under law, the Text Creation Partnership has waived all copyright and related or neighboring rights to this keyboarded and encoded edition of the work described above, according to the terms of the CC0 1.0 Public Domain Dedication (http://creativecommons.org/publicdomain/zero/1.0/). This waiver does not extend to any page images or other supplementary files associated with this work, which may be protected by copyright or other license restrictions. Please go to http://www.textcreationpartnership.org/ for more information.", "")
        textToTXT = textToTXT.replace("Ann Arbor, MI ; Oxford (UK) : Text Creation Partnership,", "")
        textToTXT = textToTXT.replace("Early English books online. ", "")

        pattern = r"\b20\d{2}-\d{2} \(EEBO-TCP Phase (1|2)\)"
        textToTXT = re.sub(pattern, "", textToTXT)

        with open(self.outputName, "w", encoding = "utf-8") as finalTXT:
            finalTXT.write(textToTXT)

if __name__ == "__main__":
    XMLSourcePath = "/Users/Jerry/Desktop/DH proj-reading/XMLInterface/XMLTraversalTest/A16864.P4.xml"
    XMLCustomizedTagsList = ["HEADER", "AVAILABILITY", "ENCODINGDESC", "EDITORIALDECL", "VID", "BIBNO", "IDNO", "SERIESSTMT", "NOTESSTMT", "NOTE", "PROJECTDESC", "LANGUSAGE", "LANGUAGE" ,"REVISIONDESC", "CHANGE" ,"RESPSTMT" ,"RESP", "IDG", "STC", "EXTENT", "TERM"]
    outputFile = "/Users/Jerry/Desktop/DH proj-reading/XMLInterface/testOutput2.txt"
    XMLParsingTool = XMLContentExtraction(XMLSourcePath, XMLCustomizedTagsList, outputFile)
    XMLParsingTool.writeToTXT()