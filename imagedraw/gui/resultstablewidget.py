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

        model = LinesTableModel(None)
        self._tableView.setModel(model)
        self._tableView.setStyleSheet("QHeaderView::section {background-color:lightgray}")
        self._tableView.verticalHeader().hide()


class LinesTableModel(qc.QAbstractTableModel):
    """
    the data model for the constituancy results table

    Note: the function names and variable lists are fixed
    by the need to override the C++ originals and cannot be
    changed
    """

    def __init__(self, data):
        """
        store the data

            Args:
                data (dict) the data store to be displayed/edited
        """
        super().__init__()
        self._data = data

    def data(self, index, role):
        """
        getter for data and display features

            Args:
                index (QModelIndex) the location of the data row(), column()
                role (int) the Qt flag for the purpose of the get, raw data, background etc

            Returns:
                required (QVariant) data for the cell
        """

        if role == qc.Qt.DisplayRole:
            return qc.QVariant("stuff")

        if role == qc.Qt.BackgroundRole:
            if index.column() == 0:
                return qg.QColor('white')
            elif index.column() < 3:
                return qg.QColor('grey')

            return qg.QColor('darkgrey')

        return qc.QVariant()

    def headerData(self, section, orientation, role):
        """
        getter for the table headers
        """
        headers = ["Num", "Start x", "Start y", "End x", "End y"]

        if role == qc.Qt.DisplayRole and orientation == qc.Qt.Horizontal:
            return qc.QVariant(headers[section])

        return qc.QVariant()

    def rowCount(self, index):
        """ the number of rows in table"""
        #return len(self._data)
        return 5

    def columnCount(self, index):
        """the number of columns in the table"""
        return 5

    def flags(self, index):
        """
        return that the numeric columns are editable
        """
        if index.column() == 0:
            return qc.Qt.ItemIsEnabled|qc.Qt.ItemIsSelectable

        return qc.Qt.ItemIsEnabled|qc.Qt.ItemIsSelectable|qc.Qt.ItemIsEditable

    def setData(self, index, value, role):
        """
        allow the new value to replace the old in the data source, this method will
        not work if the order of the data is different between the dictionary and
        the table, Python 3.6 onward preserve insetion order by default
        """
        if role == qc.Qt.EditRole and value.isnumeric():
            self.dataChanged.emit(index, index)
            return True

        return False
