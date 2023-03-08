import sys
import os
import time
import json
from PyQt5.QtCore import Qt, QObject, QThread, pyqtSignal
from PyQt5.QtWidgets import QApplication, QMainWindow, QCheckBox, QTableWidgetItem, QFileDialog
from Ui_mouse_recorder import *
from my_recorder import *

class MyWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None):
        super(MyWindow, self).__init__(parent)
        self.__cur_checkbox = None
        self.__filelist = []
        self.__curfilepath = []
        self.setupUi(self)
        self.inittable()
        self.getscripts()
        self.timeinterval_lineEdit.setPlaceholderText("请输入点击间隔（秒）：")
        self.deleteFile_Btn.clicked.connect(self.deletefile)
        self.recorder = MyRecorder(self)
        self.recorder.refresh.connect(self.refresh_file_list)
        self.recorder.minimized.connect(self.minimized_window)
        self.recorder.active.connect(self.active_window)
        self.recorder.savefile.connect(self.savefile)
        self.recorder.showstatus.connect(self.showstatus)

    def inittable(self):
        # set row and column
        self.file_tableWidget.setColumnCount(3)
        self.file_tableWidget.setRowCount(1)
        self.file_tableWidget.setColumnWidth(0, 50)
        self.file_tableWidget.setColumnWidth(1, 325)
        self.file_tableWidget.setColumnWidth(2, 325)
        # set data title
        self.file_tableWidget.horizontalHeader().setStyleSheet("QHeaderView::section{background:skyblue;}")
        self.file_tableWidget.setHorizontalHeaderItem(0, QTableWidgetItem("序号"))
        self.file_tableWidget.setHorizontalHeaderItem(1, QTableWidgetItem("文件名"))
        self.file_tableWidget.setHorizontalHeaderItem(2, QTableWidgetItem("修改时间"))
        self.file_tableWidget.horizontalHeader().setStretchLastSection(True)
        
        # setting
        self.file_tableWidget.setEditTriggers(QtWidgets.QAbstractItemView.EditTrigger.NoEditTriggers)


    def getscripts(self):
        scriptspath = self.get_scripts_path()
        if not os.path.exists(scriptspath):
            os.makedirs(scriptspath)
        if self.__filelist==[]: #file list is [], reinit file list
            for file in os.listdir(scriptspath):
                if file.endswith(".json"):
                    self.__filelist.append(file)
        row_num = len(self.__filelist)
        self.file_tableWidget.setRowCount(row_num)
        # set data items
        for row in range(row_num):
            # first column is checkbox
            item_checked = QCheckBox(parent=self.file_tableWidget)
            item_checked.setText(str(row + 1))
            item_checked.setCheckState(Qt.Unchecked)
            item_checked.clicked.connect(self.table_item_clicked)
            self.file_tableWidget.setCellWidget(row, 0, item_checked)
            # second column is filename
            item_name = QTableWidgetItem(self.__filelist[row])
            item_name.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.file_tableWidget.setItem(row, 1, item_name)
            # third column is modification time
            filepath = os.path.join(scriptspath, self.__filelist[row])
            mtime = os.stat(filepath).st_mtime
            mtime_str = time.strftime('%Y_%m_%d %H:%M:%S', time.localtime(mtime))
            item_time = QTableWidgetItem(mtime_str)
            item_time.setTextAlignment(Qt.AlignHCenter | Qt.AlignVCenter)
            self.file_tableWidget.setItem(row, 2, item_time)

    def refresh_file_list(self, file):
        #if file do not exist
        if not file in self.__filelist:  
            self.__filelist.append(file)
        self.getscripts()

    def deletefile(self):
        ix = self.file_tableWidget.indexAt(self.__cur_checkbox.pos())
        file = self.__filelist[ix.row()]
        scriptpath = self.get_scripts_path()
        filepath = scriptpath + file
        print("delete file", filepath)
        os.remove(filepath)
        self.__filelist.remove(file)
        self.getscripts()


    def get_scripts_path(self):
        #get current path
        cwdpath = os.getcwd()
        print("current path" + cwdpath)
        #create or enter scripts path
        scriptspath = cwdpath + "\scripts\\"
        print("scripts path" + scriptspath)
        return scriptspath

    # when select one check box，others should be not selected, everytime we only delete/excute one file
    def table_item_clicked(self):
        check_box = self.sender()
        ix = self.file_tableWidget.indexAt(check_box.pos())
        num = self.file_tableWidget.rowCount()
        print("check box number:", num)
        print(ix.row(), ix.column(), check_box.isChecked())
        self.__cur_checkbox = check_box
        file = self.__filelist[ix.row()]
        scriptpath = self.get_scripts_path()
        self.__curfilepath = scriptpath + file
        if check_box.isChecked() == True:
            for i in range(num):
                if i != ix.row():
                    ch = self.file_tableWidget.cellWidget(i,0)
                    ch.setCheckState(Qt.Unchecked)

    def get_current_filepath(self):
        return self.__curfilepath
    
    def minimized_window(self):
        self.setWindowState(Qt.WindowMinimized)
    
    def active_window(self):
        self.setWindowState(Qt.WindowActive)

    def savefile(self):
        path = self.get_scripts_path()
        filepath = QFileDialog.getSaveFileName(self, "保存文件", path, "json(*.json)")
        print("save file path", filepath[0])
        filename = os.path.basename(filepath[0])
        command_list = self.recorder.getcommandlist()
        self.tofile(command_list, filepath[0])
        self.refresh_file_list(filename)

    def tofile(self, commandlist, path):
        with open(path, "w") as f:
            f.write(json.dumps(commandlist))    #使用json格式写入

    def showstatus(self, str):
        self.status_textEdit.setText(str)
        

if __name__ == '__main__':
    app = QApplication(sys.argv)
    myWin = MyWindow()
    myWin.show()
    sys.exit(app.exec_())