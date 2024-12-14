import os, xml.etree.ElementTree as ET, tkinter as tk
from tkinter import filedialog
from XMLContentExtractionObject import XMLContentExtraction

class XMLToolInterface:
    def __init__(self, XMLSourceDirectory):
        self.XMLSourceDirectory = XMLSourceDirectory

    def operations(self):
        testTags = ['TITLESTMT', 'TITLE', 'AUTHOR', 'EXTENT', 'PUBLICATIONSTMT']
        XMLExtractionMachine = XMLContentExtraction(self.XMLSourceDirectory, testTags)
        XMLExtractionMachine.traverseXML()

if __name__ == "__main__":
    XMLSourceDirectory = "/Users/Jerry/Desktop/DH proj-reading/XMLInterface/XMLTraversalTest/A16864.P4.xml"
    XMLInterfaceToolMachine = XMLToolInterface(XMLSourceDirectory)
    XMLInterfaceToolMachine.operations()
