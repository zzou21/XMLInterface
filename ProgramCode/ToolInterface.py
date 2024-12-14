import os, xml.etree.ElementTree as ET, tkinter as tk
from tkinter import filedialog, messagebox
from XMLContentExtractionObject import XMLContentExtraction

class XMLToolInterface:
    def __init__(self, XMLSourceDirectory):
        self.XMLSourceDirectory = XMLSourceDirectory
        self.interfaceResultLabel = None

    def selectionInterface(self):
        rootInterface = tk.Tk()
        rootInterface.title("XML-TXT Interface")
        rootInterface.geometry("600x600")

        fileButton = tk.Button(rootInterface, text = "Process single XML file", command = self.processSingleFile, width = 25, height = 8)
        fileButton.pack(pady=10)
        self.interfaceResultLabel = tk.Label(rootInterface, text="No file or folder selected yet.", wraplength=500)
        self.interfaceResultLabel.pack(pady=20)
        rootInterface.mainloop()

    def processSingleFile(self):
        singleFilePath = filedialog.askopenfilename(title="Select a File")
        if singleFilePath:
            self.interfaceResultLabel.config(text=f"Selected File: {singleFilePath}")
            

    # def processSingleFolder(self):

    def operations(self):
        testTags = ['TITLESTMT', 'TITLE', 'AUTHOR', 'EXTENT', 'PUBLICATIONSTMT']
        XMLExtractionMachine = XMLContentExtraction(self.XMLSourceDirectory, testTags)
        XMLExtractionMachine.traverseXML()

if __name__ == "__main__":
    XMLSourceDirectory = "/Users/Jerry/Desktop/DH proj-reading/XMLInterface/XMLTraversalTest/A16864.P4.xml"
    XMLInterfaceToolMachine = XMLToolInterface(XMLSourceDirectory)
    XMLInterfaceToolMachine.selectionInterface()
