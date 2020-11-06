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

from imagedraw.gui.Ui_drawingwidget import Ui_DrawingWidget

class DrawingWidget(qw.QWidget, Ui_DrawingWidget):
    """
    Provideds the ability to display an image and, draw lines on the image
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

    @qc.pyqtSlot()
    def accept_line(self):
        """
        callback for accepting a line, save line to data and emit data_changed
        """
        print("accept_line {}".format(id(self)))

    @qc.pyqtSlot()
    def toggel_display_lines(self):
        """
        callback for 'show all' radio button
        """
        if self._displayAllButton.isChecked():
            print(">>> Show all")
        else:
            print(">>>> Only show drawing")
            
    def display_image(self, image):
        """
        display a new image
            
            Args:
                image (QImage) image to be displayed
        """
        print(f"{id(self)} showing {image}")
