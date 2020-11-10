## -*- coding: utf-8 -*-
"""
Created on Tue 10 Nov 2020

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

#import PyQt5.QtWidgets as qw
import PyQt5.QtGui as qg
import PyQt5.QtCore as qc

import numpy as np

from imagedraw.gui.DrawRect import DrawRect

class RegionsTableModel(qc.QAbstractTableModel):
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
            tmp = self._data[index.row()]
            variant = qc.QVariant(None)
            if index.column() == 0:
                variant = qc.QVariant(index.row()+1)
            elif index.column() == 1:
                variant = qc.QVariant(int(tmp.left))
            elif index.column() == 2:
                variant = qc.QVariant(int(tmp.top))
            elif index.column() == 3:
                variant = qc.QVariant(int(tmp.right))
            elif index.column() == 4:
                variant = qc.QVariant(int(tmp.bottom))

            return variant

        if role == qc.Qt.BackgroundRole:
            variant = qg.QColor('darkgrey')
            if index.column() == 0:
                variant = qg.QColor('white')
            elif index.column() < 3:
                variant = qg.QColor('grey')

            return variant

        return qc.QVariant()

    def headerData(self, section, orientation, role):
        """
        getter for the table headers
        """
        headers = ["Num", "Left x", "Top y", "Right x", "Bottom y"]

        if role == qc.Qt.DisplayRole and orientation == qc.Qt.Horizontal:
            return qc.QVariant(headers[section])

        return qc.QVariant()

    def rowCount(self, index):
        """ the number of rows in table"""
        #return len(self._data)
        if self._data is None:
            return 0

        return len(self._data)

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
            rect = self._data[index.row()]
            if index.column() == 1:
                self._data[index.row()] = DrawRect(top=rect.top,
                                                   bottom=rect.bottom,
                                                   left=np.uint32(value),
                                                   right=rect.right)
            elif index.column() == 2:
                self._data[index.row()] = DrawRect(top=np.uint32(value),
                                                   bottom=rect.bottom,
                                                   left=rect.left,
                                                   right=rect.right)
            elif index.column() == 3:
                self._data[index.row()] = DrawRect(top=rect.top,
                                                   bottom=rect.bottom,
                                                   left=rect.left,
                                                   right=np.uint32(value))
            elif index.column() == 4:
                self._data[index.row()] = DrawRect(top=rect.top,
                                                   bottom=np.uint32(value),
                                                   left=rect.left,
                                                   right=rect.right)
            else:
                return False

            self.dataChanged.emit(index, index)

            return True

        return False

    @qc.pyqtSlot(DrawRect)
    def add_region(self, region):
        """
        add a new region to the data, will clear all selections and editing

            Args:
                region (DrawRect) the region to add
        """
        self.beginResetModel()
        self._data.append(region)
        self.endResetModel()
