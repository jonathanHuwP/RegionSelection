import PyQt5.QtWidgets as qw

from imagedraw.gui.imagedrawmainwindow import ImageDrawMainWindow

class ImageDrawApplication(qw.QApplication):

  def __init__(self, args):
    super().__init__(args)
    window = ImageDrawMainWindow()
    window.show()
    self.exec_()    # enter event loop
