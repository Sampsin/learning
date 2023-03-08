# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'c:\learning\python\pyqt\mouse_recorder\mouse_recorder.ui'
#
# Created by: PyQt5 UI code generator 5.15.4
#
# WARNING: Any manual changes made to this file will be lost when pyuic5 is
# run again.  Do not edit this file unless you know what you are doing.


from PyQt5 import QtCore, QtGui, QtWidgets


class Ui_MainWindow(object):
    def setupUi(self, MainWindow):
        MainWindow.setObjectName("MainWindow")
        MainWindow.resize(800, 400)
        self.centralwidget = QtWidgets.QWidget(MainWindow)
        self.centralwidget.setObjectName("centralwidget")
        self.doc_textBrowser = QtWidgets.QTextBrowser(self.centralwidget)
        self.doc_textBrowser.setGeometry(QtCore.QRect(40, 10, 391, 61))
        self.doc_textBrowser.setObjectName("doc_textBrowser")
        self.deleteFile_Btn = QtWidgets.QPushButton(self.centralwidget)
        self.deleteFile_Btn.setGeometry(QtCore.QRect(450, 50, 131, 21))
        self.deleteFile_Btn.setObjectName("deleteFile_Btn")
        self.file_tableWidget = QtWidgets.QTableWidget(self.centralwidget)
        self.file_tableWidget.setGeometry(QtCore.QRect(40, 90, 700, 300))
        self.file_tableWidget.setObjectName("file_tableWidget")
        self.file_tableWidget.setColumnCount(0)
        self.file_tableWidget.setRowCount(0)
        self.file_tableWidget.horizontalHeader().setCascadingSectionResizes(False)
        self.file_tableWidget.verticalHeader().setVisible(False)
        self.timeinterval_lineEdit = QtWidgets.QLineEdit(self.centralwidget)
        self.timeinterval_lineEdit.setGeometry(QtCore.QRect(460, 20, 113, 20))
        self.timeinterval_lineEdit.setObjectName("timeinterval_lineEdit")
        self.status_textEdit = QtWidgets.QTextEdit(self.centralwidget)
        self.status_textEdit.setGeometry(QtCore.QRect(600, 10, 141, 61))
        self.status_textEdit.setObjectName("status_textEdit")
        MainWindow.setCentralWidget(self.centralwidget)

        self.retranslateUi(MainWindow)
        QtCore.QMetaObject.connectSlotsByName(MainWindow)

    def retranslateUi(self, MainWindow):
        _translate = QtCore.QCoreApplication.translate
        MainWindow.setWindowTitle(_translate("MainWindow", "KeyHelper"))
        self.doc_textBrowser.setHtml(_translate("MainWindow", "<!DOCTYPE HTML PUBLIC \"-//W3C//DTD HTML 4.0//EN\" \"http://www.w3.org/TR/REC-html40/strict.dtd\">\n"
"<html><head><meta name=\"qrichtext\" content=\"1\" /><style type=\"text/css\">\n"
"p, li { white-space: pre-wrap; }\n"
"</style></head><body style=\" font-family:\'SimSun\'; font-size:9pt; font-weight:400; font-style:normal;\">\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">功能说明：</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">功能1.填入时间间隔（可以是小数），按F8鼠标左键连点当前位置。</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">功能2.按F9开始鼠标键盘录制，再按F9结束录制并保存在scripts目录下。</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">功能3.勾选录制文件，按F10进行录制回放。</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">功能4.默认加载当前目录下scripts目录的脚本(其他目录目前不支持)。</p>\n"
"<p style=\" margin-top:0px; margin-bottom:0px; margin-left:0px; margin-right:0px; -qt-block-indent:0; text-indent:0px;\">功能6.点击“删除录制文件”，可以将当前选中的文件删除。</p></body></html>"))
        self.deleteFile_Btn.setText(_translate("MainWindow", "删除录制文件"))