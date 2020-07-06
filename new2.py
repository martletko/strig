import sys
import time
import os
import csv

from PyQt4 import QtCore, QtGui
from PyQt4.QtCore import SIGNAL
from PyQt4.QtGui import QApplication, QMainWindow, QFont, QLineEdit, QFormLayout

from interFace2 import Ui_MainWindow

import datetime

import multiprocessing as mp


class MainWindow(QMainWindow, Ui_MainWindow):
    def __init__(self, parent=None, *args, **kwargs):
        QMainWindow.__init__(self)
        self.setupUi(self)

        logFolderName, ok = QtGui.QInputDialog.getText(self, "ввод логина", "введите логин для поиска", QtGui.QLineEdit.Normal)
        self.logPath = logFolderName

        self.Sort_Date.clicked.connect(self.on_Sort_Date_clicked)

        self.Sort_Login.clicked.connect(self.on_Sort_Login_clicked)

        self.Save_Button.clicked.connect(self.on_Save_Button_clicked)

        self.Clear_Button.clicked.connect(self.on_Clear_Button_clicked)

        self.Print_Button.clicked.connect(self.on_Print_Button_clicked)


    def on_Sort_Date_clicked(self):
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(0)
        logs = os.listdir(self.logPath)

        data = self.Date_And_Time.text()
        data = data.split(" ")
        date1 = data[0]
        minutes = data[1]
        date1 = date1.split(".")
        minutes = minutes.split(":")
        unix_time = int(datetime.datetime(int(date1[2]), int(date1[1]),int(date1[0]), int(minutes[0]), int(minutes[1]), int(minutes[2])).timestamp())
        unix_time += 36000
        unix_time = str(unix_time)
        print_data = []
        for log in logs:
            log_path = os.path.join(self.logPath, log)
            with open(log_path, "r") as fileInput:
                for row in csv.reader(fileInput):
                    if str(unix_time) in row: 
                        print_data.append(row)
        if print_data == []:
            pass
        else:
            self.tableWidget.setRowCount(len(print_data))
            self.tableWidget.setColumnCount(len(print_data[0]))
            for i in range(0, len(print_data)):
                tokens = print_data[i]
                for j in range(len(tokens)):
                    obj = QtGui.QTableWidgetItem(tokens[j])
                    self.tableWidget.setItem(i,j,obj)
            self.tableWidget.resizeColumnsToContents()

    def on_Sort_Login_clicked(self):
        text = self.Enter_Login.text()
        logs = os.listdir(self.logPath)
        print_data = []
        for log in logs:
            log_path = os.path.join(self.logPath, log)
            with open(log_path, "r") as fileInput:
                for row in csv.reader(fileInput):
                    if text in row:
                        print_data.append(row)
        if print_data == []:
            pass
        else:
            self.tableWidget.setRowCount(len(print_data))
            self.tableWidget.setColumnCount(len(print_data[0]))
            for i in range(0, len(print_data)):
                tokens = print_data[i]
                for j in range(len(tokens)):
                    obj = QtGui.QTableWidgetItem(tokens[j])
                    self.tableWidget.setItem(i,j,obj)
            self.tableWidget.resizeColumnsToContents()


    def on_Save_Button_clicked(self):
        number_of_rows = self.tableWidget.rowCount()
        number_of_columns = self.tableWidget.columnCount()
        fileName, ok = QtGui.QInputDialog.getText(self, "ввод ", "введите имя файла без расширения", QtGui.QLineEdit.Normal)
        fileName += '.csv'
        file_path = os.path.join(self.logPath, fileName)
        if number_of_rows == 0:
            pass
        else:
            for i in range(0,number_of_rows):
                row = []
                for j in range(0,number_of_columns):
                    tmp_item = self.tableWidget.item(i,j).text()
                    row.append(tmp_item)
                with open(fileName, 'a') as myFile:
                    myWriter = csv.writer(myFile, delimiter=',')
                    myWriter.writerow(row)


    def on_Print_Button_clicked(self):
        num_of_page = self.PageLineEdit.text()
        try:
            num = int(num_of_page)
            logs = os.listdir(self.logPath)
            print_data = []
            for log in logs:
                log_path = os.path.join(self.logPath, log)
                with open(log_path, "r") as fileInput:
                    for row in csv.reader(fileInput):
                        print_data.append(row)
            
            hundred = []
            for i in range((num-1)*100, num*100, 1):
                try:
                    hundred.append(print_data[i])
                except IndexError:
                    pass
            for j in range(len(hundred)):
                self.tableWidget.setRowCount(len(hundred))
                self.tableWidget.setColumnCount(len(hundred[0]))
                tokens = hundred[j]
                for k in range(0, len(tokens)):
                    obj = QtGui.QTableWidgetItem(tokens[k])
                    self.tableWidget.setItem(j,k,obj)
            


        except TypeError:
            pass

    def on_Clear_Button_clicked(self):
        self.tableWidget.setRowCount(0)
        self.tableWidget.setColumnCount(0)



def main():
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == "__main__":
    main()    