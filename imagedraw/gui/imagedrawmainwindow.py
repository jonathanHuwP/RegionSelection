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

import os

import PyQt5.QtWidgets as qw
import PyQt5.QtGui as qg
import PyQt5.QtCore as qc
#import PyQt5.QtWebEngineWidgets as qe
import PyQt5.QtPrintSupport as qp

from imagedraw.gui.Ui_imagedrawmainwindow import Ui_ImageDrawMainWindow
from imagedraw.gui.resultstablewidget import ResultsTableWidget
from imagedraw.gui.drawingwidget import DrawingWidget
from imagedraw.gui.DrawRect import DrawRect
from imagedraw.gui.regionstablemodel import RegionsTableModel

class ImageDrawMainWindow(qw.QMainWindow, Ui_ImageDrawMainWindow):
    """
    The main window
    """

    ## signal to indicate the user has selected a new rectangle
    new_selection = qc.pyqtSignal(DrawRect)

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

        ## the drawing widget
        self._drawing_widget = None

        ## the results widget
        self._results_widget = None

        ## storage for the image
        self._image = None

        ## storage for the regions
        self._regions = []

        self.setup_drawing_tab()
        self.setup_table_tab()

    def setup_drawing_tab(self):
        """
        initalize the drawing widget
        """
        tab = self._tabWidget.widget(0)
        self._drawing_widget = DrawingWidget(tab, self)
        layout = qw.QVBoxLayout(tab)
        layout.addWidget(self._drawing_widget)

    def setup_table_tab(self):
        """
        initalize the results table widget
        """
        tab = self._tabWidget.widget(1)
        model = RegionsTableModel(self._regions)
        self._results_widget = ResultsTableWidget(tab, model)
        layout = qw.QVBoxLayout(tab)
        layout.addWidget(self._results_widget)

        self.new_selection.connect(model.add_region)
        model.dataChanged.connect(self.data_changed)

    @qc.pyqtSlot(qc.QModelIndex, qc.QModelIndex)
    def data_changed(self, tl_index, br_index):
        """
        callback for user editing of the data via tableview

            Args:
                tl_index (qc.QModelIndex) top left location in data
                br_index (qc.QModelIndex) bottom right location in data
        """
        self._drawing_widget.repaint()

    @qc.pyqtSlot(DrawRect)
    def new_region(self, region):
        """
        slot for signal that a new regions has been selected, emit own signal

            Args:
                region (DrawRect) the region that is to be added

            Emits:
                new_selection (DrawRect) forward the message to the data model
        """
        self.new_selection.emit(region)

    @qc.pyqtSlot()
    def save_data(self):
        """
        callback for saveing the data
        """
        print("save data {}".format(id(self)))

    @qc.pyqtSlot()
    def print_table(self):
        """
        callback for printing the table as pdf
        """
        print(f"print the table {id(self)}")
        printer = qp.QPrinter(qp.QPrinter.PrinterResolution)
        printer.setOutputFormat(qp.QPrinter.PdfFormat)
        printer.setPaperSize(qp.QPrinter.A4)
        printer.setOutputFileName("output.pdf")

        doc = qg.QTextDocument()

        html_string = self._results_widget.get_table_as_html()
        doc.setHtml(html_string)
        doc.print(printer)

    @qc.pyqtSlot()
    def save_image(self):
        """
        callback for saving the current image
        """
        print("save image {}".format(id(self)))
        file_name = "output.png"
        pixmap = self._drawing_widget.get_current_pixmap()
        
        if pixmap is not None:
            pixmap.save(file_name)

    @qc.pyqtSlot()
    def load_image(self):
        """
        callback for loading an image
        """
        file_name, _ = qw.QFileDialog.getOpenFileName(
            self,
            "Read Results File",
            os.path.expanduser('~'),
            "PNG (*.png);; JPEG (*.jpg)")

        if file_name is not None and file_name != '':
            self._image = qg.QImage(file_name)
            self._drawing_widget.display_image(self._image)

    def get_regions(self):
        """
        getter for the regions list
        """
        return self._regions
