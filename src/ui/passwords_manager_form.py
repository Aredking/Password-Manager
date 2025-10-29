from PyQt6 import QtCore, QtGui, QtWidgets


class Ui_Form(object):
    def setupUi(self, Form):
        Form.setObjectName("Form")
        Form.resize(800, 600)
        self.verticalLayout = QtWidgets.QVBoxLayout(Form)
        self.verticalLayout.setContentsMargins(20, 20, 20, 20)
        self.verticalLayout.setObjectName("verticalLayout")
        self.listWidget = QtWidgets.QListWidget(parent=Form)
        self.listWidget.setFocusPolicy(QtCore.Qt.FocusPolicy.NoFocus)
        self.listWidget.setObjectName("listWidget")
        self.verticalLayout.addWidget(self.listWidget)
        self.horizontalLayout = QtWidgets.QHBoxLayout()
        self.horizontalLayout.setSpacing(5)
        self.horizontalLayout.setObjectName("horizontalLayout")
        self.add_btn = QtWidgets.QPushButton(parent=Form)
        sizePolicy = QtWidgets.QSizePolicy(QtWidgets.QSizePolicy.Policy.Fixed, QtWidgets.QSizePolicy.Policy.Fixed)
        sizePolicy.setHorizontalStretch(0)
        sizePolicy.setVerticalStretch(0)
        sizePolicy.setHeightForWidth(self.add_btn.sizePolicy().hasHeightForWidth())
        self.add_btn.setSizePolicy(sizePolicy)
        font = QtGui.QFont()
        font.setFamily("Arial")
        font.setPointSize(14)
        self.add_btn.setFont(font)
        self.add_btn.setFocusPolicy(QtCore.Qt.FocusPolicy.WheelFocus)
        self.add_btn.setLayoutDirection(QtCore.Qt.LayoutDirection.LeftToRight)
        self.add_btn.setObjectName("add_btn")
        self.horizontalLayout.addWidget(self.add_btn)
        self.verticalLayout.addLayout(self.horizontalLayout)

        self.retranslateUi(Form)
        QtCore.QMetaObject.connectSlotsByName(Form)

    def retranslateUi(self, Form):
        _translate = QtCore.QCoreApplication.translate
        Form.setWindowTitle(_translate("Form", "Form"))
        self.add_btn.setText(_translate("Form", "Добавить пароль (+)"))


class PasswordsManagerForm(QtWidgets.QWidget, Ui_Form):
    def __init__(self, main_window):
        from src.ui.main import MainWindow
        super().__init__()
        self.setupUi(self)

        self.main_window: MainWindow = main_window
