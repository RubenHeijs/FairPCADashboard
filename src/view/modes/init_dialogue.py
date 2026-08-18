from PySide6.QtWidgets import *
from PySide6.QtCore import Qt
from src.view.scatter.scatter_2d import *
from PySide6.QtCore import Slot
import pandas as pd
import numpy as np

class InitDialogue(QWidget):

    def __init__(self, process_decision,parent=None):
        super().__init__(parent)
        self.process_decision = process_decision
        self.df = None
        manual_data_layout = QHBoxLayout()
        line = QFrame()
        line.setFrameShape(QFrame.VLine)       # vertical line (for HBox)
        line.setFrameShadow(QFrame.Sunken)     # gives it a subtle 3D groove look
        line.setLineWidth(1)

        manual_layout = QGridLayout()
        data_layout = QGridLayout()
        rows, cols = 7, 3


        manual_layout.addWidget(QLabel('Manual'),0,0,1,cols,alignment=Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignHCenter)
        pb_2 = QPushButton('Two Features')
        pb_2.clicked.connect(self.manual_two)
        pb_3 = QPushButton('Three Features')
        pb_3.clicked.connect(self.manual_three)
        manual_layout.addWidget(pb_2,2,1,alignment=Qt.AlignmentFlag.AlignCenter)
        manual_layout.addWidget(pb_3,4,1,alignment=Qt.AlignmentFlag.AlignCenter)


        data_layout.addWidget(QLabel('Static Data'),0,0,1,cols,alignment=Qt.AlignmentFlag.AlignTop|Qt.AlignmentFlag.AlignHCenter)


        file_select_btn = QPushButton('Select File')
        file_select_btn.clicked.connect(self.file_select_btn_click)
        data_layout.addWidget(file_select_btn,1,0)
        self.file_tb = QLineEdit('no file selected')
        data_layout.addWidget(self.file_tb,1,1)
        file_process_btn = QPushButton('Process')
        file_process_btn.clicked.connect(self.process_btn_click)
        data_layout.addWidget(file_process_btn,1,2)

    

        self.s_f_label = QLabel('Sensitive feature')
        data_layout.addWidget(self.s_f_label,2,0,alignment=Qt.AlignmentFlag.AlignVCenter|Qt.AlignmentFlag.AlignRight)
        self.s_f_cb = QComboBox()
        self.s_f_cb.currentIndexChanged.connect(self.check_valid)
        data_layout.addWidget(self.s_f_cb,2,1)

        self.f_1_label = QLabel('First feature')
        data_layout.addWidget(self.f_1_label,3,0,alignment=Qt.AlignmentFlag.AlignVCenter|Qt.AlignmentFlag.AlignRight)
        self.f_1_cb = QComboBox()
        self.f_1_cb.currentIndexChanged.connect(self.check_valid)
        data_layout.addWidget(self.f_1_cb,3,1)

        self.f_2_label = QLabel('Second feature')
        data_layout.addWidget(self.f_2_label,4,0,alignment=Qt.AlignmentFlag.AlignVCenter|Qt.AlignmentFlag.AlignRight)
        self.f_2_cb = QComboBox()
        self.f_2_cb.currentIndexChanged.connect(self.check_valid)
        data_layout.addWidget(self.f_2_cb,4,1)

        self.f_3_label = QLabel('(Optional) Third feature')
        data_layout.addWidget(self.f_3_label,5,0,alignment=Qt.AlignmentFlag.AlignVCenter|Qt.AlignmentFlag.AlignRight)
        self.f_3_cb = QComboBox()
        self.f_3_cb.currentIndexChanged.connect(self.check_valid)
        data_layout.addWidget(self.f_3_cb,5,1)


        self.warning_label = QLabel('')
        data_layout.addWidget(self.warning_label,rows-1,0,1,cols-1,alignment=Qt.AlignmentFlag.AlignVCenter|Qt.AlignmentFlag.AlignRight)

        self.start_btn = QPushButton('Start')
        self.start_btn.clicked.connect(self.data_send)
        data_layout.addWidget(self.start_btn,rows-1,cols-1)

        manual_data_layout.addLayout(manual_layout)
        manual_data_layout.addWidget(line)
        manual_data_layout.addLayout(data_layout)
        for c in range(cols):
            data_layout.setColumnStretch(c,1)
            if(c==1):
                data_layout.setColumnStretch(c,2)
            for r in range(rows):
                manual_layout.addItem(QSpacerItem(1, 0, QSizePolicy.Expanding, QSizePolicy.Expanding), r, c)
                data_layout.addItem(QSpacerItem(1, 0, QSizePolicy.Expanding, QSizePolicy.Expanding), r, c)

        manual_data_layout.setStretch(0,1)
        manual_data_layout.setStretch(2,2)
        self.setLayout(manual_data_layout)
        self.set_to_no_data()


    @Slot()
    def file_select_btn_click(self):
        fd = QFileDialog()
        self.file_tb.setText( fd.getOpenFileName(filter='*.csv')[0])
        
    @Slot()
    def process_btn_click(self):
        self.set_to_no_data()
        print('start processing')
        file = self.file_tb.displayText()
        print(file)
        try:
            self.df = pd.read_csv(file)
            if len(self.df.columns)<=3:
                self.warning_label.setText('File does not contain enough features (>2)')
                return
        except FileNotFoundError:
            self.warning_label.setText('Could not find the file')
            return
        except Exception as e :
            #self.f_1_label.setText(str(e))
            print(type(e))
            return
        self.groups = []
        for col in self.df.columns:
            self.groups.append(self.df[col].unique())
        self.init_data_selection()

    def set_to_no_data(self):
        for i in range(self.f_3_cb.count()):
            print(i, self.f_3_cb.itemData(i))
            self.s_f_cb.removeItem(0)
            self.f_1_cb.removeItem(0)
            self.f_2_cb.removeItem(0)
            self.f_3_cb.removeItem(0)

        self.s_f_cb.setVisible(False)
        self.f_1_cb.setVisible(False)
        self.f_2_cb.setVisible(False)
        self.f_3_cb.setVisible(False)

        self.s_f_label.setVisible(False)
        self.f_1_label.setVisible(False)
        self.f_2_label.setVisible(False)
        self.f_3_label.setVisible(False)
        self.warning_label.setText('Upload a file')
        self.start_btn.setEnabled(False)

    def init_data_selection(self):
        self.s_f_cb.addItems(self.df.columns)
        self.s_f_cb.setCurrentIndex( np.argmin([len(group) for group in self.groups]))
        self.s_f_cb.setVisible(True)
        self.s_f_label.setVisible(True)

        self.f_1_cb.addItems(self.df.columns)
        self.f_1_cb.setCurrentIndex(0)
        self.f_1_cb.setVisible(True)
        self.f_1_label.setVisible(True)

        self.f_2_cb.addItems(self.df.columns)
        self.f_2_cb.setCurrentIndex(1)
        self.f_2_cb.setVisible(True)
        self.f_2_label.setVisible(True)

        if len(self.df.columns)>=4:
            self.f_3_cb.addItems(self.df.columns)
            self.f_3_cb.addItem('None')
            self.f_3_cb.setCurrentIndex(len(self.df.columns))
            self.f_3_cb.setVisible(True)
            self.f_3_label.setVisible(True)
        self.check_valid()
        
    @Slot()
    def check_valid(self):
        selected = [self.f_1_cb.currentIndex(), self.f_2_cb.currentIndex(), self.f_3_cb.currentIndex(),self.s_f_cb.currentIndex()]
        if len(np.unique(selected))<len(selected):
            self.warning_label.setText('Select a different feature for each option')
            self.start_btn.setEnabled(False)
        else:
            self.warning_label.setText('')
            self.start_btn.setEnabled(True)


    @Slot()
    def manual_two(self):
        print('Manual with two features')
        self.process_decision(self,0)
    @Slot()
    def manual_three(self):
        print('Manual with three features')
        self.process_decision(self,1)
    @Slot()
    def data_send(self):
        sensitive_feature = self.df.columns[self.s_f_cb.currentIndex()]
        mode = 2
        features = [                
            self.df.columns[self.f_1_cb.currentIndex()],
            self.df.columns[self.f_2_cb.currentIndex()]
        ]
        if(self.f_3_cb.isVisible() and self.f_3_cb.currentIndex() < len(self.df.columns)): #2d
            features.append(self.df.columns[self.f_3_cb.currentIndex()])                
            mode = 3
        self.process_decision(self,mode,self.df, sensitive_feature,features)