# XML Customized Extraction Interface Tool

Author:
Jerry Zou

**Functionality**: This tool is designed to help users quickly and efficiently extract information from an XML by selecting the specific XML tags to extract content from.

**Files and Instructions**:
All code and data are stored in the folder "ProgramCode". When using this tool, make sure to download or clone the folder in its entirety.
Inside "ProgramCode" folder, there are four files: 
- *customizeXMLTags.py*: auxiliary class object to extract all XML tags from an XML file so that the user can select which ones they'd like to extract content from and which ones to ignore.
- *EEBOTagsToExclude.json*: designed as a shortcut for EEBO-TCP usages; this JSON file contains XML tags found in EEBO-TCP XML files that contain metadata and not the actual content of early modern English texts. The XML tags in this JSON file are intended to be skipped during the XML-to-TXT conversion process.
- *ToolInterface.py*: main execution file
- *XMLContentExtractionObject.py*: auxiliary class object to recursively traverse an XML file to extract content from the XML tags designated by the user and turn the content into TXT files.

**Steps**:
1) When using the tool, only execute *ToolInterface.py*, as this file calls on the other three auxiliary files.

2) After executing *ToolInterface.py*, a GUI will show up with more detailed instructions.

3) The user will be given a choice between processing one single XML file into a TXT file or turning a folder of XML files into a folder of TXT files. Each is represented by one button. A third button on the GUI is the "End Program" button.

4) After selecting the needed functionality (process single XML or folder of XMLs), the user will be prompted twice to select file paths. The first prompt will ask the user to select which XML file (or folder) they wish to convert to TXT. The second prompt will ask the user in which directory on their local device they wish to store the converted TXT file (or folder).

5) After the user has made a choice on both prompts, the GUI will display all XML tags in the XML file they have chosen. The user can simply click on the buttons that represent the XML tags that they wish to export before clicking the "Selected all" button to begin the conversion process. There is a shortcut for "EEBO-TCP shortcut", as this tool was designed with the Early English Books Online - Text Creation Partnership in mind.
    - The EEBO-TCP shortcut automatically removes the metadata that the University of Michigan and TCP put into the files when converting early modern English prints and texts into XML formats. After the user clicks on the EEBO-TCP shortcut button, the GUI will display which XML tags will be automatically skipped during the conversion process.

6) After clicking "Selected all" XML tags, the user can go to the output directory that they designated in Step 4 to find their files.

7) The tool will not end after one conversion. If the user wishes to convert more files, they can continue doing so. The tool will stop executing if the user clicks on the "End Program" button, closes the GUI window, or pauses the *ToolInterface.py* file in its runtime.

### Tasks going forward
The current version of the tool is a functional prototype, but it definitely could have a lot more functionalities. Some functionalities that have been planned to include are:
- Create a button that selects all XMLs
- Allow the user to delete some of their selected XMLs before clicking the "Selected all" button, in case they've made a mistake.
- Make the GUI window more malleable so it will expand or contract depending on how many XML buttons are on screen.



This project is tested on the XML data from Early English Books Online - Text Creation Partnership at the University of Michigan. https://textcreationpartnership.org/tcp-texts/eebo-tcp-early-english-books-online/
