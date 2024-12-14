import os, xml.etree.ElementTree as ET, tkinter as tk
from tkinter import filedialog, messagebox
from XMLContentExtractionObject import XMLContentExtraction

class XMLToolInterface:
    def __init__(self, XMLSourceDirectory):
        self.XMLSourceDirectory = XMLSourceDirectory
        self.interfaceResultLabel = None
        self.singleFileProcessCounter = 0
        self.folderFileProcessCounter = 0

    def selectionInterface(self):
        rootInterface = tk.Tk()
        rootInterface.title("XML-TXT Interface")
        rootInterface.geometry("600x600")

        fileButton = tk.Button(rootInterface, text = "Process single XML file", command = self.processSingleFile, width = 25, height = 8)
        fileButton.pack(pady = 10)

        directoryButton = tk.Button(rootInterface, text = "Process directory that contains XML files", command = self.processDirectory, width = 25, height = 8)
        directoryButton.pack(pady = 10)

        exitButton = tk.Button(rootInterface, text = "End Program.", command = rootInterface.destroy, width = 20, height = 6)
        exitButton.pack(pady = 10)

        self.interfaceResultLabel = tk.Label(rootInterface, text = "No file or folder selected yet.", wraplength = 500)
        self.interfaceResultLabel.pack(pady = 20)
        
        rootInterface.mainloop()

    def processSingleFile(self):
        singleFilePath = filedialog.askopenfilename(title = "Select an XML File", filetypes = [("XML Files", "*.xml")])
        self.interfaceResultLabel.update()

        if not singleFilePath:  # User canceled the dialog
            self.interfaceResultLabel.config(text = "File selection canceled. Please try again.")
            self.interfaceResultLabel.update()
            return

        self.interfaceResultLabel.config(text = "Please select a directory to store the output file.")
        self.interfaceResultLabel.update()
        self.interfaceResultLabel.after(1000)

        outputDirectory = filedialog.askdirectory(title = "Select an Output Directory")
        if not outputDirectory:
            self.interfaceResultLabel.config(text = "Output directory selection canceled. Please try again.")
            self.interfaceResultLabel.update()
            return
        
        self.singleFileProcessCounter += 1
        outputSingleFileName = f"output-{self.singleFileProcessCounter}.txt"

        outputFilePath = f"{outputDirectory}/{outputSingleFileName}"

        self.createSingleFileOutput(singleFilePath, outputFilePath)
        
    def processDirectory(self):
        pass

    def createSingleFileOutput(self, XMLPath, outputSingleFileName):
        if not XMLPath:
            self.interfaceResultLabel.config(text="No file selected. Please select an XML file.")
            self.interfaceResultLabel.update()  # Ensure the message updates immediately

        '''
        TODO: customize which tags to export
        '''
        testTags = ['TITLESTMT', 'TITLE', 'AUTHOR', 'EXTENT', 'PUBLICATIONSTMT']
        XMLExtractionMachine = XMLContentExtraction(XMLPath, testTags, outputSingleFileName)

        XMLExtractionMachine.traverseXML()
        self.interfaceResultLabel.config(text = "Single XML processing completed. Please select either 'Process single XML file' or 'Process folder' to perform another export or click 'End Program' to exit.")
        self.interfaceResultLabel.update()


if __name__ == "__main__":
    XMLSourceDirectory = "/Users/Jerry/Desktop/DH proj-reading/XMLInterface/XMLTraversalTest/A16864.P4.xml"
    XMLInterfaceToolMachine = XMLToolInterface(XMLSourceDirectory)
    XMLInterfaceToolMachine.selectionInterface()




    '''
    TODO: create try except so that if a folder exists, ask user to create a new folder.
    try:
        XMLExtractionMachine.traverseXML()
    except FileExistsError:
    '''