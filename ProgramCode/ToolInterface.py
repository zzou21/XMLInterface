import os, tkinter as tk, json
from tkinter import ttk
from tkinter import filedialog, messagebox
from XMLContentExtractionObject import XMLContentExtraction
from customizeXMLTags import XMLTagCustomization

class XMLToolInterface:
    def __init__(self, XMLSourceDirectory):
        self.XMLSourceDirectory = XMLSourceDirectory
        self.interfaceResultLabel = None
        self.displayButtonsForXMLTagSelection = None
        self.subFrameForScroll = None
        self.EEBOignoreTagsSet = None
        self.EEBOMode = False

    def selectionInterface(self):
        rootInterface = tk.Tk()
        rootInterface.title("XML-TXT Interface")
        rootInterface.geometry("1000x800")

        mainFrame = tk.Frame(rootInterface)
        mainFrame.grid(row = 0, column = 0, sticky = "nsew")
        rootInterface.grid_rowconfigure(0, weight = 1)
        rootInterface.grid_columnconfigure(0, weight = 1)

        canvas = tk.Canvas(mainFrame)
        canvas.grid(row = 0, column = 0, sticky = "nsew")
        scrollBar = ttk.Scrollbar(mainFrame, orient = "vertical", command = canvas.yview)
        scrollBar.grid(row = 0, column = 1, sticky = "ns")
        canvas.configure(yscrollcommand = scrollBar.set)
        canvas.bind("<Configure>", lambda e: canvas.configure(scrollregion = canvas.bbox("all")))

        self.subFrameForScroll = tk.Frame(canvas)
        canvas.create_window((0, 0), window = self.subFrameForScroll, anchor = "nw")
        mainFrame.grid_rowconfigure(0, weight = 1)
        mainFrame.grid_columnconfigure(0, weight = 1)

        canvas.bind_all("<MouseWheel>", lambda e: canvas.yview_scroll(-int(e.delta / 60), "units"))
        
        titleLabel = tk.Label(self.subFrameForScroll, text = "Customized XML-to-TXT Export Interface", font = ("Times New Roman", 20, "bold"), wraplength = 580)
        titleLabel.grid(row = 0, column = 0, columnspan = 3, pady = 20)

        descriptionLabel = tk.Label(self.subFrameForScroll, text = "Instructions:\n\n1) Select one of the options by clicking on the coorresponding button below.\n\n2) After selecting a button, you will be prompted to select either a sinle XML file or a folder. This is the single XML or the folder of XML that you wish to convert to TXT.\n\n3) Then, the window will query you again to select a directory. This is the directory of which you wish to store the outputted single TXT file or folder of TXT files to.\n\n4) After each export, the window will not automatically close so that you can perform multiple exports in one runtime session. To end the session, click on the \"End Program\" button at the every end.\n\nScroll down or expand the window if you cannot see the buttons.", font = ("Times New Roman", 14), anchor = "w",justify = "left", wraplength = 580)
        descriptionLabel.grid(row = 1, column = 0, columnspan = 3, pady = 15)

        statusIndicatorLabel = tk.Label(self.subFrameForScroll, text = "Program status: \n")
        statusIndicatorLabel.grid(row = 2, column = 0, padx = 5, pady = 1)

        self.interfaceResultLabel = tk.Label(self.subFrameForScroll, text = "No file or folder selected yet.", font = ("Ariel", 13), wraplength = 500)
        self.interfaceResultLabel.grid(row = 3, column = 0, columnspan = 3, pady = 20)

        fileButton = tk.Button(self.subFrameForScroll, text = "Process single XML file", command = self.processSingleFile, width = 20, height = 3)
        fileButton.grid(row = 4, column = 0, padx = 10, pady = 10)

        directoryButton = tk.Button(self.subFrameForScroll, text = "Process directory\nthat contains XML files", command = self.processDirectory, width = 20, height = 3)
        directoryButton.grid(row = 4, column = 1, padx = 10, pady = 10)

        exitButton = tk.Button(self.subFrameForScroll, text = "End Program", command = rootInterface.destroy, width = 15, height = 3)
        exitButton.grid(row = 4, column = 2, padx = 10, pady = 10)
        
        rootInterface.mainloop()

    def processSingleFile(self):
        singleFilePath = filedialog.askopenfilename(title = "Select an XML File", filetypes = [("XML Files", "*.xml")])
        self.interfaceResultLabel.update()

        if not singleFilePath or not singleFilePath.endswith(".xml"):
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
        
        singleFileCounterSuffix = 1
        outputSingleFileName = f"output-{singleFileCounterSuffix}.txt"

        outputFilePath = f"{outputDirectory}/{outputSingleFileName}"

        while os.path.exists(outputFilePath):
            outputSingleFileName = f"output-{singleFileCounterSuffix}.txt"
            outputFilePath = f"{outputDirectory}/{outputSingleFileName}"
            singleFileCounterSuffix += 1
        
        XMLTagListMachine = XMLTagCustomization()
        uniqueXMLList = XMLTagListMachine.traverseDisplaySingleFileInterface(singleFilePath)
        windowWidth = 600
        buttonsPerRow = windowWidth // 100

        self.interfaceResultLabel.config(text = "Select all XML tags that you want to export: ")
        self.interfaceResultLabel.update()
        
        EEBOSpecialButton = tk.Button(self.subFrameForScroll, text = "EEBO-TCP Shortcut", command = lambda: EEBOSpecialShortCut(), width = 18, height = 2)
        EEBOSpecialButton.grid(row = 5, column = 2, padx = 7, pady = 7)

        allSelectedTagsToInclude = set()
        allTagButtonsTrackerList = []
        for count, oneTag in enumerate(uniqueXMLList):
            row = count // buttonsPerRow
            column = count % buttonsPerRow
            tagButton = tk.Button(self.subFrameForScroll, text = oneTag, command = lambda tag=oneTag: addTagToSet(tag), width = 9, height = 2)
            tagButton.grid(row = row + 6, column = column, padx = 5, pady = 5)
            allTagButtonsTrackerList.append(tagButton)
        endTagSelectionButton = tk.Button(self.subFrameForScroll, text = "Selected all\nXML Tags", command = lambda: createXMLExtractionMachine(singleFilePath, allSelectedTagsToInclude, outputFilePath), width = 20, height = 3)
        endTagSelectionButton.grid(row = 4, column = 4, padx = 10, pady = 10)
        
        def EEBOSpecialShortCut():
            EEBOTagsJson = open("ProgramCode/EEBOTagsToExclude.json")
            EEBOTagsToIgnore = json.load(EEBOTagsJson)
            self.EEBOignoreTagsSet = set(EEBOTagsToIgnore["EEBOXMLTagsToExclude"])
            self.interfaceResultLabel.config(text = f"XML tags to EXCLUDE in EEBO: {self.EEBOignoreTagsSet}. \n\nNow click \"Selected all XML Tags\" button to proceed.")
            self.interfaceResultLabel.update()
            self.EEBOMode = True

        def addTagToSet(tag):
            allSelectedTagsToInclude.add(tag)
            allSelectedTagsToIncludeAsSortedList = sorted(list(allSelectedTagsToInclude))
            self.interfaceResultLabel.config(text = f"Selected XML tags: {allSelectedTagsToIncludeAsSortedList}")
            self.interfaceResultLabel.update()

        def createXMLExtractionMachine(singleFilePath, allSelectedTagsToInclude, outputFilePath):
            print("reached here")
            if not allSelectedTagsToInclude and not self.EEBOMode:
                self.interfaceResultLabel.config(text = "No tags selected. Please select at least one tag.")
                self.interfaceResultLabel.update()
                return
            
            for button in allTagButtonsTrackerList:
                button.destroy()
            allTagButtonsTrackerList.clear()

            if self.EEBOMode == True:
                XMLTagListMachineEEBO = XMLTagCustomization()
                allTagsInFile = XMLTagListMachineEEBO.traverseDisplaySingleFileInterface(singleFilePath)
                updatedEEBOTagsThatHaveUsefulContent = [tag for tag in allTagsInFile if tag not in self.EEBOignoreTagsSet]
                print(f"tags being used: {updatedEEBOTagsThatHaveUsefulContent}")
                XMLExtractionMachine = XMLContentExtraction(singleFilePath, updatedEEBOTagsThatHaveUsefulContent, outputFilePath)
                self.createSingleFileOutput(XMLExtractionMachine)
            else:
                XMLExtractionMachine = XMLContentExtraction(singleFilePath, allSelectedTagsToInclude, outputFilePath)
                self.createSingleFileOutput(XMLExtractionMachine)

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

    def createSingleFileOutput(self, XMLExtractionMachine):
        XMLExtractionMachine.traverseAndOutputXML()
        self.interfaceResultLabel.config(text = f"Single XML processing completed.\nStored in: {XMLExtractionMachine.outputName}\n\nPlease select either 'Process single XML file' or 'Process folder' to perform another export or click 'End Program' to exit.")
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
                XMLExtractionMachine.traverseAndOutputXML()

        self.interfaceResultLabel.config(text = "Folder of XMl files processing completed. Please select either 'Process single XML file' or 'Process folder' to perform another export or click 'End Program' to exit.")
        self.interfaceResultLabel.update()


    #TODO update directory output so that we calll teh XML Content export object in the proceesDirectory function
if __name__ == "__main__":
    XMLSourceDirectory = "/Users/Jerry/Desktop/DH proj-reading/XMLInterface/XMLTraversalTest/A16864.P4.xml"
    XMLInterfaceToolMachine = XMLToolInterface(XMLSourceDirectory)
    XMLInterfaceToolMachine.selectionInterface()