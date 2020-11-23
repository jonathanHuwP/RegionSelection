## -*- coding: utf-8 -*-
"""
Created on Tue 27 Oct 2020

Licensed under the Apache License, Version 2.0 (the "License"); you may not use
this file except in compliance with the License. You may obtain a copy of the
License at http://www.apache.org/licenses/LICENSE-2.0

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
# pylint: disable = import-error

import PyQt5.QtWidgets as qw
import PyQt5.QtGui as qg
import PyQt5.QtCore as qc

from regionselection.gui.regionselectionlabel import RegionSelectionLabel
from regionselection.gui.Ui_regionselectionwidget import Ui_RegionSelectionWidget

class RegionSelectionWidget(qw.QWidget, Ui_RegionSelectionWidget):
    """
    Provideds the ability to display an image and, draw lines on the image
    """

    def __init__(self, parent=None, regions_store=None):
        """
        the object initalization function

            Args:
                parent (QObject): the parent QObject for this window
                regions_store (ImageDrawMainWindow): the object holding the list of regions

            Returns:
                None
        """
        super().__init__(parent)

        self.setupUi(self)

        ## the label which will display images
        self._image_label = RegionSelectionLabel(self, regions_store)
        self._image_label.set_adding()
        self._image_label.new_selection.connect(regions_store.new_region)

    @qc.pyqtSlot()
    def toggel_display_regions(self):
        """
        callback for 'show all' radio button
        """
        if self._displayAllButton.isChecked():
            self._image_label.set_display_all()
            self.repaint()
        else:
            self._image_label.set_adding()

    def display_image(self, image):
        """
        display a new image

            Args:
                image (QImage) image to be displayed
        """
        self._image_label.setAlignment(
                qc.Qt.AlignTop | qc.Qt.AlignLeft)
        self._image_label.setSizePolicy(
                qw.QSizePolicy.Ignored,
                qw.QSizePolicy.Fixed)
        self._image_label.setSizePolicy(
                qw.QSizePolicy.Minimum,
                qw.QSizePolicy.Minimum)

        self._scrollArea.setWidget(self._image_label)
        self._scrollArea.setHorizontalScrollBarPolicy(qc.Qt.ScrollBarAsNeeded)
        self._scrollArea.setVerticalScrollBarPolicy(qc.Qt.ScrollBarAsNeeded)
        self._scrollArea.setVisible(True)

        self._image_label.setPixmap(qg.QPixmap(image))

    def get_current_pixmap(self):
        """
        getter for the currently displayed image, including regions

            Returns:
                QPixmap
        """
        return self._image_label.grab()

    def get_raw_pixmap(self):
        """
        getter for the original image, without regions

            Returns:
                QPixmap
        """
        return self._image_label.pixmap()
