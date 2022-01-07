
from PyQt5 import  QtWidgets
from PyQt5 import QtGui
from PyQt5.QtWidgets import QFileDialog 
from views.main import Ui_MainWindow
from PyQt5.QtCore import *
from PyQt5.QtGui import *
from PyQt5.QtWidgets import *
from models.operationListModel import *
from models.parser import *
from models.operators import *
from models.configuration import *
import logging
import webbrowser
import threading, time
class MainWindowModel(Ui_MainWindow):
    global_input_text : str = ""
    def __init__(self):
        self.log = logging.getLogger()
        pass

    def init(self):
        self.actionOpen_File.triggered.connect(self.open_file)
        self.actionSave_Parsed_File.triggered.connect(self.save_parsed_file)
        self.actionSave_Configuration.triggered.connect(self.save_config)
        self.actionOpen_Configuration.triggered.connect(self.load_config)
        self.actionHelp_regex_test_app.triggered.connect(self.help_open_regex_test_app)

        self.textPatternFind.textChanged.connect(self.patterns_changed)
        self.textPatternReplace.textChanged.connect(self.patterns_changed)
        self.pushButtonAdd.clicked.connect(self.add_operation_to_list)
        self.pushButtonDeleteFromList.clicked.connect(self.remove_operation)
        self.listView.clicked.connect(self.display_sequenced_operation)
        self.pushButtonNewOperation.clicked.connect(self.new_operation)
        self.init_combobox_ops()
        self.list_model = OperationListModel()        

    def display_sequenced_operation(self):
        ids = self.listView.selectedIndexes()
        if ids:
            id = ids[0].row()
            self.update_displayed_parsed(id)

        pass

    def help_open_regex_test_app(self):
        webbrowser.open_new_tab("https://regexr.com/")
    
    def save_parsed_file(self):
        ops = [ i.op for i in self.list_model.items]
        if len(ops) <= 0:
            self.plainTextOutput.clear()
            self.update_text_view(self.global_input_text)
            return
        op_sequencer = Parser(ops)
        results = op_sequencer.apply(self.global_input_text)
        parsing = results[-1].output

        filename = QFileDialog.getSaveFileName(None, caption='Save File')
        if len(filename[0]) > 0:
            f = open(filename[0], 'w')
            with f:
                if len(self.lineEditHeader.text()) > 0:
                    lines = [self.lineEditHeader.text() + "\n",  parsing]
                else:
                    lines = [parsing]
                f.writelines(lines)
        pass

    def new_operation(self):
        self.update_displayed_parsed_for_new_operation()
        self.textPatternReplace.clear()
        self.textPatternFind.clear()
        self.plainTextOutput.clear()
        
        for w in [self.textPatternReplace, self.textPatternFind, self.pushButtonAdd]:
            w.setEnabled(True)
        pass

    def init_combobox_ops(self):
        for t in OperatorType:
            self.comboBoxOperations.addItem(t)
        self.comboBoxOperations.currentTextChanged.connect(self.operation_changed)

    def remove_operation(self):
        ids = self.listView.selectedIndexes()
        if ids:
            for i in ids:
                self.list_model.delete(i.row())
            self.update_displayed_parsed()


    def update_displayed_parsed_for_new_operation(self):
        ops = [ i.op for i in self.list_model.items]
        if len(ops) >= 1:
            op_sequencer = Parser(ops)
            final_resut = op_sequencer.apply(self.global_input_text)
            self.update_text_view(final_resut[-1].output)
            self.plainTextOutput.clear()
        else:
            self.plainTextOutput.clear()
            self.update_text_view(self.global_input_text)
        pass

    def update_displayed_parsed(self, up_to_index:int=-1):
        ops = [ i.op for i in self.list_model.items]
        if len(ops) <= 0:
            self.plainTextOutput.clear()
            self.update_text_view(self.global_input_text)
            return
        op_sequencer = Parser(ops)
        results = op_sequencer.apply(self.global_input_text)
        parsing = results[up_to_index]
        self.update_text_view(parsing.input)
        self.plainTextOutput.setPlainText(parsing.output)
        self.comboBoxOperations.setCurrentText(parsing.op.type.value)
        
        self.textPatternReplace.clear()
        self.textPatternFind.clear()
        self.textPatternFind.setEnabled(True)
        op = parsing.op
        self.textPatternFind.setPlainText(op.pattern)
        if op.type == OperatorType.FIND:
            self.textPatternReplace.setEnabled(False)
        elif op.type == OperatorType.REPLACE:
            self.textPatternReplace.setEnabled(True)
            self.textPatternReplace.setPlainText(op.replace)
        else:
            self.log.error("Operation type {} not handled.".format(id))
        pass
        for w in [self.textPatternReplace, self.textPatternFind, self.pushButtonAdd]:
            w.setEnabled(False)

    def open_file(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)

        if dlg.exec_():
            filenames = dlg.selectedFiles()
            f = open(filenames[0], 'r')
            
            with f:
                data = f.read()
                self.update_text_view(data)
                self.global_input_text = data
                self.plainTextGlobalInput.setPlainText(data)
                self.pushButtonAdd.setEnabled(True)
            self.comboBoxOperations.setEnabled(True)
            self.operation_changed(self.comboBoxOperations.currentText()) 
            self.update_displayed_parsed()

    def update_text_view(self, input_text:str):
        self.plainTextOperatorInput.setPlainText(input_text)

    def operation_changed(self, id:str):
        self.textPatternReplace.clear()
        self.textPatternFind.clear()
        self.plainTextOutput.clear()
        self.update_displayed_parsed_for_new_operation()
        self.textPatternFind.setEnabled(True)
        if id == OperatorType.FIND:
            self.textPatternReplace.setEnabled(False)
        elif id == OperatorType.REPLACE:
            self.textPatternReplace.setEnabled(True)
        else:
            self.log.error("Operation type {} not handled.".format(id))

    def patterns_changed(self):
        pattern = self.textPatternFind.toPlainText()
        id = self.comboBoxOperations.currentText()
        self.apply_operator(self.get_operator())
        
    def get_operator(self):
        pattern = self.textPatternFind.toPlainText()
        id = self.comboBoxOperations.currentText()
        if id == OperatorType.FIND:
            return OperatorFind(pattern)
        elif id == OperatorType.REPLACE:
            return OperatorReplace(pattern, self.textPatternReplace.toPlainText())
        else:
            self.log.error("Operation type {} not handled.".format(id))
            return None

    def apply_operator(self, op:Operator):
        parsed_text = op.apply(self.plainTextOperatorInput.toPlainText())
        if parsed_text:
            self.plainTextOutput.setPlainText(parsed_text)
        else:
            self.plainTextOutput.clear()

    def get_current_input_output_text(self):
        return self.plainTextOperatorInput.toPlainText(), self.plainTextOutput.toPlainText()

    def add_operation_to_list(self):
        #item = QStandardItem(self.get_operator())
        input, output = self.get_current_input_output_text()
        
        self.list_model.add(ParsingItem(self.get_operator(), input, output))
        self.listView.setModel(self.list_model)
        self.textPatternFind.clear()
        self.textPatternReplace.clear()
        self.update_displayed_parsed_for_new_operation()
        pass

    def apply_listed_operations(self):
        pass

    def get_list_operations(self):        
        pass

    def save_config(self):
        ops = [ i.op for i in self.list_model.items]
        if len(ops) <= 0:
            return

        filename = QFileDialog.getSaveFileName(None, caption='Save File')
        if len(filename[0]) > 0:
            config = ConfigurationJson.from_operations(ops)
            config.set_header(self.lineEditHeader.text())
            config.write(filename[0])

    def load_config(self):
        dlg = QFileDialog()
        dlg.setFileMode(QFileDialog.AnyFile)

        if dlg.exec_():
            filenames = dlg.selectedFiles()
            config, ok = ConfigurationJson.from_file(filenames[0])
            try:
                if ok:
                    op_sequencer = Parser(config.to_operations())
                    parsings = op_sequencer.apply(self.global_input_text)
                    self.list_model.clear()
                    for p in parsings:
                        self.list_model.add(p)
                    self.listView.setModel(self.list_model)
                    self.update_text_view(parsings[-1].input)
                    self.plainTextOutput.setPlainText(parsings[-1].output)
                    self.comboBoxOperations.setCurrentText(parsings[-1].op.type.value)
                    self.textPatternReplace.clear()
                    self.textPatternFind.clear()
                    self.lineEditHeader.setText(config["header"])
            except Exception as e:
                self.log.error("Error parsing the configuration file")
                ok = False

            if not ok:
                msg = QMessageBox()
                msg.setText("Error loading configuration file {}.".format(filenames[0]))
                msg.setWindowTitle( "Error")
                msg.setIcon(QMessageBox.Warning)
                msg.setStandardButtons(QMessageBox.Ok) 
                msg.show()
                msg.exec_()
                return

if __name__ == "__main__":
    import sys
    app = QtWidgets.QApplication(sys.argv)

    try:
        # reference: https://github.com/5yutan5/PyQtDarkTheme
        import qdarktheme
        app.setStyleSheet(qdarktheme.load_stylesheet())
    except:
        pass
    MainWindow = QtWidgets.QMainWindow()
    ui = MainWindowModel()
    ui.setupUi(MainWindow)
    ui.init()
    MainWindow.show()
    sys.exit(app.exec_())