## -*- coding: utf-8 -*-
"""
Created on Tue 27 Oct 2020

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License. You may obtain a copy of the
License at
http://www.apache.org/licenses/LICENSE-2.0

Unless required by applicable law or agreed to in writing, software distributed
under the License is distributed on an "AS IS" BASIS, WITHOUT WARRANTIES OR
CONDITIONS OF ANY KIND, either express or implied. See the License for the
specific language governing permissions and limitations under the License.

This work was funded by Joanna Leng's EPSRC funded RSE Fellowship (EP/R025819/1)

@copyright 2020
@author: j.h.pickering@leeds.ac.uk and j.leng@leeds.ac.uk
"""
# set up linting conditions
# pylint: disable = too-many-public-methods
# pylint: disable = c-extension-no-member

import PyQt5.QtWidgets as qw
import PyQt5.QtCore as qc

from imagedraw.gui.Ui_imagedrawmainwindow import Ui_ImageDrawMainWindow
from imagedraw.gui.resultstablewidget import ResultsTableWidget
from imagedraw.gui.drawingwidget import DrawingWidget

class ImageDrawMainWindow(qw.QMainWindow, Ui_ImageDrawMainWindow):
    """
    The main window
    """

    def __init__(self, parent=None):
        """
        the object initalization function

            Args:
                parent (QObject): the parent QObject for this window

            Returns:
                None
        """
        super().__init__(parent)
        self.setupUi(self)
        self.setup_drawing_tab()
        self.setup_table_tab()

    def setup_drawing_tab(self):
        """
        initalize the drawing widget
        """
        tab = self._tabWidget.widget(0)
        drawing_widget = DrawingWidget(tab)
        layout = qw.QVBoxLayout(tab)
        layout.addWidget(drawing_widget)

    def setup_table_tab(self):
        """
        initalize the results table widget
        """
        print("setup table")
        tab = self._tabWidget.widget(1)
        results_widget = ResultsTableWidget(tab)
        layout = qw.QVBoxLayout(tab)
        layout.addWidget(results_widget)

    @qc.pyqtSlot()
    def save_data(self):
        """
        callback for saveing the data
        """
        print("save data {}".format(id(self)))

    @qc.pyqtSlot()
    def save_image(self):
        """
        callback for saving the current image
        """
        print("save image {}".format(id(self)))

    @qc.pyqtSlot()
    def load_image(self):
        """
        callback for loading an image
        """
        print("load image {}".format(id(self)))
