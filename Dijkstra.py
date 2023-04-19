"""
Key information


Hashtags are used for labelling and quick explanations
Triple quotations are used for more in depth explanations - maybe info for documenting  


Subroutine naming : 
    'pages' contain corresponding frames.
    'make' return something.
    'create' do not.
    'show' print out what they refer to.

Important tags: 'node' , 'edge', 'nodeLetter'

In customGraphPage - 



"""

#importing required libraries
import tkinter as tk
from PIL import Image, ImageTk

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

    # calling which page is to be called first
    customGraphPage(root)
    
    # removable in end project
    print(f"screen width: {screenWidth}, screen height: {screenHeight}")

    root.mainloop()

# procedure used to delete the current frame - freeing up resources
def deleteFrames(root):
    print("frame deleted.")
    for frames in root.winfo_children():
        print (frames)
        frames.destroy()

"""
Standardised tkinter widgets: More concise
makeFullFrame - frame on top of root that covers the whole screen.

"""

def makeFullFrame(root,colour):
    global screenHeight,screenWidth
    frame = tk.Frame(
        root,
        width = screenWidth,height = screenHeight
    )
    frame.place(x=0,y=0)
    frame.configure(bg=colour)
    return frame



    

def customGraphPage(root):
    global numberOfNodes,numberOfEdges,nodeDragData,nodeData,nodeEdges
    numberOfNodes,numberOfEdges = 0,0

    customGraphFrame = makeFullFrame(root,"grey")
    
    """
    Creating 2D dictionary to store the node's center coords .
    They all have the first key as 'n(i)' as integers correspond to the auto incremented ID of the tkinter objects. 
    This means each an edge created before the 16 nodes could have the ID of 1-16 thus be referenced when trying to use tags
    """
    nodeData = {}
    #for i in range(16):
    #    nodeData[f"n{i}"] = {"label": i, "x": 0, "y": 0}

    """
    Storing the edges weights between the nodes using 2D list.
    Every time a node is added, another row is appended.
    """

    nodeEdges = []
    
    
    # dictionary used to temporarily store and change each node being dragged
    nodeDragData = {"x": 0, "y": 0, "item": None}
    
    # function used to display all the widgets of the customGraph frame
    customGraphFrameWidgets(customGraphFrame)




 
def makeCircle(canvas,xCoord,yCoord,radius, **kwargs):
    x0 = xCoord - radius 
    y0 = yCoord - radius 
    x1 = xCoord + radius 
    y1 = yCoord + radius 
    return canvas.create_oval(x0, y0 ,x1 ,y1, tags = (f"n{numberOfNodes}","node"), **kwargs)


def createNode(canvas): 
    global numberOfNodes,radius
    radius = 30
    
    # max 16 nodes allowed currently - 0 to 15
    if numberOfNodes < 16: 
        
        startCentreX = 300+20*numberOfNodes
        startCentreY = 900+20*numberOfNodes

        #creating a node with tags "{the number of the node}" and "node" , with each creation being offset by a bit 
        makeCircle(
            canvas,startCentreX,startCentreY,radius,
            fill = "#CBC3E3",outline = "#301934", width = radius//15
        )
        
        # adds a new row to nodeEdges
        row = []
        for i in range(16):
            row.append(100)            
        
        nodeEdges.append(row)

        # adds a new node to the nodeData dictionary
        
        nodeData[f"n{numberOfNodes}"] = {"label": numberOfNodes, "x": startCentreX, "y": startCentreY,"from":[],"to":[]}
        
        
        # the label inside the node, which will appear with its corresponding node and move alongside it.
        canvas.create_text(
            startCentreX,startCentreY,
            text = str(nodeData[f"n{numberOfNodes}"]["label"]),
            fill = "black", tags = (f"l{numberOfNodes}","nodeLabel")
        )
        
        # will store the intial position of each node which is hardcoded (for now)
        # label position is irrelevant as we move using its tag alongside the node
        nodeData[f"n{numberOfNodes}"]["x"]= startCentreY
        nodeData[f"n{numberOfNodes}"]["y"]= startCentreY

        
        # binds the dragging commands to items in canvas with tag "node"
        canvas.tag_bind("node", "<ButtonPress-1>",lambda e:nodeDragStart(e,canvas))
        canvas.tag_bind("node", "<B1-Motion>", lambda e:nodeDrag(e,canvas))
        canvas.tag_bind("node", "<ButtonRelease-1>",lambda e:nodeDragEnd(e,canvas))

        numberOfNodes += 1
    
    else: 
        print("Too many nodes - max 16")


# creates the edge using the inputs from the entry widgets 
def createEdge(canvas,edgeFromEntry,edgeToEntry,weightEntry): 
    global numberOfEdges
    
     
    # gets user inputs from the entry widgets
    fromNode,toNode,weight = getEdgeEntry(edgeFromEntry,edgeToEntry,weightEntry) 
    
    # when adding their edges, i can put the order of which they are connected in asc order in their tags
    if fromNode > toNode:
        firstNode = int(toNode) 
        secondNode = int(fromNode)
    else:
        firstNode = int(fromNode)
        secondNode = int(toNode)

    #getting the centers of the two nodes to be connected
    x0 = nodeData[f"n{firstNode}"]["x"]
    y0 = nodeData[f"n{firstNode}"]["y"]
    x1 = nodeData[f"n{secondNode}"]["x"]
    y1 = nodeData[f"n{secondNode}"]["y"]
    print(x0,y0,x1,y1)
    
    #adding the weight into the 2D list
    weight = int(weight)
    nodeEdges[firstNode][secondNode] = weight
    nodeEdges[secondNode][firstNode] = weight
    
    

    #creating the edge between nodes on the canvas
    canvas.create_line(x0,y0,x1,y1,fill = "green",width = "2", tags = ("edges",f"e{numberOfEdges}"))
    
    #adding the tag unto the appropriate edges depending if its to or from
    nodeData[f"n{firstNode}"]["from"].append(f"{numberOfEdges}a") 
    nodeData[f"n{secondNode}"]["to"].append(f"{numberOfEdges}b")

    #getting midtpoints of the edge to create a weight label on it
    midpointX = (x0+x1)//2 
    midpointY = (y0+y1)//2 
    canvas.create_text(
        midpointX,midpointY,fill = "black",font =("DejaVu Sans",13),text=f"{weight}",tags = ("edgeWeight")
    )
    
    # changes order of which objects are on top 
    canvas.tag_raise("node") 
    canvas.tag_raise("nodeLabel") 
    canvas.tag_raise("edgeWeight")

    #increments number of edges by 1 
    numberOfEdges += 1

#NODE DRAG
#beginning of node drag - mouse click on node
def nodeDragStart(event,canvas):

    
    # record the item clicked(uses its object id to get its tag) and mouse location
    objectID = canvas.find_closest(event.x, event.y, start = "node")[0] 
    nodeName = canvas.gettags(objectID)[0]
    print(f"Tags of node selected: {canvas.gettags(objectID)} , {type(nodeName)}")


    nodeDragData["item"] = nodeName
    nodeDragData["x"] = event.x
    nodeDragData["y"] = event.y
    



def nodeDrag(event,canvas):
    #gets the first tag of the item and also gets only the number of it
    nodeTag = nodeDragData["item"]
    nodeNumber = nodeTag[1:]

    # compute how much the mouse has moved
    deltaX = event.x - nodeDragData["x"]
    deltaY = event.y - nodeDragData["y"]
    # moves the object and the label by the correct distance 
    canvas.move(nodeDragData["item"], deltaX, deltaY)
    
    #these for loops to try move the correct edge
    #for i in range(len(nodeData[nodeTag]["to"])):
    #    canvas.move(f"{nodeNumber}a",deltaX,deltaY)

    
    #for i in range(len(nodeData[nodeTag]["to"])):
    #    canvas.move(f"{nodeNumber}b",0,0,deltaX,deltaY)
    
    #moves the node label with the node
    canvas.move(f"l{nodeNumber}",deltaX,deltaY)

    #canvas.coords(nodeDragData["item"],event.x,event.y)
    # records the new position of mouse
    nodeDragData["x"] = event.x
    nodeDragData["y"] = event.y

    

    

    # changes node's colour as it is being dragged
    canvas.itemconfigure(nodeDragData["item"],fill = "#9F2B68")

    # records the position on the canvas of the node (x and y coordinates of centre)
    nodeName = nodeDragData["item"]

    x0 = int(canvas.coords(nodeDragData["item"])[0])
    y0 = int(canvas.coords(nodeDragData["item"])[1])
    
    nodeData[nodeDragData["item"]]["x"] = x0 + radius 
    nodeData[nodeDragData["item"]]["y"] = y0 + radius
    

def nodeDragEnd(event,canvas):
    global rawNodeCoords,edgeCreationState
    """End drag of an object"""
    # reset the drag information and stores the coordinates of their centres.
    #canvas.itemconfigure(nodeDragData["item"],fill = "")
    
    
    canvas.itemconfigure(nodeDragData["item"],fill = "#CBC3E3")


# how to call the user inputs from the edge entry boxes and deleting what was entered in the entry boxes
def getEdgeEntry(entryFrom,entryTo,weightEntry): 
    
    fromNode = entryFrom.get()
    print(f"From: {fromNode}")
    entryFrom.delete(0,len(fromNode))

    toNode = entryTo.get()
    print(f"To: {toNode}")
    entryTo.delete(0,len(toNode))
    
    weight = weightEntry.get()
    weightEntry.delete(0,len(weight))
    print(f"Weight :{weight}")

    
    return fromNode,toNode,weight



#shows nodeData's nested dictionaries line by line
def showNodeDataDict():
    print("")
    for i in range(numberOfNodes):
        print(nodeData[f"n{str(i)}"])
    print("")


def showEdges():
    print("\nNode edges :")

    for i in range(len(nodeEdges)):
        print(f"{i}:{nodeEdges[i]}")


#this will allow the user to reset the graph and placing new nodes and edges
def resetCanvas(customGraphFrame,canvas):
    global numberOfNodes,nodeData,nodeEdges
    customGraphFrame.delete('node')
    customGraphFrame.delete('edge')
    customGraphFrame.delete('nodeLabel')
    
    numberOfNodes = 0
    nodeData = {}
    nodeEdges = []


def runDijkstra(startNode):
    # rough start - start node will always be 0 
    # from prior validation, all the nodes will be at least be connected in the network 
    # if no edge between 2 nodes, they have weight 100, largest weight input is 99 - acts as inf+

    global numberOfNodes

    startNode = 0 
    for n in range(numberOfNodes):
        print(nodeEdges[n])
     
    

#procedure to place all the buttons and labels on the screen
def customGraphFrameWidgets(customGraphFrame):

    #text font I would like to use, the coding rooms original
    textFont_13D = ("DejaVu Sans",13)


    customGraphCanvas = tk.Canvas (customGraphFrame,
    width = screenWidth*0.8, height = screenHeight *0.8 , bg = "#414a4c")
    customGraphCanvas.place(relx=0.005,rely=0.01)

    mousePosLabel = tk.Label (
        customGraphFrame,
        width = 25,height = 3
    )
    mousePosLabel.place(relx = 0.33, rely=0.83)

    #tracks and displays the position of the mouse on the screen.
    customGraphCanvas.bind("<Motion>",lambda e: mousePosLabel.configure(text = f"Coordinates|x:{e.x},y:{e.y}|"))


    createNodeButton = tk.Button(
        customGraphFrame,text="Create Node",
        width = 50, height = 3,command = lambda: createNode(customGraphCanvas) 
    )
    createNodeButton.place(relx=0.005,rely=0.83)


    showNodeDataButton = tk.Button(
        customGraphFrame, text = "Print node data",
        width = 50 , height = 3, command = showNodeDataDict
    )
    showNodeDataButton.place(relx=0.49,rely=0.83)

    showEdgesButton = tk.Button(
        customGraphFrame,text= "Print edge data",
        width = 50, height = 3, command= showEdges
    )
    showEdgesButton.place(relx=0.70,rely=0.83)

    """Seperate frame inside customGraphFrame which will hold the edge creation entry boxes"""    
    
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
    edgeFromEntry = tk.Entry(
        edgeEntryFrame,
        width = 3
    )
    

    edgeToLabel = tk.Label(
        edgeEntryFrame,
        text = "To",
        height = 5,
        width =10
    )

    edgeToEntry = tk.Entry(
        edgeEntryFrame,
        width = 3
    )  
    weightLabel = tk.Label(
        edgeEntryFrame,
        text = "Weight",
        height = 5,
        width =10
    )
    
    weightEntry = tk.Entry(
        edgeEntryFrame,
        width=3,borderwidth=5,validate="key"
    )    
    edgeEntryButton = tk.Button(
        edgeEntryFrame, text = "Create edge",
        width = 20,font = textFont_13D)
    """Placing down all the widgets of edgeEntryFrame and configuring their commands"""

    edgeFromLabel.grid(row=1,column=0)
    edgeFromLabel.configure(font = textFont_13D)
    edgeFromEntry.grid(row=1,column=1)
    edgeFromEntry.configure(validatecommand = (edgeFromEntry.register(nodeInputValidation),'%P','%d'),font = textFont_13D)
    
    edgeToLabel.grid(row = 2, column =0)
    edgeToLabel.configure(font = textFont_13D)
    edgeToEntry.grid(row=2,column=1)
    edgeToEntry.configure(validatecommand = (edgeToEntry.register(nodeInputValidation),'%P','%d'),font = textFont_13D)
    

    weightLabel.grid(row = 3, column =0)
    weightLabel.configure(font = textFont_13D)
    weightEntry.grid(row=3,column=1)
    weightEntry.configure(validatecommand = (weightEntry.register(weightValidation),'%P','%d'),font = textFont_13D)
    
    
    edgeEntryButton.grid(row=4,columnspan =2 )
    edgeEntryButton.configure(command = lambda: createEdge(customGraphCanvas,edgeFromEntry,edgeToEntry,weightEntry))


def nodeInputValidation(inputString,actionType):
    global numberOfNodes
    if actionType =='1':
        if not inputString.isdigit():
            print("Inputs can only integers of the nodes")
            return False
        elif numberOfNodes <= 1:
            print("not enought nodes yet")
            return False
        elif int(inputString)>numberOfNodes:
            print("There is no node with this label")
            return False
    return True


def weightValidation(inputString,actionType):
    if actionType == '1': #a character insert will be a 1
        if not inputString.isdigit():
            print("Input can only be an integer")
            return False
        elif int(inputString) == 0 and len(inputString)==1:
            print("cannot start with 0")
            return False
        elif len(inputString)==3:
            print("Max weight - 99") # only allows 2 digit numbers - ie weight is 1 - 99 
            return False
    return True


main()
