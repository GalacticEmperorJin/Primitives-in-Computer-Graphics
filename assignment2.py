import math as mt
import tkinter as tk
from tkinter import ttk
from pyopengltk import OpenGLFrame
from tkinter import *
from OpenGL.GL import *
from OpenGL.GLU import *
from OpenGL.GLUT import *
import subprocess

class AppOgl(OpenGLFrame):
    def initgl(self): # scene initialisation
 
        glLoadIdentity()
        glClearColor(0,0,0,0)
        gluPerspective(45, (self.width/self.height), 0.1, 1000.0)
        glTranslatef(0,-32,-725)
        glBlendFunc(GL_SRC_ALPHA, GL_ONE_MINUS_SRC_ALPHA)
        glEnable(GL_BLEND)
        glPointSize(10)
        
        #DDA line
        self.LineDDA = False
        self.LineDDAData = [None]*4
        
        #Bersenham line
        self.LineBersenham = False
        self.LineBersenhamData = [None]*4
        
        #midpoint line
        self.midPoint = False
        self.midPointData = [None]*3
        
        #circle area fill
        self.circleFill = False
        self.fillCircle = False
        self.circleFillData = (0,0,0)
    
        #triangle area fill
        self.triFill = False
        self.fillTri = False
        self.triFillData = ((0,0),(0,0),(0,0))
        
        #Line clipping
        self.clipLine = False
        self.clipLineData = [None]*4
        self.clipLineOverlay = False
        self.clipLineOverlayData = []
        self.clipLineStart = False
        
        #triangle clipping
        self.clipTri = False
        self.clipTriData = [None]*6
        self.clipTriOverlay = False
        self.clipTriOverlayData = []
        self.clipTriStart = False
    
    def redraw(self):
        
        glClear(GL_COLOR_BUFFER_BIT | GL_DEPTH_BUFFER_BIT)
        self.plotFunc()
        
        if self.LineDDA:
            try: LineDDA(self.LineDDAData[0],self.LineDDAData[1],self.LineDDAData[2],self.LineDDAData[3])
            except: pass
            
        if self.LineBersenham:
            try: LineBersenham(self.LineBersenhamData[0],self.LineBersenhamData[1],self.LineBersenhamData [2],self.LineBersenhamData[3])
            except: pass
            
        if self.midPoint:
            try: midPoint(self.midPointData[0],self.midPointData[1],self.midPointData[2])
            except: pass
            
        if self.circleFill == True:
            if self.fillCircle == True:
                fill = True
            else: fill = False
            try: 
                areaFilling(c1 = (self.circleFillData[0], self.circleFillData[1]) , r = self.circleFillData[2], shape = 'c', fill = fill)
            except: pass
        
        if self.triFill == True:
            if self.fillTri == True:
                fill = True
            else: fill = False
            try:
                areaFilling(c1=(self.triFillData[0],self.triFillData[1]),c2 = (self.triFillData[2],self.triFillData[3]), c3 = (self.triFillData[4],self.triFillData[5]),shape = 't', fill = fill)
            except: pass
                
        if self.clipLine == True:
            try: LineDDA(self.clipLineData[0],self.clipLineData[1],self.clipLineData[2],self.clipLineData[3])
            except: pass
        if self.clipLineOverlay == True:
            for i in self.clipLineOverlayData:
                LineDDA(i[0],i[1],i[2],i[3])
        if self.clipLineStart == True:
            Clipping(self,self.clipLineOverlayData, 'line')
            
        if self.clipTri == True:
            try:
                LineDDA(self.clipTriData[0],self.clipTriData[1],self.clipTriData[2],self.clipTriData[3])
                LineDDA(self.clipTriData[2],self.clipTriData[3],self.clipTriData[4],self.clipTriData[5])
                LineDDA(self.clipTriData[4],self.clipTriData[5],self.clipTriData[0],self.clipTriData[1])
            except: pass
        if self.clipTriOverlay == True:
            try: 
                for i in self.clipTriOverlayData:
                    LineDDA(i[0],i[1],i[2],i[3])
            except:pass
        if self.clipTriStart == True:
            Clipping(self,self.clipTriOverlayData, 'triangle')

            
    def plotFunc(self):
        glColor4f(1,1,1,1)
        glBegin(GL_LINES)
        glVertex2f(-self.width/2,0)
        glVertex2f(self.width,0)
        glVertex2f(0,-self.height/2)
        glVertex2f(0,self.height)
        glEnd()
      

class tkWindow():
    def __init__(self,root,app) -> None:
        self.root = root
        self.app = app
        
        self.sidebar()
        self.button()
        self.setup()
    
    def sidebar(self):
        
        label = Label(root, text="Primitives in Computer Graphics", font = 'times 20',fg= 'white', background="#0e1013")
        label.pack(side = TOP, anchor = N, pady = 5)
        
        frame = Frame(root, height = 35, background="#0e1013")
        frame.pack(side = TOP, anchor = N, fill = BOTH, expand = YES)
        
    def button(self): #sidebar button
        # Selection comboBox
        selectionBox = ttk.Combobox(root, width=20)
        selectionBox['values'] = ("DDA line", "Bersenham line","Mid Point Circle Drawing","Circle Fill","Triangle Fill","Line Clipping", "Triangle Clipping")
        selectionBox.place( x = 15, y = 50)
        selectionBox.bind('<<ComboboxSelected>>',self.selectFunc)
        
        self.resetButton = tk.Button(root, width = 10, text = "RESET",command = lambda: self.reset())
        self.resetButton.place(x = 705, y = 45)
    
    def selectFunc(self,event):
        if event.widget.get() == "DDA line": self.entryDDA()
        
        if event.widget.get() == "Bersenham line": self.entryBersenham()
        
        if event.widget.get() == "Mid Point Circle Drawing": self.entryMidpoint()
        
        if event.widget.get() == "Circle Fill": self.entryAreaFillCir()
        
        if event.widget.get() == "Triangle Fill": self.entryAreaFillTri()
        
        if event.widget.get() == "Line Clipping": self.entryLineclipping()
        
        if event.widget.get() == "Triangle Clipping": self.entryTriclipping()
        
        # if event.widget.get() == "3d Object": self.enterObjLoader()
        
    def setup(self):
        # DDA setup
        self.DDAx1label = ttk.Label(root, text = "x1:")
        self.DDAx1entry = ttk.Entry(root, width = 5)
        
        self.DDAy1label = ttk.Label(root, text="y1:")
        self.DDAy1entry = ttk.Entry(root, width=5)
        
        self.DDAx2label = ttk.Label(root, text="x2:")
        self.DDAx2entry = ttk.Entry(root, width=5)
        
        self.DDAy2label = ttk.Label(root, text="y2:")
        self.DDAy2entry = ttk.Entry(root, width=5)
        
        self.drawDDAButton = ttk.Button(root,width = 15,text = "Draw Line", command = lambda: self.draw_lineDDA())
        
        #Bresenham setup
        self.Bx1label = ttk.Label(root, text = "x1:")
        self.Bx1entry = ttk.Entry(root, width = 5)
        
        self.By1label = ttk.Label(root, text="y1:")
        self.By1entry = ttk.Entry(root, width=5)
        
        self.Bx2label = ttk.Label(root, text="x2:")
        self.Bx2entry = ttk.Entry(root, width=5)
        
        self.By2label = ttk.Label(root, text="y2:")
        self.By2entry = ttk.Entry(root, width=5)
        
        self.drawBresenhamButton = ttk.Button(root,width = 15,text = "Draw Line", command = lambda: self.draw_lineBersenham())
        
        #midpoint 
        self.CxLabel = ttk.Label(root, text = "x :")
        self.CxEntry = ttk.Entry(root, width = 5)
        
        self.CyLabel = ttk.Label(root, text="y :")
        self.CyEntry = ttk.Entry(root, width=5)
        
        self.radLabel = ttk.Label(root, text="Radius:")
        self.radEntry = ttk.Entry(root, width=5)
        
        self.drawMidButton = ttk.Button(root,width = 15,text = "Draw Circle", command = lambda: self.draw_midPoint())
        
        #Area  Filling
        self.AFCxlabel = ttk.Label(root, text = "x: ")
        self.AFCxentry = ttk.Entry(root, width = 5)
        
        self.AFCylabel = ttk.Label(root, text = "y: ")
        self.AFCyentry = ttk.Entry(root, width=5)
        
        self.AFCRadlabel = ttk.Label(root, text="Rad:")
        self.AFCRadentry = ttk.Entry(root, width=5)
        
        self.drawCircleButton = ttk.Button(root,width = 15,text = "Fill", command = lambda: self.fillCir())
        self.fillButton = ttk.Button(root, width = 15, text = "Draw Circle", command = lambda: self.draw_AreaFillCir())
        
        #Triangle Filling
        self.AFTx1label = ttk.Label(root, text = "x1: ")
        self.AFTx1entry = ttk.Entry(root, width = 5)
        self.AFTy1label = ttk.Label(root, text = "y1: ")
        self.AFTy1entry = ttk.Entry(root, width = 5)
        
        self.AFTx2label = ttk.Label(root, text = "x2: ")
        self.AFTx2entry = ttk.Entry(root, width = 5)
        self.AFTy2label = ttk.Label(root, text = "y2: ")
        self.AFTy2entry = ttk.Entry(root, width = 5)
        
        self.AFTx3label = ttk.Label(root, text = "x3: ")
        self.AFTx3entry = ttk.Entry(root, width = 5)
        self.AFTy3label = ttk.Label(root, text = "y3: ")
        self.AFTy3entry = ttk.Entry(root, width = 5)
        
        self.drawTriButton = ttk.Button(root,width = 15,text = "Fill", command = lambda: self.fillTri())
        self.fillTriButton = ttk.Button(root, width = 15, text = "Draw Triangle", command = lambda: self.draw_AreaFillTri())
        
        #line clipping
        self.clipLx1label = ttk.Label(root, text = "x1:")
        self.clipLx1entry = ttk.Entry(root, width = 5)
        
        self.clipLy1label = ttk.Label(root, text="y1:")
        self.clipLy1entry = ttk.Entry(root, width=5)
        
        self.clipLx2label = ttk.Label(root, text="x2:")
        self.clipLx2entry = ttk.Entry(root, width=5)
        
        self.clipLy2label = ttk.Label(root, text="y2:")
        self.clipLy2entry = ttk.Entry(root, width=5)
        
        self.drawClipButton = ttk.Button(root,width = 15,text = "Draw Line", command = lambda: self.clipLineOK())
        self.clipButton = ttk.Button(root, width = 15, text = "Clip Line", command = lambda: self.clipLineStart())
        
        #triangle clipping
        self.clipTx1label = ttk.Label(root, text = "x1:")
        self.clipTx1entry = ttk.Entry(root, width = 5)
        self.clipTy1label = ttk.Label(root, text="y1:")
        self.clipTy1entry = ttk.Entry(root, width=5)
        
        self.clipTx2label = ttk.Label(root, text="x2:")
        self.clipTx2entry = ttk.Entry(root, width=5)
        self.clipTy2label = ttk.Label(root, text="y2:")
        self.clipTy2entry = ttk.Entry(root, width=5)
        
        self.clipTx3label = ttk.Label(root, text="x3:")
        self.clipTx3entry = ttk.Entry(root, width=5)
        self.clipTy3label = ttk.Label(root, text="y3:")
        self.clipTy3entry = ttk.Entry(root, width=5)
        
        self.drawClipTbutton = ttk.Button(root,width = 15,text = "Draw Triangle", command = lambda: self.clipTriOK())
        self.clipTbutton = ttk.Button(root, width = 15, text = "Clip Triangle", command = lambda: self.clipTriStart())
        
        #3d object loader
        # self.loadButton = ttk.Button(root,width = 15,text = "Load 3d Object", command = lambda: self.objLoad())
       
        
    def entryDDA(self):
        self.DDAx1label.place(x = 180, y = 51)
        self.DDAx1entry.place(x = 205, y = 50)
        self.DDAy1label.place(x = 250, y = 51)
        self.DDAy1entry.place(x = 275, y = 50)
        self.DDAx2label.place(x = 320, y = 51)
        self.DDAx2entry.place(x = 345, y = 50)
        self.DDAy2label.place(x = 390, y = 51)
        self.DDAy2entry.place(x = 415, y = 50)   
        self.drawDDAButton.place(x = 595, y = 45)      
    
    def entryBersenham(self):
        
        self.Bx1label.place(x = 180, y = 51)
        self.Bx1entry.place(x = 205, y = 50)
        self.By1label.place(x = 250, y = 51)
        self.By1entry.place(x = 275, y = 50)
        self.Bx2label.place(x = 320, y = 51)
        self.Bx2entry.place(x = 345, y = 50)
        self.By2label.place(x = 390, y = 51)
        self.By2entry.place(x = 415, y = 50)   
        
        self.drawBresenhamButton.place(x = 595, y = 45)
        
    def entryMidpoint(self):
        
        self.CxLabel.place(x = 180, y = 51)
        self.CxEntry.place(x = 205, y = 50)
        self.CyLabel.place(x = 250, y = 51)
        self.CyEntry.place(x = 275, y = 50)
        self.radLabel.place(x = 320, y = 51)
        self.radEntry.place(x = 370, y = 50)
        self.drawMidButton.place(x = 595, y = 45)
    
    def entryAreaFillCir(self):
       
        self.AFCxlabel.place(x = 180, y = 51)
        self.AFCxentry.place(x = 205, y = 50)
        self.AFCylabel.place(x = 280, y = 51)
        self.AFCyentry.place(x = 305, y = 50)
        self.AFCRadlabel.place(x = 380, y = 51)
        self.AFCRadentry.place(x = 415, y = 50)   
        self.drawCircleButton.place(x = 595, y = 45)
        self.fillButton.place(x = 490, y = 45)
    
    def entryAreaFillTri(self):
        
        self.AFTx1label.place(x = 180, y = 51)
        self.AFTx1entry.place(x = 205, y = 50)
        self.AFTy1label.place(x = 250, y = 51)
        self.AFTy1entry.place(x = 275, y = 50)
        
        self.AFTx2label.place(x = 320, y = 51)
        self.AFTx2entry.place(x = 345, y = 50)
        self.AFTy2label.place(x = 390, y = 51)
        self.AFTy2entry.place(x = 415, y = 50)
        
        self.AFTx3label.place(x = 460, y = 51)
        self.AFTx3entry.place(x = 485, y = 50)
        self.AFTy3label.place(x = 530, y = 51)
        self.AFTy3entry.place(x = 555, y = 50)
            
        self.drawTriButton.place(x = 600, y = 45)
        self.fillTriButton.place(x = 600, y = 15)  
    
    def entryLineclipping(self):
        
        self.clipLx1label.place(x = 180, y = 51)
        self.clipLx1entry.place(x = 205, y = 50)
        self.clipLy1label.place(x = 250, y = 51)
        self.clipLy1entry.place(x = 275, y = 50)
        self.clipLx2label.place(x = 320, y = 51)
        self.clipLx2entry.place(x = 345, y = 50)
        self.clipLy2label.place(x = 390, y = 51)
        self.clipLy2entry.place(x = 415, y = 50)   
        self.drawClipButton.place(x = 595, y = 45)
        self.clipButton.place(x = 490, y = 45)     
    
    def entryTriclipping(self):
        self.clipTx1label.place(x = 180, y = 51)
        self.clipTx1entry.place(x = 205, y = 50)
        self.clipTy1label.place(x = 250, y = 51)
        self.clipTy1entry.place(x = 275, y = 50)
        self.clipTx2label.place(x = 320, y = 51)
        self.clipTx2entry.place(x = 345, y = 50)
        self.clipTy2label.place(x = 390, y = 51)
        self.clipTy2entry.place(x = 415, y = 50)
        self.clipTx3label.place(x = 460, y = 51)
        self.clipTx3entry.place(x = 485, y = 50)
        self.clipTy3label.place(x = 530, y = 51)
        self.clipTy3entry.place(x = 555, y = 50)
            
        self.drawClipTbutton.place(x = 600, y = 45)
        self.clipTbutton.place(x = 600, y = 15)   
    
    # def enterObjLoader(self):
    #     self.loadButton.place(x = 350, y = 50)
        
    def draw_lineDDA(self):
        self.app.LineDDA = True
        try:
            self.app.LineDDAData[0] = int(self.DDAx1entry.get())
            self.app.LineDDAData[1] = int(self.DDAy1entry.get())
            self.app.LineDDAData[2] = int(self.DDAx2entry.get())
            self.app.LineDDAData[3] = int(self.DDAy2entry.get())
        except: pass

    def draw_lineBersenham(self):
        self.app.LineBersenham = True
        try:
            self.app.LineBersenhamData[0] = int(self.Bx1entry.get())
            self.app.LineBersenhamData[1] = int(self.By1entry.get())
            self.app.LineBersenhamData[2] = int(self.Bx2entry.get())
            self.app.LineBersenhamData[3] = int(self.By2entry.get())
        except: pass

    def draw_midPoint(self):
        self.app.midPoint = True
        try:
            self.app.midPointData[0] = int(self.CxEntry.get())
            self.app.midPointData[1] = int(self.CyEntry.get())
            self.app.midPointData[2] = int(self.radEntry.get())
        except: pass
    
    def draw_AreaFillCir(self):
        self.app.circleFill = True
        try: self.app.circleFillData = (int(self.AFCxentry.get()), int(self.AFCyentry.get()), int(self.AFCRadentry.get()))
        except: pass 
    
    def fillCir(self):
        self.draw_AreaFillCir()
        self.app.fillCircle = True
        
    def draw_AreaFillTri(self):
        self.app.triFill = True
        try: self.app.triFillData = (int(self.AFTx1entry.get()),int(self.AFTy1entry.get()),int(self.AFTx2entry.get()),int(self.AFTy2entry.get()),int(self.AFTx3entry.get()),int(self.AFTy3entry.get()))
        except: pass
        
    def fillTri(self):
        self.draw_AreaFillTri()
        self.app.fillTri = True
        
    def clipLineOK(self):
        self.app.clipLineOverlay = True
        try:
            x1 = int(self.clipLx1entry.get())
            y1 = int(self.clipLy1entry.get())
            x2 = int(self.clipLx2entry.get())
            y2 = int(self.clipLy2entry.get())
            self.app.clipLineOverlayData.append([x1,y1,x2,y2])
        except: pass
    
    def clipLineStart(self):
        self.clipLineOK()
        self.app.clipLine = False
        self.app.clipLineStart = True 
        
    def clipTriOK(self):
        self.app.clipTriOverlay = True
        try:
            x1= int(self.clipTx1entry.get())
            y1 = int(self.clipTy1entry.get())
            x2 = int(self.clipTx2entry.get())
            y2 = int(self.clipTy2entry.get())
            x3 = int(self.clipTx3entry.get())
            y3 = int(self.clipTy3entry.get())
            self.app.clipTriOverlayData.append([x1,y1,x2,y2])
            self.app.clipTriOverlayData.append([x2,y2,x3,y3])
            self.app.clipTriOverlayData.append([x3,y3,x1,y1])
        except: pass
    
    def clipTriStart(self):
        self.clipTriOK()
        self.app.clipTri = False
        self.app.clipTriStart = True
    
    # def objLoad(self):
        
    #     subprocess.Popen(["python", "P:\python1\Assignment\objLoader.py"])
             
    def reset(self):
        self.app.initgl()
    
        #delete entry for dda entry
        self.DDAx1entry.delete(0,'end')
        self.DDAy1entry.delete(0,'end')       
        self.DDAx2entry.delete(0,'end')
        self.DDAy2entry.delete(0,'end')
            
        #delete block for dda entry
        self.DDAx1label.place_forget()
        self.DDAx1entry.place_forget()
        self.DDAy1label.place_forget()
        self.DDAy1entry.place_forget()
        self.DDAx2label.place_forget()
        self.DDAx2entry.place_forget()
        self.DDAy2label.place_forget()
        self.DDAy2entry.place_forget()
        self.drawDDAButton.place_forget()     
        
        #delete entry for Bersenham entry
        self.Bx1entry.delete(0,'end')
        self.By1entry.delete(0,'end')
        self.Bx2entry.delete(0,'end')
        self.By2entry.delete(0,'end')
            
        #delete block for Bersenham entry
        self.Bx1label.place_forget()
        self.Bx1entry.place_forget()        
        self.By1label.place_forget()
        self.By1entry.place_forget()
        self.Bx2label.place_forget()
        self.Bx2entry.place_forget()
        self.By2label.place_forget()
        self.By2entry.place_forget()
        self.drawBresenhamButton.place_forget()
        
        #delete entry for midPoint
        self.CxEntry.delete(0,'end')
        self.CyEntry.delete(0,'end')
        self.radEntry.delete(0,'end')
        
        #delete block for midPoint
        self.CxLabel.place_forget()
        self.CxEntry.place_forget()
        self.CyLabel.place_forget()
        self.CyEntry.place_forget()
        self.radLabel.place_forget() 
        self.radEntry.place_forget()
        
        self.drawMidButton.place_forget()
        
        #delete entry for Area Filling Circle entry
        self.AFCxentry.delete(0,'end')
        self.AFCyentry.delete(0,'end') 
        self.AFCRadentry.delete(0,'end')
      
        #delete block for Area Filling Circle entry
        self.AFCxlabel.place_forget()
        self.AFCxentry.place_forget()
        self.AFCylabel.place_forget()
        self.AFCyentry.place_forget()
        self.AFCRadlabel.place_forget()
        self.AFCRadentry.place_forget() 
        
        self.drawCircleButton.place_forget()
        self.fillButton.place_forget()
        
        #delete entry for triangle filling
        self.AFTx1entry.delete(0,'end')
        self.AFTy1entry.delete(0,'end')
        self.AFTx2entry.delete(0,'end')
        self.AFTy2entry.delete(0,'end')
        self.AFTx3entry.delete(0,'end')
        self.AFTy3entry.delete(0,'end')
        
        #delete block for triangle filling
        self.AFTx1label.place_forget()
        self.AFTx1entry.place_forget()
        self.AFTy1label.place_forget()
        self.AFTy1entry.place_forget()
        
        self.AFTx2label.place_forget()
        self.AFTx2entry.place_forget()
        self.AFTy2label.place_forget()
        self.AFTy2entry.place_forget()
        
        self.AFTx3label.place_forget()
        self.AFTx3entry.place_forget()
        self.AFTy3label.place_forget()
        self.AFTy3entry.place_forget()
            
        self.drawTriButton.place_forget()
        self.fillTriButton.place_forget() 
        
        #delete entry for line clipping
        self.clipLx1entry.delete(0,'end')
        self.clipLy1entry.delete(0,'end')
        self.clipLx2entry.delete(0,'end')
        self.clipLy2entry.delete(0,'end')
        
        #delete block for line clipping
        self.clipLx1label.place_forget()
        self.clipLx1entry.place_forget()
        self.clipLy1label.place_forget()
        self.clipLy1entry.place_forget()
        self.clipLx2label.place_forget()
        self.clipLx2entry.place_forget()
        self.clipLy2label.place_forget()
        self.clipLy2entry.place_forget()
        
        self.drawClipButton.place_forget()
        self.clipButton.place_forget()
        
        #delete entry for triangle clipping
    
        self.clipTx1entry.delete(0, 'end')
        self.clipTy1entry.delete(0, 'end')
        self.clipTx2entry.delete(0, 'end')
        self.clipTy2entry.delete(0, 'end')
        self.clipTx3entry.delete(0, 'end')
        self.clipTy3entry.delete(0, 'end')
        
        #delete block for triangle clipping
        self.clipTx1label.place_forget()
        self.clipTx1entry.place_forget()
        self.clipTy1label.place_forget()
        self.clipTy1entry.place_forget()
        self.clipTx2label.place_forget()
        self.clipTx2entry.place_forget()
        self.clipTy2label.place_forget()
        self.clipTy2entry.place_forget()
        self.clipTx3label.place_forget()
        self.clipTx3entry.place_forget()
        self.clipTy3label.place_forget()
        self.clipTy3entry.place_forget()
            
        self.drawClipTbutton.place_forget()
        self.clipTbutton.place_forget()   
    
#formula
class LineDDA:
    def __init__(self,x1,y1,x2,y2) -> None:
        
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.formula(x1,y1,x2,y2)
    
    
    def point(self, x1, y1):
        
        glPointSize(3)
        glColor3f(1,0,0)
        glBegin(GL_POINTS)
        glVertex3f(x1,y1,0)
        glEnd()
    
    def formula(self,x1,y1,x2,y2):
        dX = x2 - x1
        dY = y2 - y1
        
        if(abs(dX) > abs(dY)):
            steps = abs(dX)
        else:
            steps = abs(dY)
        
        xInc = dX/steps
        yInc = dY/steps
        
        x = x1
        y = y1
        i = 1
        
        while i <= steps:
            self.point(mt.floor(x),mt.floor(y))
            x += xInc
            y += yInc
            i += 1


class LineBersenham:     
    def __init__(self, x1, y1, x2, y2) -> None:
        
        self.x1 = x1
        self.y1 = y1
        self.x2 = x2
        self.y2 = y2
        self.formulaBersenham(x1,y1,x2,y2)

    def Point(self,x1,y1):
        glPointSize(3)
        glColor3f(0.0, 0.0, 1.0)
        glBegin(GL_POINTS)
        glVertex3f(x1, y1,0.0)
        glEnd()

    def formulaBersenham(self, x1, y1, x2, y2):
        
        dx = abs(x2 - x1)
        dy = abs(y2 - y1)
        slope = dy/float(dx)
        x, y = x1, y1 
        if slope > 0:
            dx, dy = dy, dx
            x, y = y, x
            x1, y1 = y1, x1
            x2, y2 = y2, x2
        p = 2 * dy - dx
        self.Point(x, y)
        for k in range(2, dx):
            if p > 0:
                y = y + 1 if y < y2 else y - 1
                p = p + 2*(dy - dx)
            else:
                p = p + 2*dy
            x = x + 1 if x < x2 else x - 1
            self.Point(x, y) 


class midPoint:
    def __init__(self, Cx, Cy, rad) -> None:
        self.Cx = Cx
        self.Cy = Cy
        self.r = rad
        self.drawCircle()

    def drawCircle(self):
        P = 1 - self.r
        X = 0
        Y = self.r
        while X <= Y:
            X = X + 1
            if P < 0:
                P = P + 2 * X + 1
            else:
                P = P + 2 * (X - Y) + 1
                Y = Y - 1
            self.draw(X,Y,self.Cx,self.Cy)
    
    def draw(self,x,y,Cx,Cy):
        self.Point(Cx+x, Cy+y)
        self.Point(Cx+x, Cy-y)
        self.Point(Cx-x, Cy+y)
        self.Point(Cx-x, Cy-y)
        self.Point(Cx+y, Cy+x)
        self.Point(Cx-y, Cy+x)
        self.Point(Cx+y, Cy-x)
        self.Point(Cx-y, Cy-x)

    def Point(self,x0,y0):
        glPointSize(3)
        glColor3f(0,1,0)
        glBegin(GL_POINTS)
        glVertex3f(x0, y0,0.1)
        glEnd()            


class areaFilling:
    def __init__(self, c1 = (0,0), c2 = (0,0), c3 = (0,0), r = 0, shape = '', fill = False) -> None:
        
        if shape == 'c':
            midPoint(c1[0], c1[1], r)
            if fill:
                self.floodFill(c1[0] + 400, c1[1] + 268)
        elif shape == 't':
            glLineWidth(5)
            glColor(1,0,0)
            glBegin(GL_LINE_LOOP)
            glVertex2f(c1[0],c1[1])
            glVertex2f(c2[0],c2[1])
            glVertex2f(c3[0],c3[1])
            glEnd()
            glLineWidth(1)

            x = (c1[0] + c2[0] + c3[0])/3
            y = (c1[1] + c2[1] + c3[1])/3
            if fill:
                self.floodFill(x + 400, y + 268)

 
    def floodFill(self,x,y):
        start = self.getColor(x,y)
        queue = [(x,y)]
        visited = set()
        while len(queue) > 0:
            x,y = queue.pop()
            visited.add((x,y))
            self.setPixel(x,y)
            
            for x,y in self.neighbors(x,y,start):
                if (x,y) not in visited:
                    queue.append((x,y))

    def neighbors(self,x,y,start):
        indices = [(x+3,y), (x-3,y), (x,y-3), (x,y+3)]
        return [(x,y) for x,y in indices if self.isValid(x,y) and self.getColor(x,y) == start]

    def isValid(self,x,y):
        return x >= 0 and y >= 0 and x < 800 and y < 600

    def setPixel(self,x, y):
        glPointSize(4.3)
        glBegin(GL_POINTS)
        glVertex2f(x - 400,y - 268)
        glEnd()
        glFlush()

    def getColor(self,x, y):
        color = (GLuint * 1)(0)
        glReadPixels(x, y, 1, 1, GL_RGB, GL_UNSIGNED_BYTE, color)
        color = int(color[0])
        r = color & 255
        g = (color >> 8) & 255
        b = (color >> 16) & 255
        color = (r, g, b)
        return color


class Clipping:
    def __init__(self, app, lineData, shape) -> None:
        self.app = app
        self.lineData = lineData
        self.shape = shape
        self.xmin = -155
        self.xmax = 155
        self.ymin = -80
        self.ymax = 80

        self.left = 1
        self.right = 2
        self.bot = 4
        self.top = 8

        self.clipBox()
        self.compute()

    def clipBox(self):
        glColor3f(1,1,1)
        glBegin(GL_LINE_LOOP)
        glVertex2f(self.xmin, self.ymin)
        glVertex2f(self.xmax, self.ymin)
        glVertex2f(self.xmax, self.ymax)
        glVertex2f(self.xmin, self.ymax)
        glEnd()

    def compute(self):
        i = 0
        while i < len(self.lineData):
            while True:
                self.C1 = self.getCode(self.lineData[i][0],self.lineData[i][1])
                self.C2 = self.getCode(self.lineData[i][2],self.lineData[i][3])

                if (self.C1 | self.C2) == 0:
                    break
                elif (self.C1 & self.C2) != 0:
                    if self.shape == 'line':
                        self.app.clipLineOverlayData.pop(i)
                    elif self.shape == 'triangle':
                        self.app.clipTriOverlayData.pop(i)
                    break
                else:
                    self.clip(self.lineData[i][0], self.lineData[i][1], self.lineData[i][2], self.lineData[i][3], i)
            i += 1

    def clip(self,x1,y1,x2,y2, i):
        if self.C1:
            C = self.C1
        else:
            C = self.C2

        if C & self.left:
            x = self.xmin
            y = y1 + (y2-y1) * ((self.xmin - x1)/(x2 - x1))
        if C & self.right:
            x = self.xmax
            y = y1 + (y2-y1) * ((self.xmax - x1)/(x2 - x1))
        if C & self.bot:
            y = self.ymin
            x = x1 + (x2-x1) * ((self.ymin - y1)/(y2 - y1))
        if C & self.top:
            y = self.ymax
            x = x1 + (x2-x1) * ((self.ymax - y1)/(y2 - y1))

        if self.shape == 'line':
            data = self.app.clipLineOverlayData[i]
        elif self.shape == 'triangle':
            data = self.app.clipTriOverlayData[i]
            
        if C == self.C1:
            data[0] = x
            data[1] = y
        else:
            data[2] = x
            data[3] = y

    def getCode(self, x,y):
        Code = 0
        if x < self.xmin:
            Code = Code | self.left
        if x > self.xmax:
            Code = Code | self.right
        if y < self.ymin:
            Code = Code | self.bot
        if y > self.ymax:
            Code = Code | self.top
        if Code != 0:
            print(Code)
        return Code
                  
if __name__ == "__main__":
    root = tk.Tk()
    root.title("FCG_Assignment2")
    root.minsize(800,600)
    root.configure(background="#0e1013")
    
    app = AppOgl(root, width = 800, height = 600)
    app.animate = 1
    
    tkWindow(root, app)
    
    app.pack(fill=tk.BOTH, expand=tk.YES)
    app.mainloop()