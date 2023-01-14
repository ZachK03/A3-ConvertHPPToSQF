import tkinter as tk
from tkinter import ttk
from tkinter import messagebox
from tkinter import END
from tkinter.constants import LEFT

formattedControls = []

def convertControlToSQF (control):
    if control == ";":
        return
    ctrlName = None
    ctrlType = None
    idc = None
    text = None
    xPos = None
    textColor = None
    backgroundColor = None
    activeColor = None
    toolTip = None
    code=codeEntry.get("1.0","end-1c")
    code = control
    print(control)

    indexStart=code.find("class ")
    if(indexStart != -1):
        indexEnd=code.find(": Rsc")
        ctrlName = code[indexStart+6:indexEnd]
        code=code[indexEnd:(len(code))-1]

    indexStart=code.find(": Rsc")
    if(indexStart != -1):
        indexEnd=code.find("{")
        ctrlType = code[indexStart+2:indexEnd-1]
        code=code[indexEnd+1:(len(code))-1]

    indexStart=code.find("idc")
    if(indexStart != -1):
        indexEnd=code.find(";")
        idc = code[indexStart+6:indexEnd]
        code=code[indexEnd+1:(len(code))-1]

    indexStart=code.find("text")
    if indexStart != -1:
        indexEnd=code.find(";")
        text = code[indexStart+7:indexEnd]
        code=code[indexEnd+1:(len(code))-1]

    indexStart=code.find("x = ")
    if indexStart != -1:
        indexEnd=code.find(";")
        xPos = code[indexStart+4:indexEnd]
        code=code[indexEnd+1:len(code)]

    indexStart=code.find("y = ")
    if indexStart != -1:
        indexEnd=code.find(";")
        yPos = code[indexStart+4:indexEnd]
        code=code[indexEnd+1:len(code)]

    indexStart=code.find("w = ")
    if indexStart != -1:
        indexEnd=code.find(";")
        xHeight = code[indexStart+4:indexEnd]
        code=code[indexEnd+1:len(code)]

    indexStart=code.find("h = ")
    if indexStart != -1:
        indexEnd=code.find("safezoneH")
        yHeight = code[indexStart+4:indexEnd+9]
        code=code[indexEnd+10:len(code)]


    indexStart=code.find("colorText[]")
    if indexStart != -1:
        indexEnd=code.find(";")
        textColor = code[indexStart+15:indexEnd-1]
        code=code[indexEnd+1:(len(code))-1]

    indexStart=code.find("colorBackground[]")
    if indexStart != -1:
        indexEnd=code.find(";")
        backgroundColor = code[indexStart+21:indexEnd-1]
        code=code[indexEnd+1:(len(code))-1]

    indexStart=code.find("colorActive[]")
    if indexStart != -1:
        indexEnd=code.find(";")
        activeColor = code[indexStart+17:indexEnd-1]
        code=code[indexEnd+1:(len(code))-1]

    indexStart=code.find("tooltip = ")
    if indexStart != -1:
        indexEnd=code.find(";")
        toolTip = code[indexStart+10:indexEnd]
        code=code[indexEnd+1:(len(code))-1]


    if ctrlName is not None:
        createControlName = "_{ctrlName}";
        createControlName = createControlName.format(ctrlName = ctrlName)
    else:
        createControlName = "ctrl"

    if ctrlType is not None:
        createControlText = " = _display ctrlCreate ['{ctrlType}',{idc}];\n"
        createControlText = createControlText.format(ctrlType = ctrlType, idc=idc)
    else:
        createControlText=""

    if text is not None:
        createCtrlText = "_{ctrlName} ctrlSetText {text};\n"
        createCtrlText = createCtrlText.format (ctrlName=ctrlName, text=text)
    else:
        createCtrlText=""

    if xPos is not None:
        setPosText = "_{ctrlName} ctrlSetPosition [{xPosition},{yPosition},{width},{height}];\n"
        setPosText = setPosText.format(ctrlName=ctrlName,xPosition=xPos,yPosition=yPos,width=xHeight,height=yHeight)
    else:
        setPosText=""

    if textColor is not None:
        createCtrlTextColor = "_{ctrlName} ctrlSetTextColor [{color}];\n"
        createCtrlTextColor = createCtrlTextColor.format(ctrlName=ctrlName,color=textColor)
    else:
        createCtrlTextColor=""

    if backgroundColor is not None:
        createCtrlBGColor = "_{ctrlName} ctrlSetBackgroundColor [{bgColor}];\n"
        createCtrlBGColor = createCtrlBGColor.format(ctrlName=ctrlName,bgColor=backgroundColor)
    else:
        createCtrlBGColor=""

    if activeColor is not None:
        createCtrlActiveColor = "_{ctrlName} ctrlSetActiveColor [{activeColor}];\n"
        createCtrlActiveColor = createCtrlActiveColor.format(ctrlName=ctrlName,activeColor=activeColor)
    else:
        createCtrlActiveColor=""

    if toolTip is not None:
        createCtrlTooltip = "_{ctrlName} ctrlSetTooltip {toolTip};\n"
        createCtrlTooltip = createCtrlTooltip.format(ctrlName=ctrlName,toolTip=toolTip)
    else:
        createCtrlTooltip=""

    populateListOfFormmatedControls(createControlName,createControlText,createCtrlText,setPosText,createCtrlTextColor,createCtrlBGColor,createCtrlActiveColor,createCtrlTooltip)


def convertCfgToControls ():
    codeFull=codeEntry.get("1.0","end-1c")
    controlsList = []
    formattedControls = []
    amountOfControls = codeFull.count("class")
    
    for x in range(0,amountOfControls):
        indexStart=codeFull.find("class")
        indexEnd=codeFull.find(";\n};")
        controlsList.append(codeFull[indexStart:indexEnd+4])
        codeFull=codeFull[indexEnd+1:len(codeFull)]

    for control in controlsList:
        convertControlToSQF(control)
    
    popUpOutput()

def populateListOfFormmatedControls(controlName, controlCreate, textCreate = "", posCreate = "", textColorCreate="",backgroundColorCreate="",activeColorCreate="",toolTipCreate=""):
    outputText = "{name}{create}{text}{pos}{color}{bgColor}{activeColor}{toolTip}{name} ctrlCommit 0;\n\n"
    outputText = outputText.format(name=controlName,create=controlCreate,text=textCreate,pos=posCreate,color=textColorCreate,bgColor=backgroundColorCreate,activeColor=activeColorCreate,toolTip=toolTipCreate)
    formattedControls.append(outputText)

def popUpOutput ():
    win = tk.Toplevel()
    win.title("Converted GUI Config")
    win.geometry("600x400")

    outputText = ""

    for str in formattedControls:
        outputText = outputText + str

    labelPop = tk.Label(win, text="Formatted SQF:")
    labelPop.pack()

    text = tk.Text(win, state='disabled', width=120)
    text.configure(state='normal')
    text.insert('end', outputText)
    text.configure(state='disabled')
    text.pack()
    

mainWindow = tk.Tk()
mainWindow.title("Convert GUI Config to SQF")
icon = tk.PhotoImage(file ="ZAMW.png")
mainWindow.iconphoto(True, icon)
mainWindow.configure(bg="#8c8c8c")

mainWindow.geometry("600x400")

codeLabel = tk.Label(mainWindow, text="Config Code:",bg="#8c8c8c")
codeLabel.pack()

codeEntry = tk.Text(mainWindow, width=50, height=20)
codeEntry.pack()

buttonConvert = tk.Button(mainWindow, text="Convert to SQF", command=convertCfgToControls, bg="#8c8c8c")
buttonConvert.pack()

mainWindow.mainloop()