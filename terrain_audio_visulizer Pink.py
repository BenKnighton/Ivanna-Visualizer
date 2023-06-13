meshColour = (0.96, 0.58, 0.53, 1) #0.96, 0.58, 0.53, 1
circleColour = (1, 0.463, 0.561, 1)
hexColour =(1, 0.349, 0.631, 1)#(0.866, 1, 0.6588, 1)#(1, 0.349, 0.631, 1)#(0.96, 0.58, 0.53, 1)
shortName = "IVANNA"
fullName = "Informative • Virtualy • Acting • Neural • Network • Assistant"
nameTextColour = (244, 147, 134)
fullNameTextColour = (244, 147, 134)
picture = 'Background copy.png'


from PIL import Image
import numpy as np
from opensimplex import OpenSimplex
import pyqtgraph.opengl as gl
from pyqtgraph.Qt import QtCore, QtGui
import struct
import pyaudio
import sys

from OpenGL.GL import *


text = """

 ### #     # ### ####### ###    #    #       ###  #####  ####### ######      
  #  ##    #  #     #     #    # #   #        #  #     # #       #     #     
  #  # #   #  #     #     #   #   #  #        #  #       #       #     #     
  #  #  #  #  #     #     #  #     # #        #   #####  #####   #     #     
  #  #   # #  #     #     #  ####### #        #        # #       #     #     
  #  #    ##  #     #     #  #     # #        #  #     # #       #     #     
 ### #     # ###    #    ### #     # ####### ###  #####  ####### ######      
                                                                                                                                            
"""

print(text)



#idea add vad and hence change noise levels
class Terrain(QtGui.QMainWindow):
    def __init__(self):
        super().__init__()
        #Initialize the graphics window and mesh surface
        
        # setup the view window
        self.window = gl.GLViewWidget()
        self.window.setWindowTitle("I.V.A.N.A")
        self.window.setGeometry(120, 80, 900, 700)

        self.window.setCameraPosition(distance=1200, elevation=8,)#80, 20
        self.window.show()

        scale_factor = 0.75
        # constants and arrays
        self.factor = 20 *scale_factor
        self.nsteps = 1.3 * self.factor
        
        self.offset = 0
        self.ypoints = np.arange((-20 * self.factor), (20 * self.factor) + self.nsteps, self.nsteps)
        self.xpoints = np.arange((-20 * self.factor) , (20 * self.factor) + self.nsteps, self.nsteps)
        self.nfaces = len(self.ypoints) #32
        # print(self.nfaces)

        self.RATE = 44100
        self.CHUNK = len(self.xpoints) * len(self.ypoints)

        self.p = pyaudio.PyAudio()
        self.stream = self.p.open(
            format=pyaudio.paInt16,
            channels=1,
            rate=self.RATE,
            input=True,
            output=True,
            frames_per_buffer=self.CHUNK,
        )
        
        # perlin noise object
        self.noise = OpenSimplex()

        # create the veritices array
        verts, faces, colors = self.mesh()

        #Audio Mesh
        self.mesh1 = gl.GLMeshItem(
            faces=faces,
            vertexes=verts,
            faceColors=colors,
            drawEdges=True,
            smooth=True,
            edgeColor=meshColour,
            drawFaces=False,
            # computeNormals=True,
        )
        # self.mesh1.setColor("black")
        self.mesh1.setGLOptions("opaque")
        # self.mesh1.setDepthValue(-0.1)
        # self.mesh1.setVisible(0.1)
        self.window.addItem(self.mesh1)


        #Hexagon
        # md = gl.MeshData.cylinder(6, 6, radius=[(y)/2, (y)/2], length=1)
        # m1 = gl.GLMeshItem(meshdata=md,
        #                         smooth=True,
        #                         color=(1, 1, 1, 1),
        #                         glOptions="additive")

        # m1.translate(0, 0, -120)
        # self.window.addItem(m1)


        distance = 50
        #Image
        image = Image.open(picture)
        data = np.array(image)

        y = data.shape[0]
        x = data.shape[1]

        img = gl.GLImageItem(data=data, smooth=True, glOptions='opaque')
        img.translate(-(y)/2, -(x)/2, -(180+distance))
        self.window.addItem(img)
        
        
        #Text 1
        #Watch face color (218, 219, 109)
        gm = gl.GLTextItem(text=shortName, color=nameTextColour)
        gm.setData(font= QtGui.QFont("OCR A Extended", 20))
        gm.translate(0, ((x)/2)-70, -(180+distance))
        self.window.addItem(gm)

        #Text 2
        gm = gl.GLTextItem(text=fullName, color=fullNameTextColour)
        gm.setData(font= QtGui.QFont("OCR A Extended", 9))
        gm.translate(((y)/2)-70, 0, -(180+distance))
        self.window.addItem(gm)
 


        #Hex 1
        hr = 300

        hd = gl.MeshData.cylinder(6, 6, radius=[hr,hr], length=1)
        h1 = gl.GLMeshItem(meshdata=hd,
                                smooth=True,
                                color=hexColour,
                                glOptions="additive")

        h1.translate(0, 0, -(20+distance))
        self.window.addItem(h1)

        #Hex 2
        hd = gl.MeshData.cylinder(6, 6, radius=[hr/2, hr/2], length=1)
        h1 = gl.GLMeshItem(meshdata=hd,
                                smooth=True,
                                color=hexColour,
                                glOptions="additive")

        h1.translate(0, hr*0.86603, -(20+distance)) # * (sqrt 3) / 2
        self.window.addItem(h1)

        #Hex 3
        hd = gl.MeshData.cylinder(6, 6, radius=[hr * 0.43301 , hr * 0.43301], length=1) # * (sqrt 3) / 4
        h1 = gl.GLMeshItem(meshdata=hd,
                                smooth=True,
                                color=hexColour,
                                glOptions="additive")

        h1.translate(hr, 0, -(20+distance))
        self.window.addItem(h1)



        #Circles
        md = gl.MeshData.cylinder(100, 100, radius=[(y/2)+50, (y/2)+50], length=1)
        m1 = gl.GLMeshItem(meshdata=md,
                                smooth=True,
                                color=(circleColour),
                                glOptions="additive")

        m1.translate(0, 0, -(120+distance))
        self.window.addItem(m1)









        #Circle mesh
        def Create_Verticies(y, x, xdisplacment = 0, ydisplacment = 0, factor=1, center=True):
            verts = []
            if center:
                xdisplacment = -x/2
                ydisplacment = -y/2

            #Line in  the y direction for 20 steps
            for j in range(y):
                for i in range(x):
                    a = [0+int(i)+xdisplacment, 0+int(j)+ydisplacment, 0]
                    b = [1+int(i)+xdisplacment, 1+int(j)+ydisplacment, 0]
                    c = [0+int(i)+xdisplacment, 1+int(j)+ydisplacment, 0]
                    verts.append([np.array(a)*factor, np.array(b)*factor, np.array(c)*factor])

                    a = [0+int(i)+xdisplacment, 0+int(j)+ydisplacment, 0]
                    b = [1+int(i)+xdisplacment, 0+int(j)+ydisplacment, 0]
                    c = [1+int(i)+xdisplacment, 1+int(j)+ydisplacment, 0]
                    verts.append([np.array(a)*factor, np.array(b)*factor, np.array(c)*factor])

            return np.array(verts, dtype=np.float32)


        verts = Create_Verticies(31, 31, factor=1) #32, 32,


        m2 = gl.GLMeshItem(
            vertexes=verts,
            smooth=True, 
            drawFaces=False,
            drawEdges=True,
            edgeColor=meshColour
                        )
        m2.translate(0,0,0)
        m2.scale(20*1.3*scale_factor, 20*1.3*scale_factor, 1)
        self.window.addItem(m2)




        len_M = 31

        x = [29, 27, 25, 21, 17, 11]
        for j, i in enumerate(x):
            verts = Create_Verticies(i, 1, factor=1, xdisplacment = (len_M/2)+j, ydisplacment = -i/2, center=False) #32, 32,
            m2 = gl.GLMeshItem(
                vertexes=verts,
                smooth=True, 
                drawFaces=False,
                drawEdges=True,
                edgeColor=meshColour
                            )

            m2.scale(20*1.3*scale_factor, 20*1.3*scale_factor, 1)
            self.window.addItem(m2)

        x = [29, 27, 25, 21, 17, 11]
        for j, i in enumerate(x):
            verts = Create_Verticies(i, 1, factor=1, xdisplacment = -(len_M/2)-j-1, ydisplacment = -i/2, center=False) #32, 32,
            m2 = gl.GLMeshItem(
                vertexes=verts,
                smooth=True, 
                drawFaces=False,
                drawEdges=True,
                edgeColor=meshColour
                            )

            m2.scale(20*1.3*scale_factor, 20*1.3*scale_factor, 1)
            self.window.addItem(m2)


        x = [29, 27, 25, 21, 17, 11]
        for j, i in enumerate(x):
            verts = Create_Verticies(1, i, factor=1, xdisplacment = -i/2, ydisplacment = -(len_M/2)-j-1, center=False) #32, 32,
            m2 = gl.GLMeshItem(
                vertexes=verts,
                smooth=True, 
                drawFaces=False,
                drawEdges=True,
                edgeColor=meshColour
                            )

            m2.scale(20*1.3*scale_factor, 20*1.3*scale_factor, 1)
            self.window.addItem(m2)

        x = [29, 27, 25, 21, 17, 11]
        for j, i in enumerate(x):
            verts = Create_Verticies(1, i, factor=1, xdisplacment = -i/2, ydisplacment = (len_M/2)+j, center=False) #32, 32,
            m2 = gl.GLMeshItem(
                vertexes=verts,
                smooth=True, 
                drawFaces=False,
                drawEdges=True,
                edgeColor=meshColour
                            )

            m2.scale(20*1.3*scale_factor, 20*1.3*scale_factor, 1)
            self.window.addItem(m2)
            # m2.translate(0,0,)
            # self.window.addItem(m2)





        t = 1

        x = [29, 27, 25, 21, 17, 11]
        for j, i in enumerate(x):
            verts = Create_Verticies(i, 1, factor=1, xdisplacment = (len_M/2)+j, ydisplacment = -i/2, center=False) #32, 32,
            m2 = gl.GLMeshItem(
                vertexes=verts,
                smooth=True, 
                drawFaces=False,
                drawEdges=True,
                edgeColor=meshColour
                            )

            m2.scale(20*1.3*scale_factor, 20*1.3*scale_factor, 1)
            m2.translate(0,t,0)
            self.window.addItem(m2)

        x = [29, 27, 25, 21, 17, 11]
        for j, i in enumerate(x):
            verts = Create_Verticies(i, 1, factor=1, xdisplacment = -(len_M/2)-j-1, ydisplacment = -i/2, center=False) #32, 32,
            m2 = gl.GLMeshItem(
                vertexes=verts,
                smooth=True, 
                drawFaces=False,
                drawEdges=True,
                edgeColor=meshColour
                            )

            m2.scale(20*1.3*scale_factor, 20*1.3*scale_factor, 1)
            m2.translate(0,t,0)
            self.window.addItem(m2)


        x = [29, 27, 25, 21, 17, 11]
        for j, i in enumerate(x):
            verts = Create_Verticies(1, i, factor=1, xdisplacment = -i/2, ydisplacment = -(len_M/2)-j-1, center=False) #32, 32,
            m2 = gl.GLMeshItem(
                vertexes=verts,
                smooth=True, 
                drawFaces=False,
                drawEdges=True,
                edgeColor=meshColour
                            )

            m2.scale(20*1.3*scale_factor, 20*1.3*scale_factor, 1)
            m2.translate(0,t,0)
            self.window.addItem(m2)

        x = [29, 27, 25, 21, 17, 11]
        for j, i in enumerate(x):
            verts = Create_Verticies(1, i, factor=1, xdisplacment = -i/2, ydisplacment = (len_M/2)+j, center=False) #32, 32,
            m2 = gl.GLMeshItem(
                vertexes=verts,
                smooth=True, 
                drawFaces=False,
                drawEdges=True,
                edgeColor=meshColour
                            )

            m2.scale(20*1.3*scale_factor, 20*1.3*scale_factor, 1)
            m2.translate(0,t,0)
            self.window.addItem(m2)











    def mesh(self, offset=0, height=2.5, wf_data=None):

        if wf_data is not None:
            wf_data = struct.unpack(str(2 * self.CHUNK) + "B", wf_data)
            wf_data = np.array(wf_data, dtype="b")[::2] + 128 
            wf_data = np.array(wf_data, dtype="int32") - 128
            
            wf_data = wf_data * 0.08  #height of verts
            wf_data = wf_data ** 2
            
            # if wf_data[0] < 0.5:
            #     wf_data = wf_data * 0
                
            
            wf_data = wf_data.reshape((len(self.xpoints), len(self.ypoints)))
        else:
            wf_data = np.array([1] * 1024)
            wf_data = wf_data.reshape((len(self.xpoints), len(self.ypoints)))

        faces = []
        colors = []
        verts = np.array([
            [x, y, wf_data[xid][yid] * self.noise.noise2(x=xid / 5 + offset, y=yid / 5 + offset)]
            for xid, x in enumerate(self.xpoints) for yid, y in enumerate(self.ypoints)], dtype=np.float32)

        for yid in range(self.nfaces - 1):
            yoff = yid * self.nfaces
            for xid in range(self.nfaces - 1):
                faces.append([
                    xid + yoff,
                    xid + yoff + self.nfaces,
                    xid + yoff + self.nfaces + 1,
                ])
                faces.append([
                    xid + yoff,
                    xid + yoff + 1,
                    xid + yoff + self.nfaces + 1,

                
                ])
                
                tupple_ = [0, 0, 0, 0] #colours
                colors.append(tupple_)
                colors.append(tupple_)

        faces = np.array(faces, dtype=np.uint32)
        colors = np.array(colors, dtype=np.float32)

        return verts, faces, colors #vers - down, + up

    def update(self):
        self.window.orbit(0.3,0)
        wf_data = self.stream.read(self.CHUNK, exception_on_overflow=False)
        verts, faces, colors = self.mesh(offset=self.offset, wf_data=wf_data)
        self.mesh1.setMeshData(vertexes=verts, faces=faces, faceColors=colors)
        self.offset -= 0.05 #tweak this value to change pitch og = 0.05

    def start(self):
        
        #get the graphics window open and setup
        if (sys.flags.interactive != 1) or not hasattr(QtCore, "PYQT_VERSION"):
            QtGui.QApplication.instance().exec_()

    def animation(self, frametime=10):
        
        #calls the update method to run in a loop
        timer = QtCore.QTimer()
        timer.timeout.connect(self.update)
        timer.start(frametime)
        self.start()

def audio_visualizer():
    t = Terrain()
    t.animation()

if __name__ == "__main__":
    app = QtGui.QApplication(sys.argv)
    audio_visualizer()



##from threading import Thread
##
##audio_visulizer = Thread(target=audio_visualizer, daemon=True)
##audio_visulizer.start()















