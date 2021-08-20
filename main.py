from PyQt5.QtPrintSupport import QPrinter, QPrintDialog
from PyQt5 import QtWidgets
import sys
import zipfile
import tempfile
import os
import subprocess

supported_types = ["*.pdf"]


def fatal_error(message):
    QtWidgets.QMessageBox.critical(None, "Error", str(message))
    app.exit(1)
    exit()


if __name__ == '__main__':
    app = QtWidgets.QApplication(sys.argv)

    if len(sys.argv) < 2:
        fatal_error("Missed arguments")

    dialog = QPrintDialog()
    if not dialog.exec():
        exit(0)
    printer = dialog.printer()
    print(printer.copyCount())

    dir_temp = tempfile.TemporaryDirectory()

    try:
        zip_archive = zipfile.ZipFile(sys.argv[1], 'r')
        zip_archive.extractall(dir_temp.name)

        for s_type in supported_types:
            args = [
                "lpr", "-o", "landscape",
                "-#", str(printer.copyCount()),
                "-P", printer.printerName(),
                f"{dir_temp.name}/{s_type}"
                ]
            proc = subprocess.Popen(args, stdout=subprocess.PIPE, stderr=subprocess.PIPE)
            proc.wait()
            print(proc.communicate())


    except FileNotFoundError as e:
        fatal_error(e)

    app.quit()





