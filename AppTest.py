import sys

sys.path.append('./Controller')
sys.path.append('./Model')

from PyQt5.QtWidgets import (

    QApplication, QDialog, QMainWindow, QMessageBox

)

from PyQt5.uic import loadUi


from main_window_controller import Ui_MainWindow

from price_predictions_in_ecommercewish import price_model

#from model import ImageModel
#from model import PricePredictionModel


class Window(QMainWindow, Ui_MainWindow):

    def __init__(self, parent=None):

        super().__init__(parent)

        self.setupUi(self)

        self.label.setText("Hola Que hace")

        self.pushButton.clicked.connect(self.say_hello)

        #self.connectSignalsSlots()

    
    def say_hello(one, two):

        one.label.setText(one.textEdit.toPlainText())
        print("Button clicked, Hello!")

    def connectSignalsSlots(self):

        self.action_Exit.triggered.connect(self.close)

        self.action_Find_Replace.triggered.connect(self.findAndReplace)

        self.action_About.triggered.connect(self.about)


    def findAndReplace(self):

        dialog = FindReplaceDialog(self)

        dialog.exec()


    def about(self):

        QMessageBox.about(

            self,

            "About Sample Editor",

            "<p>A sample text editor app built with:</p>"

            "<p>- PyQt</p>"

            "<p>- Qt Designer</p>"

            "<p>- Python</p>",

        )


class FindReplaceDialog(QDialog):

    def __init__(self, parent=None):

        super().__init__(parent)

        loadUi("ui/find_replace.ui", self)


if __name__ == "__main__":

    price_model.execute()

    app = QApplication(sys.argv)

    win = Window()

    win.show()

    sys.exit(app.exec())