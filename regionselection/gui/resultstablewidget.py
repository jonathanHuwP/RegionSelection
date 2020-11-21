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
# pylint: disable = c-extension-no-member
# pylint: disable = import-error
# pylint: disable = too-few-public-methods

import PyQt5.QtWidgets as qw
import PyQt5.QtCore as qc

from regionselection.gui.Ui_resultstablewidget import Ui_ResultsTableWidget

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

    def get_table_as_html(self):
        """
        get the current table as a html string

            Returns:
                string of html
        """
        html = "<table style=\"width:100%\">\n<tr>"
        index = self._tableView.model().index(0, 0)
        rows = self._tableView.model().rowCount(index)
        columns = self._tableView.model().columnCount(index)

        for column in range(columns):
            if not self._tableView.isColumnHidden(column):
                header = self._tableView.model().headerData(column,
                                                            qc.Qt.Horizontal,
                                                            qc.Qt.DisplayRole).value()
                html += f"<th>{header}</th>"
        html += "</tr>\n"

        for row in range(rows):
            html += "<tr>"
            for column in range(columns):
                if not self._tableView.isColumnHidden(column):
                    index = self._tableView.model().index(row, column)
                    data = self._tableView.model().data(index, qc.Qt.DisplayRole).value()
                    html += f"<td>{data}</td>"
            html += "</tr>\n"

        html += "\n</table>"

        return html
