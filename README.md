# RegionSelection
Demonstration of the use of Qt model views as a means of keeping multiple data view up to date.

In the program the user can load and view an image. By clicking and dragging on the image the user can select rectangular region. A list of these regions is shown in a QTableView held in a separate tab. A Qt model encapsulates the data and makes changes available to the table. The user can edit the data via the table and, which is handled by the model. The data changed signal from the model is connected to the image viewer, so if the viewer is in "show all selected regions" mode, changed input in the table will immediately appear in the view.

## Description
This project is the result of a self-teaching exercise in the use of Qt models and
the structuring of a Python/PyQt project.

## Running
To build the Qt Ui_ files run the script build_ui.py.

>python built_ui.py

To run the program run main.py

>python run_regionselection.py

## Possible Improvements

Possible improvements are

1. Put the table and view widgets in a splitter so they can be seen simultaneously.

## Acknowledgement
This work was funded by Joanna Leng's EPSRC funded RSE Fellowship (EP/R025819/1)
