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
import PyQt5.QtGui as qg
import PyQt5.QtCore as qc

from imagedraw.gui.Ui_resultstablewidget import Ui_ResultsTableWidget

class ResultsTableWidget(qw.QWidget, Ui_ResultsTableWidget):
    """
    Provideds the ability to display an image and, draw lines on the image
    """

    def __init__(self, parent, model):
        """
        the object initalization function

            Args:
                parent (QObject): the parent QObject for this window
                data (list(DrawRect)): the source data

            Returns:
                None
        """
        super().__init__(parent)

        self.setupUi(self)

        self._tableView.setModel(model)
        self._tableView.setStyleSheet("QHeaderView::section {background-color:lightgray}")
        self._tableView.verticalHeader().hide()

    def new_data(self):
        print(">>>>>>> new data")
        self._tableView.viewport().update()
        self.repaint()
