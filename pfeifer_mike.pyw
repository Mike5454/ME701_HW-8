import sys
import numpy as np

import matplotlib
matplotlib.use('Qt5Agg')

from PyQt5.QtWidgets import QApplication, QLabel, QLineEdit, QVBoxLayout, QComboBox, \
QSizePolicy, QPushButton, QFileDialog

from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

class Form(QLabel) :
    def __init__(self, parent=None) :
        super(Form, self).__init__(parent)
        self.setGeometry(300, 300, 800, 800)
        self.setWindowTitle('Function Calculator')
        # Define three text boxes, one each for f(x), the value x, and
        # the output.  I've done the first for you.
        self.function_edit = QComboBox(self)
        self.function_edit.addItem ("sin(x)")
        self.function_edit.addItem ("cos(x)")
        self.function_edit.addItem ("tan(x)")
        self.function_edit.addItem ("custom")
        # Step 1. Add box for "x"
        self.value_edit = QLineEdit("x = ...")
        self.value_edit.selectAll()
        # Step 2. Add box for "output"
        self.output_edit = QLineEdit(" ")
        self.plot = MatplotlibCanvas()
        self.output_edit.selectAll()
        self.btn1 = QPushButton("Save File", self)
        # Step 3. How do we combine these widgets?  Use a *layout*....
        layout = QVBoxLayout ()
        layout.addWidget(self.function_edit)
        layout.addWidget(self.value_edit)
        layout.addWidget(self.output_edit)
        layout.addWidget(self.btn1)
        layout.addWidget(self.plot)
        self.setLayout(layout)
        # Step 4. Make sure the function box is the default one active.
        
        # Step 5. Connect updateUI to the event that one returns while the 
        #         output box is active
        self.btn1.clicked.connect(self.save)
        
        self.output_edit.returnPressed.connect(self.updateUI)
        self.function_edit.currentIndexChanged.connect(self.i)
        # Step 6. Implement updateUI.

        # Step 7. Give the GUI a title.
        
    def i(self):
        i = self.function_edit.currentIndex()
        if i ==3 : 
            self.function_edit.setEditable(True)
        else:
            self.function_edit.setEditable(False)
        
    def save(self):
        x = self.value_edit.text()
        fun = self.function_edit.currentText()
        out = self.output_edit.text()
        name = QFileDialog.getSaveFileName(self, 'Save File', 'path/to/default', '*.txt')
        name = str(name[0])
        wri = open(name,'w')
        wri.write("The Function %s\n \n" % fun)
        wri.write("The x Values %s\n" % x)
        wri.write("\n The y Values\n %s" % out)
        wri.close
        
    def updateUI(self) :
        check = self.function_edit.currentIndex()
        val = self.function_edit.currentText()
        if check != 3 :
            val = str("np.") + str(val)
        c = self.value_edit.text()
        y = eval(str(c))
        if type(y) == tuple:
            fin = []
            for z in y:
                x = z
                ans = eval(val)
                fin.append(ans)
        else:
            x = y
            fin = eval(val)
        self.output_edit.setText(str(fin))
        self.plot.redraw(y, fin)
       
class MatplotlibCanvas(FigureCanvas) :
    
    def __init__(self, parent=None, width=5, height=4, dpi=100) :
        self.fig = Figure(figsize=(width, height), dpi=dpi)
        self.axes = self.fig.add_subplot(111)
        self.axes.hold(False)
        self.compute_initial_figure()
        FigureCanvas.__init__(self, self.fig)
        self.setParent(parent)
        FigureCanvas.setSizePolicy(self, QSizePolicy.Expanding, QSizePolicy.Expanding)
        FigureCanvas.updateGeometry(self)
      
    def compute_initial_figure(self):
        self.x = 0
        self.y = 0
        self.axes.plot(self.x, self.y)
        self.axes.set_xlabel('x')
        self.axes.set_ylabel('y(x)')    
        
    def redraw(self, x, y) :
        self.axes.plot(x, y)
        self.draw() 

app = QApplication(sys.argv)
form = Form()
form.show()
app.exec_()
