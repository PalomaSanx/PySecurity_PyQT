import sys
import nmap
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
from pip._vendor.distlib.compat import raw_input


class ejemplo_GUI(QMainWindow):
    def __init__(self):
        super().__init__()
        uic.loadUi("seguridad.ui", self)
        self.botonNmap.clicked.connect(self.fn_activarNmap)

    def fn_activarNmap(self):
        host = self.target.toPlainText()
        nm = nmap.PortScanner()
        nm.scan(host, '22-443')

        for host in nm.all_hosts():
            string = 'Host : %s (%s)' % (host, nm[host].hostname())
            string = string + '\n----------------------------------------------------'
            string = string + '\nState : %s' % nm[host].state()
            string = string + '\n----------------------------------------------------'

        for proto in nm[host].all_protocols():

            string = string + '\nProtocol : {}'.format(proto)
            lport = nm[host][proto].keys()
            for port in lport:
                string = string + '\nport : {}\tstate : {}'.format(port, nm[host][proto][port]['state'])

       ## string = string +'\n'+nm.csv()

        self.resultado.setText(string)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = ejemplo_GUI()
    GUI.show()
    sys.exit(app.exec_())
