import os, tkinter as tk
from tkinter import ttk
from tkinter import filedialog, messagebox
from XMLContentExtractionObject import XMLContentExtraction

class XMLToolInterface:
    def __init__(self, XMLSourceDirectory):
        self.XMLSourceDirectory = XMLSourceDirectory
        self.interfaceResultLabel = None
        self.displayButtonsForXMLTagSelection = None
        self.singleFileProcessCounter = 0
        self.folderFileProcessCounter = 0

    def selectionInterface(self):
        rootInterface = tk.Tk()
        rootInterface.title("XML-TXT Interface")
        rootInterface.geometry("600x600")

        mainFrame = tk.Frame(rootInterface)
        mainFrame.grid(row = 0, column = 0, sticky = "nsew")
        rootInterface.grid_rowconfigure(0, weight=1)
        rootInterface.grid_columnconfigure(0, weight=1)

        canvas = tk.Canvas(mainFrame)
        canvas.grid(row=0, column=0, sticky="nsew")
        scrollBar = ttk.Scrollbar(mainFrame, orient = "vertical", command = canvas.yview)
        scrollBar.grid(row=0, column=1, sticky="ns")
        canvas.configure(yscrollcommand = scrollBar.set)
        canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion = canvas.bbox("all")))

        subFrameForScroll = tk.Frame(canvas)
        canvas.create_window((0, 0), window = subFrameForScroll, anchor = "nw")
        mainFrame.grid_rowconfigure(0, weight=1)
        mainFrame.grid_columnconfigure(0, weight=1)

        #TODO: solve mouse wheel issue: only scrolls in the scroll bar column
        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(-int(e.delta / 60), "units"))
        

        titleLabel = tk.Label(subFrameForScroll, text = "Customized XML-to-TXT Export Interface", font = ("Times New Roman", 24, "bold"))
        titleLabel.grid(row=0, column=0, columnspan=3, pady=20)

        descriptionLabel = tk.Label(subFrameForScroll, text = "Instructions:\n\n1) Select one of the options by clicking on the coorresponding button below.\n\n2) After selecting a button, you will be prompted to select either a sinle XML file or a folder. This is the single XML or the folder of XML that you wish to convert to TXT.\n\n3) Then, the window will query you again to select a directory. This is the directory of which you wish to store the outputted single TXT file or folder of TXT files to.\n\n4) After each export, the window will not automatically close so that you can perform multiple exports in one runtime session. To end the session, click on the \"End Program\" button at the every end.", font = ("Times New Roman", 16), anchor = "w",justify = "left", wraplength = 580)
        descriptionLabel.grid(row=1, column=0, columnspan=3, pady=15)

        self.interfaceResultLabel = tk.Label(subFrameForScroll, text = "No file or folder selected yet.", font = ("Ariel", 13, "bold"), wraplength = 500)
        self.interfaceResultLabel.grid(row=2, column=0, columnspan=3, pady=20)

        fileButton = tk.Button(subFrameForScroll, text = "Process single XML file", command = self.processSingleFile, width = 15, height = 8)
        fileButton.grid(row = 3, column = 0, padx = 10, pady = 10)

        directoryButton = tk.Button(subFrameForScroll, text = "Process directory\nthat contains XML files", command = self.processDirectory, width = 15, height = 8)
        directoryButton.grid(row = 3, column = 1, padx = 10, pady = 10)

        exitButton = tk.Button(subFrameForScroll, text = "End Program", command = rootInterface.destroy, width = 15, height = 4)
        exitButton.grid(row = 3, column = 2, padx = 10, pady = 10)
        
        rootInterface.mainloop()

    def processSingleFile(self):
        singleFilePath = filedialog.askopenfilename(title = "Select an XML File", filetypes = [("XML Files", "*.xml")])
        self.interfaceResultLabel.update()

        if not singleFilePath:
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
        sourceXMLDirectoryPath = filedialog.askdirectory(title = "Select a directory of XML files to convert to TXT")
        self.interfaceResultLabel.update()
        if not sourceXMLDirectoryPath:
            self.interfaceResultLabel.config(text = "Directory selection canceled. Please try again.")
            self.interfaceResultLabel.update()
            return
        
        self.interfaceResultLabel.config(text = "Please select a directory to store the output folder.")
        self.interfaceResultLabel.update()
        self.interfaceResultLabel.after(1000)

        outputDirectory = filedialog.askdirectory(title = "Select an Output Directory")
        if not outputDirectory:
            self.interfaceResultLabel.config(text = "Output directory selection canceled. Please try again.")
            self.interfaceResultLabel.update()
            return
        
        outputTXTFolderName = "XMLTXTOutputFolder"
        newFolderPath = os.path.join(outputDirectory, outputTXTFolderName)
        repeatedFolderCounter = 1
        
        while os.path.exists(newFolderPath):
            newFolderPath = os.path.join(outputDirectory, f"{outputTXTFolderName}-{repeatedFolderCounter}")
            repeatedFolderCounter += 1
        os.makedirs(newFolderPath)

        self.createDirectoryOutput(sourceXMLDirectoryPath, newFolderPath)

    def createSingleFileOutput(self, XMLPath, outputSingleFileName):
        if not XMLPath:
            self.interfaceResultLabel.config(text="No file selected. Please select an XML file.")
            self.interfaceResultLabel.update()

        '''
        TODO: customize which tags to export
        '''
        testTags = ['TITLESTMT', 'TITLE', 'AUTHOR', 'EXTENT', 'PUBLICATIONSTMT']
        XMLExtractionMachine = XMLContentExtraction(XMLPath, testTags, outputSingleFileName)

        XMLExtractionMachine.traverseXML()
        self.interfaceResultLabel.config(text = "Single XML processing completed. Please select either 'Process single XML file' or 'Process folder' to perform another export or click 'End Program' to exit.")
        self.interfaceResultLabel.update()
    
    def createDirectoryOutput(self, sourceXMLDirectoryPath, newFolderPath):
        if not sourceXMLDirectoryPath:
            self.interfaceResultLabel.config(text="No file selected. Please select an XML file.")
            self.interfaceResultLabel.update()

        testTags = ['TITLESTMT', 'TITLE', 'AUTHOR', 'EXTENT', 'PUBLICATIONSTMT']
        for singleXMLFile in os.listdir(sourceXMLDirectoryPath):
            if singleXMLFile.endswith(".xml"):
                newFileName = "ToTXT" + os.path.splitext(singleXMLFile)[0] + ".txt"
                XMLExtractionMachine = XMLContentExtraction(os.path.join(sourceXMLDirectoryPath, singleXMLFile), testTags, os.path.join(newFolderPath, newFileName))
                XMLExtractionMachine.traverseXML()

        self.interfaceResultLabel.config(text = "Folder of XMl files processing completed. Please select either 'Process single XML file' or 'Process folder' to perform another export or click 'End Program' to exit.")
        self.interfaceResultLabel.update()

if __name__ == "__main__":
    XMLSourceDirectory = "/Users/Jerry/Desktop/DH proj-reading/XMLInterface/XMLTraversalTest/A16864.P4.xml"
    XMLInterfaceToolMachine = XMLToolInterface(XMLSourceDirectory)
    XMLInterfaceToolMachine.selectionInterface()