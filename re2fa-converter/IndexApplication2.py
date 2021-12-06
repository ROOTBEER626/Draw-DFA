from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *


from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.figure import Figure

import networkx as nx

from AutomataTheoryQt import *
import sys, time

class MainApp(QWidget):
    def __init__(self):
        super().__init__()
        layout = QVBoxLayout(self)
        self.setWindowTitle("RE2FA")
        self.centwijet = QWidget()
        self.lineedit = QLineEdit()
        self.ttletext = QLabel()
        self.pushbutn = QPushButton()
        self.titlebar = QWidget()
        self.textedit = QTextEdit()
        self.canvas = FigureCanvas(Figure(figsize=(3,3)))
        self.ax = self.canvas.figure.add_subplot(111)  
        layout.addWidget(self.centwijet)
        layout.addWidget(self.lineedit)
        layout.addWidget(self.ttletext)
        layout.addWidget(self.titlebar)
        layout.addWidget(self.textedit)
        layout.addWidget(self.pushbutn)
        layout.addWidget(self.canvas)
        self.getData()


    def getData(self):
        self.getFAinText()

    def getFAinText(self):
        self.textedit.setReadOnly(True)
        self.pushbutn.clicked.connect(self.compdata)
        return

    def getFAinGraph(self, InputRegularExpression):
        self.ax.clear() 
        nfaObject = NFAfromRegex(InputRegularExpression)
        nfa = nfaObject.getNFA()
        dfaObject = DFAfromNFA(nfa)
        G = dfaObject.drawDFA()
        #G = dfaObject.drawMinimisedDFA()
        #G = nfaObject.drawNFA()
        pos = nx.shell_layout(G)
        labels = nx.get_edge_attributes(G, "label")
        color_map = []
        #for node in G:
        #    if node is nfa.startstate:
        #        color_map.append('blue')
        #    if node in nfa.finalstates:
        #        color_map.append('red')
        #    else:
        #        color_map.append('green')
        nx.draw(
                G,
                pos,
                node_color='black',
                with_labels=True,
                edge_color="black",
                font_color="white",
                font_size=8,
                node_size=1000,
                node_shape="o",
                ax=self.ax,
            )
        nx.draw_networkx_edge_labels(G, pos, edge_labels=labels, ax=self.ax)
        self.ax.figure.canvas.draw()
        return


    def compdata(self):
        InputRegularExpression = self.lineedit.text()
        ReturnData = "<b> Started the Conversion</b>" + "<br/><i>" + time.ctime() + "</i><br/><br/>"
        try:
            ReturnData = ReturnData + "<i>Horizontal and vertical scrolling is supported</i><br/><br/>" + RegexComputation(InputRegularExpression)
        except BaseException as ExceptionEvent:
            ReturnData = ReturnData + "<b>Failure: </b>" + str(ExceptionEvent)
        Data = ReturnData + "<br/><br/>" + "<b>Stopped RE2FA conversion</b>" + "<br/>"
        self.textedit.setText(Data)
        self.getFAinGraph(InputRegularExpression)

def RegexComputation(InputRegularExpression):
    startTime = time.time()
    nfaObject = NFAfromRegex(InputRegularExpression)
    nfa = nfaObject.getNFA()
    dfaObject = DFAfromNFA(nfa)
    stopTime = time.time()
    TotalTime = stopTime - startTime
    actualData = "<b>Regular Expression: </b>" + str(InputRegularExpression) + "<br/>" + "<br/>" + \
                 "<b> Non-deterministic Finite Automata</b>" + "<br/" + nfaObject.displayNFA() + "br/>" + \
                 "<b>Deterministic Finite Automate</b>" + "<br/>" + dfaObject.displayDFA() + "<br/>" + \
                 "<b> Minimised Deterministic Finite Automata</b>" + "<br/>" + dfaObject.displayMinimisedDFA() + "<br/>" + \
                 "<b> Computation time: </b>" + str(TotalTime) + " seconds" + "<br/>"
    return(actualData)

def main():
    import sys

    app = QApplication([])

    window = MainApp()
    window.showMaximized()

    sys.exit(app.exec_())

if __name__ == "__main__":
    main()


