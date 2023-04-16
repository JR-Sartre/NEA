import tkinter as tk


def main():
    #start of the tkinter loop
    root = tk.Tk()


    # getting screen size in pixels  
    global screenWidth,screenHeight
    screenWidth = root.winfo_screenwidth()
    screenHeight = root.winfo_screenheight()
    
    # root window dimensions and size
    root.title("Dijkstra Project")
    root.geometry(f"{screenWidth}x{screenHeight}")
    root.maxsize = (screenWidth,screenHeight)
    root.configure(bg="white")

    #calling which page is to be called first
    customGraphPage(root,screenWidth,screenHeight)
    
    print(f"screen width: {screenWidth}, screen height: {screenHeight}")

    root.mainloop()

# procedure used to delete the current frame - freeing up resources
def deleteFrames(root):
    print("frame deleted.")
    for frames in root.winfo_children():
        print (frames)
        frames.destroy()

# all of the full size frame's size and placement on the window is constant, so this function makes things easier for myself
def makeFrame(root,colour,screenWidth,screenHeight):
    frame = tk.Frame(
        root,
        width = screenWidth,height = screenHeight
    )
    frame.place(x=0,y=0)
    frame.configure(bg=colour)
    return frame



    

def customGraphPage(root,screenWidth,screenHeight):
    global numberOfNodes,nodeDragData,nodeData
    numberOfNodes = 0

    customGraphFrame = makeFrame(root,"grey",screenWidth,screenHeight)
    
    """
    Creating 2D dictionary to store the node's center coords .
    they all have the first key as n(i) as integers correspond to the auto incremented ID of the tkinter objects. 
    This means each an edge created before the 16 nodes could have the ID of 1-16 thus be referenced in the dictionary
    """
    nodeData = {}
    for i in range(16):
        nodeData[f"n{i}"] = {"number": i, "empty": True, "x": 0, "y": 0}

    """
    The list below is to store the edges weights between the nodes
    Every time a node is added another 
    """

    nodeEdges = []
    
    
    #dictionary used to temporarily store and change each node being dragged
    nodeDragData = {"x": 0, "y": 0, "item": None}

    
    
    #function used to display all the widgets of the customGraph frame
    customGraphFrameWidgets(customGraphFrame)


#creates the edge using the inputs from the entry widgets 
def createEdge(canvas,edgeFromEntry,edgeToEntry): 
    edgeInputCheck = True
    fromNode,toNode = getEdgeEntry(edgeFromEntry,edgeToEntry) # gets user inputs from the entry widgets
    
    # here should be some validation for the entry box inputs
    if edgeInputCheck == False: 
        print("can only input numbers")
    
    
    x0 = nodeData[fromNode]["x"]
    y0 = nodeData[fromNode]["y"]
    x1 = nodeData[toNode]["x"]
    y1 = nodeData[toNode]["y"]
    print(x0,y0,x1,y1)

    edgeLine = canvas.create_line(x0,y0,x1,y1,fill = "green",width = "2", tags = ("edges"))
    midpointX = (x0+x1)//2 
    midpointY = (y0+y1)//2 
    edgeWeight = canvas.create_text(
        midpointX,midpointY,fill = "black",font =("DejaVu Sans",13),text="weight",tags = (f"{fromNode}to{toNode}","weights"))
    canvas.tag_raise("node") # makes the nodes raise above the edges on the canvas
    canvas.tag_raise("nodeNumber") # so the number is on top of the node


# how to call the user inputs from the edge entry boxes and deleting what was entered in the entry boxes
def getEdgeEntry(entryFrom, entryTo,weightEntry): 
    
    fromNode = entryFrom.get()
    print(f"From: {fromNode}")
    entryFrom.delete(0,len(fromNode))

    toNode = entryTo.get()
    print(f"To: {toNode}")
    entryTo.delete(0,len(toNode))
    
    weight = weightEntry.get()
    weightEntry.delete(0,len(weight))
    print(f"weight = {weight}")

    
    return fromNode,toNode,weight


    
#shows nodeData's nested dictionaries line by line
def showDict():
    print("")
    for i in range(16 ):
        print(nodeData[f"n{str(i)}"])
    print("")


    


"""find_closest(x, y, halo=None, start=None)
Returns a singleton tuple containing the object ID of the object closest to point (x, y). If there are no qualifying objects, returns an empty tuple."""



def createCircle(canvas,xCoord,yCoord,radius, **kwargs):
    global numberOfNodes
    x0 = xCoord - radius 
    y0 = yCoord - radius 
    x1 = xCoord + radius 
    y1 = xCoord + radius 
    return canvas.create_oval(x0, y0 ,x1 ,y1, tags = (f"n{numberOfNodes}","node"), **kwargs)


def createNode(canvas): 
    global numberOfNodes,radius
    radius = 30
    if numberOfNodes < 16: 
        

        nodeData[f"n{numberOfNodes}"]["empty"] = False
        nodeData[f"n{numberOfNodes}"]["x"] = 300+20*numberOfNodes
        nodeData[f"n{numberOfNodes}"]["y"] = 300+20*numberOfNodes
        #creating a node with tags "{the number of the node}" and "node" , with each creation being offset by a bit 
        node = createCircle(
            canvas,300+20*numberOfNodes,300+20*numberOfNodes,radius,
            fill = "white",outline = "#DDD", width = 4
        )
        # the label inside the node, which will appear with its corresponding node
        nodeLetter = canvas.create_text(
            300+20*numberOfNodes,300+20*numberOfNodes,
            text = str(nodeData[f"n{numberOfNodes}"]["number"]),
            fill = "black", tags = (f"l{numberOfNodes}","nodeNumber")
            )

        
        # binds the dragging commands to items in canvas with tag "node"
        canvas.tag_bind("node", "<ButtonPress-1>",lambda e:nodeDragStart(e,canvas))
        canvas.tag_bind("node", "<B1-Motion>", lambda e:nodeDrag(e,canvas))
        canvas.tag_bind("node", "<ButtonRelease-1>",lambda e:nodeDragEnd(e,canvas))

        numberOfNodes += 1
    
    else: 
        print("TOO MANY NODES")

def nodeDragStart(event,canvas):

    """Begining drag of an object"""
    # record the item clicked(uses its object id to get its tag) and mouse location

    objectID = canvas.find_closest(event.x, event.y, start = "node")[0] 
    nodeName = canvas.gettags(objectID)[0]
    print(f"tags of node selected: {canvas.gettags(objectID)} , {type(nodeName)}")


    nodeDragData["item"] = nodeName
    nodeDragData["x"] = event.x
    nodeDragData["y"] = event.y
    



def nodeDrag(event,canvas):
    """Handle dragging of an object"""
    number = nodeDragData["item"]
    number = number[1:]

    # compute how much the mouse has moved
    deltaX = event.x - nodeDragData["x"]
    deltaY = event.y - nodeDragData["y"]
    # moves the object by the correct distance 
    canvas.move(nodeDragData["item"], deltaX, deltaY)
    canvas.move(f"l{number}",deltaX,deltaY)

    #canvas.coords(nodeDragData["item"],event.x,event.y)
    # records the new position of mouse
    nodeDragData["x"] = event.x
    nodeDragData["y"] = event.y

    

    

    # changes node's colour
    canvas.itemconfigure(nodeDragData["item"],fill = "red")

    # records the position on the canvas of the node (x and y coordinates of centre)
    nodeName = nodeDragData["item"]

    x0 = int(canvas.coords(nodeDragData["item"])[0])
    y0 = int(canvas.coords(nodeDragData["item"])[1])
    x1 = int(canvas.coords(nodeDragData["item"])[2])
    y1 = int(canvas.coords(nodeDragData["item"])[3])
    
    nodeData[nodeDragData["item"]]["x"] = x0 + radius 
    nodeData[nodeDragData["item"]]["y"] = y0 + radius
    

def nodeDragEnd(event,canvas):
    global rawNodeCoords,edgeCreationState
    """End drag of an object"""
    # reset the drag information and stores the coordinates of their centres.
    #canvas.itemconfigure(nodeDragData["item"],fill = "")
    
    
    canvas.itemconfigure(nodeDragData["item"],fill = "white")

def resetCanvas(customGraphFrame,canvas):
    pass


def runDijkstra(numberOfNodes):
    edgeData =[[0 for i in range(numberOfNodes)] for j in range(numberOfNodes)]

#procedure to place all the buttons on the screen
def customGraphFrameWidgets(customGraphFrame):

    customGraphCanvas = tk.Canvas (customGraphFrame,
    width = screenWidth*0.8, height = screenHeight *0.8 , bg = "#FFE0B2")
    customGraphCanvas.place(relx=0.005,rely=0.01)

    mousePosLabel = tk.Label (
        customGraphFrame,
        width = 25,height = 3
    )
    mousePosLabel.place(relx = 0.33, rely=0.83)

    #tracks and displays the position of the mouse on the screen.
    customGraphCanvas.bind("<Motion>",lambda e: mousePosLabel.configure(text = f"Coordinates|x:{e.x},y:{e.y}| "))


    createNodeButton = tk.Button(
        customGraphFrame,text="Create Node",
        width = 50, height = 3,command = lambda: createNode(customGraphCanvas) 
    )
    createNodeButton.place(relx=0.005,rely=0.83)


    showCoordDictButton = tk.Button(
        customGraphFrame, text = "Print node data",
        width = 50 , height = 3, command = showDict
    )
    showCoordDictButton.place(relx=0.49,rely=0.83)

    textFont_13D = ("DejaVu Sans",13)

    edgeEntryFrame = tk.Frame(
        customGraphFrame,
        width=350,height = 700 
    )
    edgeEntryFrame.place(relx=0.81,rely=0.1)


    edgeFromLabel = tk.Label(
        edgeEntryFrame,
        text = "From",
        height = 5,
        width =10
    )
    edgeFromLabel.grid(row=1,column=0)
    edgeFromLabel.configure(font = textFont_13D)

    edgeFromEntry = tk.Entry(
        edgeEntryFrame,
        width = 3
    )
    edgeFromEntry.grid(row=1,column=1)
    edgeFromEntry.configure(font = textFont_13D)

    edgeToLabel = tk.Label(
        edgeEntryFrame,
        text = "To",
        height = 5,
        width =10
    )
    edgeToLabel.grid(row = 2, column =0)
    edgeToLabel.configure(font = textFont_13D)

    edgeToEntry = tk.Entry(
        edgeEntryFrame,
        width = 3
    )  
    edgeToEntry.grid(row=2,column=1)
    edgeToEntry.configure(font = textFont_13D)
    
    weightLabel = tk.Label(
        edgeEntryFrame,
        text = "Weight",
        height = 5,
        width =10
    )
    weightLabel.grid(row = 3, column =0)
    weightLabel.configure(font = textFont_13D)
    
    weightEntry = tk.Entry(
        edgeEntryFrame,
        width=3
    )
    weightEntry.grid(row=3,column=1)
    weightEntry.configure(font = textFont_13D)

    edgeEntryButton = tk.Button(
        edgeEntryFrame, text = "Create edge",
        width = 20, command = lambda: createEdge(customGraphCanvas,edgeFromEntry,edgeToEntry,weightEntry) ,font = textFont_13D)
    edgeEntryButton.grid(row=4,columnspan =2 )



def entryCharacterLimit(entry):
    if len(entry.get()) > 0:
        entry.delete()



main()

