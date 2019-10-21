# -*- coding: utf-8 -*-

# Form implementation generated from reading ui file 'addMatch.ui'
#
# Created by: PyQt5 UI code generator 5.9.2
#
# WARNING! All changes made in this file will be lost!

from PyQt5 import QtCore, QtGui, QtWidgets


import MySQLdb as mdb


try:
	db = mdb.connect('localhost', 'root', 'divpes1998', 'TOURNAMENT')
	print("database connected")
	cur=db.cursor()
except mdb.Error as e:
	QMessageBox.about(self, 'Connection', 'Failed To Connect Database')
	sys.exit(1)

tuple_team_row=cur.execute("SELECT DISP_NAME FROM TEAM")
tuple_team_data=cur.fetchall()
list_team_data=list(tuple_team_data)
	

	

class Ui_Form(object):
	def on_click_addMatch(self):
		over=self.oversSpinBox.value()
		team1=self.team1ComboBox.currentText()
		team2=self.team2ComboBox.currentText()
		date=self.dateEdit.text()
		time=self.timeEdit.text()
		print(date)
		print(time)
		cur.execute("INSERT INTO ADDMATCH (HOST_TEAM,OPP_TEAM,MATCH_DATE,MATCH_TIME,OVERS) VALUES('%s','%s','%s','%s','%s')"%(team1,team2,date,time,over))
		db.commit()
		#self.init_upcoming_match()
		self.dateEdit.clear()
		self.timeEdit.clear()


	def setupUi(self, Form):
		Form.setObjectName("Form")
		Form.resize(472, 266)
		Form.setStyleSheet("background-color: rgb(136, 138, 133);")
		self.layoutWidget = QtWidgets.QWidget(Form)
		self.layoutWidget.setGeometry(QtCore.QRect(10, 10, 451, 246))
		self.layoutWidget.setObjectName("layoutWidget")
		self.gridLayout = QtWidgets.QGridLayout(self.layoutWidget)
		self.gridLayout.setContentsMargins(0, 0, 0, 0)
		self.gridLayout.setObjectName("gridLayout")
		self.addMatchLabel = QtWidgets.QLabel(self.layoutWidget)
		sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Expanding, QtWidgets.QSizePolicy.Preferred)
		sizePolicy.setHorizontalStretch(0)
		sizePolicy.setVerticalStretch(1)
		sizePolicy.setHeightForWidth(self.addMatchLabel.sizePolicy().hasHeightForWidth())
		self.addMatchLabel.setSizePolicy(sizePolicy)
		self.addMatchLabel.setMaximumSize(QtCore.QSize(134, 16777215))
		font = QtGui.QFont()
		font.setPointSize(17)
		font.setBold(True)
		font.setWeight(75)
		self.addMatchLabel.setFont(font)
		self.addMatchLabel.setAlignment(QtCore.Qt.AlignCenter)
		self.addMatchLabel.setObjectName("addMatchLabel")
		self.gridLayout.addWidget(self.addMatchLabel, 0, 0, 1, 1, QtCore.Qt.AlignHCenter)
		self.addMatchForm = QtWidgets.QFormLayout()
		self.addMatchForm.setObjectName("addMatchForm")
		self.team1NameLabel = QtWidgets.QLabel(self.layoutWidget)
		self.team1NameLabel.setObjectName("team1NameLabel")
		self.addMatchForm.setWidget(0, QtWidgets.QFormLayout.LabelRole, self.team1NameLabel)
		self.team1ComboBox = QtWidgets.QComboBox(self.layoutWidget)
		self.team1ComboBox.setObjectName("team1ComboBox")
		#list1=['abc','def','ghi','lkg','bnm']
		for ele in list_team_data:
			for strr in ele:
				self.team1ComboBox.addItem(strr)
		self.addMatchForm.setWidget(0, QtWidgets.QFormLayout.FieldRole, self.team1ComboBox)
		self.team2NameLabel = QtWidgets.QLabel(self.layoutWidget)
		self.team2NameLabel.setObjectName("team2NameLabel")
		self.addMatchForm.setWidget(1, QtWidgets.QFormLayout.LabelRole, self.team2NameLabel)
		self.team2ComboBox = QtWidgets.QComboBox(self.layoutWidget)
		self.team2ComboBox.setObjectName("team2ComboBox")
		for ele in list_team_data:
			for strr in ele:
				self.team2ComboBox.addItem(strr)
		self.addMatchForm.setWidget(1, QtWidgets.QFormLayout.FieldRole, self.team2ComboBox)
		self.dateLabel = QtWidgets.QLabel(self.layoutWidget)
		self.dateLabel.setObjectName("dateLabel")
		self.addMatchForm.setWidget(2, QtWidgets.QFormLayout.LabelRole, self.dateLabel)
		self.dateEdit = QtWidgets.QDateEdit(self.layoutWidget)
		self.dateEdit.setObjectName("dateEdit")
		self.addMatchForm.setWidget(2, QtWidgets.QFormLayout.FieldRole, self.dateEdit)
		self.timeLabel = QtWidgets.QLabel(self.layoutWidget)
		self.timeLabel.setObjectName("timeLabel")
		self.addMatchForm.setWidget(3, QtWidgets.QFormLayout.LabelRole, self.timeLabel)
		self.timeEdit = QtWidgets.QTimeEdit(self.layoutWidget)
		self.timeEdit.setObjectName("timeEdit")
		self.addMatchForm.setWidget(3, QtWidgets.QFormLayout.FieldRole, self.timeEdit)
		self.oversLabel = QtWidgets.QLabel(self.layoutWidget)
		self.oversLabel.setObjectName("oversLabel")
		self.addMatchForm.setWidget(4, QtWidgets.QFormLayout.LabelRole, self.oversLabel)
		self.oversSpinBox = QtWidgets.QSpinBox(self.layoutWidget)
		self.oversSpinBox.setMinimum(10)
		self.oversSpinBox.setMaximum(50)
		self.oversSpinBox.setProperty("value", 20)
		self.oversSpinBox.setObjectName("oversSpinBox")
		self.addMatchForm.setWidget(4, QtWidgets.QFormLayout.FieldRole, self.oversSpinBox)
		self.gridLayout.addLayout(self.addMatchForm, 1, 0, 1, 1)
		self.addMatchButton = QtWidgets.QPushButton(self.layoutWidget)
		self.addMatchButton.setObjectName("addMatchButton")
		self.gridLayout.addWidget(self.addMatchButton, 2, 0, 1, 1)
		self.gridLayout.setRowStretch(0, 1)
		self.gridLayout.setRowStretch(1, 3)
		self.gridLayout.setRowStretch(2, 1)

		
		#added by divyam
		self.addMatchButton.clicked.connect(self.on_click_addMatch)
		self.retranslateUi(Form)
		QtCore.QMetaObject.connectSlotsByName(Form)

	def retranslateUi(self, Form):
		_translate = QtCore.QCoreApplication.translate
		Form.setWindowTitle(_translate("Form", "Form"))
		self.addMatchLabel.setText(_translate("Form", "Add Match"))
		self.team1NameLabel.setText(_translate("Form", "Team1 Name"))
		self.team2NameLabel.setText(_translate("Form", "Team2 Name"))
		self.dateLabel.setText(_translate("Form", "Date"))
		self.timeLabel.setText(_translate("Form", "Time"))
		self.oversLabel.setText(_translate("Form", "Overs"))
		self.addMatchButton.setText(_translate("Form", "Add Match"))


if __name__ == "__main__":
	import sys
	app = QtWidgets.QApplication(sys.argv)
	Form = QtWidgets.QWidget()
	ui = Ui_Form()
	ui.setupUi(Form)
	Form.show()
	sys.exit(app.exec_())

