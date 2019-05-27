import sys
import os


def liber_dir():
    return os.getenv("MLIBER_PATH")


def main():
    liber = liber_dir()
    sys.path.append(liber)
    from Qt import QtWidgets
    import pyqt_clarisse
    app = QtWidgets.QApplication.instance()
    if not app:
        app = QtWidgets.QApplication(["Clarisse"])
    from mliber_widgets.main_widget import MainWidget
    fw = MainWidget()
    fw.show()
    pyqt_clarisse.exec_(app)


if __name__ == "__main__":
    main()
