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

@copyright 2020
@author: j.h.pickering@leeds.ac.uk and j.leng@leeds.ac.uk
"""

import os

# a list of the modules that the package requires
modules = ["regionselectionmainwindow", "regionselectionwidget", "resultstablewidget"]

# relative path to the Qt .ui files
ui_path = "./resources/designer_ui/{}.ui"

# relative path to the python source files
py_path = "./regionselection/gui/Ui_{}.py"

def build(module_name):
    """
    run pyuic5 on a single module
    
        Args:
            module_name (string) the module name with no decoration or postfix
    """
    ui_file = ui_path.format(module_name)
    py_file = py_path.format(module_name)
    
    command = "pyuic5 {} -o {}"
    
    # in the case of failure CPython will print its own error message
    if os.system(command.format(ui_file, py_file)) == 0:
        print("made Ui_{}.py".format(module_name))

if __name__ == "__main__":
    for module in modules:
        build(module)
