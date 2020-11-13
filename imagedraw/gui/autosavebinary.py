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
import tempfile
import pickle

class AutoSaveBinary(object):
    """
    construct and use a binary autosave file
    """

    _MAGIC_CODE = "idw-01"

    def __init__(self, project):
        """
        set-up the object

            Args:
                project (string) the project name will be added to save
                file_path (string) the full path name of the file if not present tempfile is created
        """
        # get file, close file, save file path
        descriptor, file_path = tempfile.mkstemp(suffix='.idback',
                                                 prefix='.',
                                                 dir=os.getcwd(),
                                                 text=False)
        os.close(descriptor)

        ## store the file path
        self._file_path = file_path

        ## store the project name
        self._project = project

    def get_file_path(self):
        """
        getter for the file path
        """
        return self._file_path

    def save_data(self, output):
        """
        write data to the binary file

            Args:
                output (object) the data to be output
        """
        with open(self._file_path, 'w+b') as file:
            # delete existing contents
            file.truncate(0)

            # make tuple of project name and output
            data = (self._MAGIC_CODE, self._project, output)

            # save binary
            pickle.dump(data, file)

def list_backup_files(dir_path):
    """
    make a list of all backup files

        Args:
            dir_path (string) full path to search directory

        Returns:
            list of backup files in the directory
    """
    files = []

    raw = os.listdir(dir_path)

    for item in raw:
        if os.path.isfile(item) and item.endswith(".idback"):
            files.append(os.path.join(dir_path, item))

    return files

def list_backup_projects(file_paths):
    projects = []

    for file in file_paths:
        data = None

        # ignore empty or corrupt files
        try:
            data = pickle.load(open(file, 'rb'))
        except EOFError:
            pass

        if data is not None and len(data) > 1 and data[0] == AutoSaveBinary._MAGIC_CODE:
            projects.append(data[1])

    return projects

def get_backup_project(file_path):
    project = None
    data = None

    try:
        tmp = pickle.load(open(file, 'rb'))
    except EOFError:
        return None, None

    if tmp[0] == AutoSaveBinary._MAGIC_CODE:
        return tmp[1], tmp[2]

    return None, None
