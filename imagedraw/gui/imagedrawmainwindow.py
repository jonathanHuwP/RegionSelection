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
import csv
import numpy as np

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
import imagedraw.gui.autosavebinary as autosave

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

        ## storage for the autosave object
        self._autosave = None

        ## name of the current project
        self._project = None

    def make_autosave(self):
        """
        create a new autosave file
        """
        files = autosave.list_backup_files(os.getcwd())
        for file in files:
            print(file)

        projects = autosave.list_backup_projects(files)
        for project in projects:
            print(project)

        # get autosave file
        self._autosave = autosave.AutoSaveBinary(self._project)

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
        self.autosave()

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
        self.autosave()

    @qc.pyqtSlot()
    def load_data(self):
        if self._image is None:
            qw.QMessageBox.information(self, "No Image", "You must have an image")
            return

        if len(self._regions) > 0:
            reply = qw.QMessageBox.question(self,
                                            "Overwrite",
                                            "You will loose current data?")

            if reply == qw.QMessageBox.Yes:
                print("Go ahded")
            else:
                print("abort")

        file_name, _ = qw.QFileDialog.getOpenFileName(
            self,
            self.tr("Save File"),
            os.path.expanduser('~'),
            self.tr("CSV (*.csv)"))

        if file_name is not None and file_name != '':
            self.read_regions_csv_file(file_name)
            
    def read_regions_csv_file(self, file_name):
        """
        read a csv file of regions
        
            Args:
                file_name (string) the full path to the file
        """
        with open(file_name, 'r') as in_file:
            reader = csv.reader(in_file)
            
            # get the project name and remove header line
            self._project = next(reader, None)
            self.setWindowTitle(self._project[0])
            headers = next(reader, None)
            
            for row in reader:
                self._regions.append(DrawRect(np.uint32(row[0]), 
                                              np.uint32(row[2]), 
                                              np.uint32(row[1]), 
                                              np.uint32(row[3])))
                                              
            self.data_changed(None, None)
            self.make_autosave()

    @qc.pyqtSlot()
    def save_data(self):
        """
        callback to save the data
        """
        if len(self._regions) < 1:
            qw.QMessageBox.information(self, "Save", "You have no data to save")
            return

        file_name, _ = qw.QFileDialog.getSaveFileName(
            self,
            self.tr("Save File"),
            os.path.expanduser('~'),
            self.tr("CSV (*.csv)"))

        if file_name is not None:
            data = []
            for region in self._regions:
                data.append([region.top, region.bottom, region.left, region.right])

            with open(file_name, 'w', newline='') as file:
                writer = csv.writer(file)
                header = ["top y", "left x", "bottom y", "right x"]
                writer.writerow([self._project])
                writer.writerow(header)
                writer.writerows(data)

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
            reply = qw.QInputDialog.getText(self,
                                            "Project Name",
                                            "Proj Name",
                                            qw.QLineEdit.Normal)
            if not reply[1]:
                return

            if reply[0] != '':
                self._project = reply[0]
            else:
                self._project = file_name

            self._image = qg.QImage(file_name)
            self._drawing_widget.display_image(self._image)
            self.setWindowTitle(self._project)

    def get_regions(self):
        """
        getter for the regions list
        """
        return self._regions

    def autosave(self):
        if self._autosave is None:
            self.make_autosave()

        self._autosave.save_data(self._regions)
