import sys
import nmap
from PyQt5 import uic
from PyQt5.QtWidgets import QMainWindow, QApplication
import logo_rc
import shodan
from urllib.request import urlopen
import whois
import sys
import os
import prueba



class ejemplo_GUI(QMainWindow):

    def __init__(self):
        super().__init__()
        uic.loadUi("seguridad.ui", self)
        self.botonNmap.clicked.connect(self.fn_activarNmap)
        self.botonShodan.clicked.connect(self.fn_activarShodan)
        self.botonRobots.clicked.connect(self.fn_activarRobots)
        self.botonWhois.clicked.connect(self.fn_activarWhois)
        self.botonDiccionario.clicked.connect(self.fn_activarDiccionario)

    def fn_activarNmap(self):
        host = self.target.toPlainText()
        nm = nmap.PortScanner()
        nm.scan(host, '22-443')  # nmap -oX - -p 22-443 -sV 127.0.0.1
        string = nm.command_line()
        string = string + '\n----------------------------------------------------'

        for host in nm.all_hosts():
            string = string + '\nHost : %s (%s)' % (host, nm[host].hostname())
            string = string + '\n----------------------------------------------------'
            string = string + '\nState : %s' % nm[host].state()
            string = string + '\n----------------------------------------------------'

        for proto in nm[host].all_protocols():
            string = string + '\nProtocol : {}'.format(proto)
            lport = nm[host][proto].keys()
            for port in lport:
                string = string + '\nport : {}\tstate : {}'.format(port, nm[host][proto][port]['state'])

        self.resultado.setText(string)

    def fn_activarShodan(self):
        host = self.target.toPlainText()
        SHODAN_API_KEY = "TU API"
        api = shodan.Shodan(SHODAN_API_KEY)
        results = api.host(host)
        # Mostramos la informacion.
        for item in results['data']:
            string2 = 'Port: {}\t Banner: {}'.format(item['port'], item['data'])
        self.resultado.setText(string2)

    def fn_activarRobots(self):
        string3=''
        url = self.target.toPlainText()
        with urlopen("http://"+url +"/robots.txt") as stream:
             string3=string3+stream.read().decode("utf-8")+"\n"

        self.resultado.setText(string3)
    def fn_activarWhois(self):
        url = self.target.toPlainText()
        dominio = whois.query(url)
        print(dominio.name)

    def fn_activarDiccionario(self):


        # self.user_min_longitude = self.getInput('- Enter min longitude of word [0]        : ', 'int',  '0')
        prueba.mainCLS.user_max_longitude = prueba.mainCLS.getInput('- Enter max longitude of word [4]        : ', 'int', '4')

        prueba.MainCLS.user_use_letters = prueba.MainCLS.getInput('- Use letters?                [Y/n]      : ', 'bool', 'y')
        if prueba.MainCLS.user_use_letters == True:
            prueba.MainCLS.user_use_lowercase = prueba.MainCLS.getInput('- Use lowercase?              [Y/n]      : ', 'bool', 'y')
            prueba.MainCLS.user_use_uppercase = prueba.MainCLS.getInput('- Use uppercase?              [y/N]      : ', 'bool', 'n')

        prueba.MainCLS.user_use_numbers = prueba.MainCLS.getInput('- Use numbers?                [Y/n]      : ', 'bool', 'y')
        prueba.MainCLS.user_use_specials = prueba.MainCLS.getInput('- Use special chars?          [y/N]      : ', 'bool', 'n')
        prueba.MainCLS.user_filename = prueba.MainCLS.getInput('- Filename of dictionary      [dict.txt] : ', 'file', 'dict.txt')

        prueba.MainCLS.list_string = ''

        if prueba.MainCLS.user_use_letters == True:

            if prueba.MainCLS.user_use_lowercase == True:
                prueba.MainCLS.list_string = prueba.MainCLS.list_string + 'abcdefghijklmnopqrstuvwxyz'

            if prueba.MainCLS.user_use_uppercase == True:
                prueba.MainCLS.list_string = prueba.MainCLS.list_string + 'ABCDEFGHIJKLMNOPQRSTUVWXYZ'

        if prueba.MainCLS.user_use_numbers == True:
            prueba.MainCLS.list_string = prueba.MainCLS.list_string + '0123456789'

        if prueba.MainCLS.user_use_specials == True:
            prueba.MainCLS.list_string = prueba.MainCLS.list_string + '\\/\'"@#$%&/()=?¿!¡+-*_.:,;'

        prueba.MainCLS.total_of_words = 0
        prueba.MainCLS.total_of_characters = 0
        for n in range(0, prueba.MainCLS.user_max_longitude):
            total = (len(self.list_string) ** (n + 1))
            prueba.MainCLS.total_of_words = prueba.MainCLS.total_of_words + total
            # (word length * count words) + \n
            prueba.MainCLS.total_of_characters = prueba.MainCLS.total_of_characters + (total * (n + 1)) + total

        # Summary
        response = prueba.MainCLS.printSummary()
        if response == False:
            return

        # Load file
        if os.path.isfile(prueba.MainCLS.user_filename):
            os.remove(prueba.MainCLS.user_filename)
        prueba.MainCLS.file_handler = open(prueba.MainCLS.user_filename, 'w')

        # Execute all
        prueba.MainCLS.loop('', prueba.MainCLS.user_max_longitude)

        # End
        prueba.MainCLS.file_handler.close()
        print ("\r                                                       \r- End!")





if __name__ == '__main__':
    app = QApplication(sys.argv)
    GUI = ejemplo_GUI()
    GUI.show()
    sys.exit(app.exec_())
