## -*- coding: utf-8 -*-
"""
Created on Tue 02 Nov 2020

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
# pylint: disable = too-few-public-methods
# pylint: disable = c-extension-no-member

import PyQt5.QtWidgets as qw

from imagedraw.gui.imagedrawmainwindow import ImageDrawMainWindow

class ImageDrawApplication(qw.QApplication):
    """top level application"""

    def __init__(self, args):
        """
        initialize a main window and start event loop
        """
        super().__init__(args)
        window = ImageDrawMainWindow()
        window.show()
        self.exec_()    # enter event loop
