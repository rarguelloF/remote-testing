#!/usr/bin/python

import sys
from time import time

import optparse
import getpass

from paramiko import SSHClient, SSHException, AuthenticationException, AutoAddPolicy
import socket
import select

# remote-testing imports
import doc_func
from tests import *

class sshConnection():

    def __init__(self, host, user, password):
        self.host = host
        self.user = user
        self.password = password
        self.connection = None
        self.channel = None

    def connect(self):
        try:
            print "[+] Estableciendo conexion SSH con %s@%s...." % (self.user, self.host)
            self.connection = SSHClient()
            self.connection.set_missing_host_key_policy(AutoAddPolicy())
            self.connection.connect(
                self.host, 
                username = self.user, 
                password = self.password, 
                allow_agent = False, 
                look_for_keys = False
            )
        except AuthenticationException, e:
            print "[+] Error de autenticacion: " ,e
            return 1
        except SSHException, e:
            print "[+] Error en SSH: " , e
            return 2
        except socket.error, e:
            print "[+] Error de conexion: ", e
            return 3
        else: 
            print "[+] Conexion establecida."
            return 0

    def send_command(self, command):
        if not self.connection:
            print '[+] No hay ninguna conexion abierta.'
            return 1
        else:
            cmd_output = ''
            i = 1
            while i <= 3:
                try:
                    # Send the command (non-blocking)
                    stdin, stdout, stderr = self.connection.exec_command(command)
                except SSHException as e:
                    if i<3:
                        print '[+] Error en la conexion SSH: %s.\n' % e
                        print 'Volviendo a intentar conectar... (intento %s de 3)' % i
                        self.connection = self.connect()
                        i+=1
                        time.sleep(2)
                    else:
                        print '[+] Fallo de conexion. Abortando prueba.'
                        return 1

            # Wait for the command to terminate
            while not stdout.channel.exit_status_ready():
                # Only print data if there is data to read in the channel
                if stdout.channel.recv_ready():
                    rl, wl, xl = select.select([stdout.channel], [], [], 0.0)
                    if len(rl) > 0:
                        # Print data from stdout
                        cmd_output+=stdout.channel.recv(1024)
            return cmd_output

    def disconnect(self):
        if self.connection:
            self.connection.close()
            return 0
        else:
            print '[+] No hay ninguna conexion abierta.'
            return 1



def read_config_file(filename):
    '''
    Parsea el fichero de configuracion especificado con la
    siguiente sintaxis:

    user1@host1 password1
    user2@host2 password2
    ...
    '''
    hosts = []
    with open(filename, 'r') as f:
        text = f.read()
        for line in text.split('\n'):
            try:
                host, pwd = line.split(' ')
                user, ip = host.split('@')
            except:
                if line != '':
                    print 'Bad line: %s' % line
            else:
                hosts.append((ip, user, pwd))
    return hosts

def select_test(conn, doc):
    dict_tests = {
        '1': custom_test,
        '2': OSPF_test,
        '3': Comprobar_Contador_ACL,
    }
    print "PRUEBAS"
    print "1) Elegir comando"
    print "2) Comprobar sesion OSPF"
    print "3) Comprobar contador ACL"

    option = raw_input('Selecciona el numero de prueba a realizar: ')

    try:
        dict_tests[option](conn, doc)
    except KeyError as e:
        print 'Opcion no existe.'

def parse_program_options():
    parser = optparse.OptionParser(usage='Usage: remote-tests.py [options]')

    parser.add_option('-f', help='''Si se especifica, recoge la informacion de los hosts 
        a testear del fichero dado.''', dest='hosts_file', default=None, action='store')
    parser.add_option('-o', help='''Nombre del .doc de salida.''', 
        dest='doc_name', default='Prueba', action='store')

    (opts, args) = parser.parse_args()

    hosts = None
    if opts.hosts_file:
        try:
            hosts = read_config_file(opts.hosts_file)
        except Exception as e:
            print 'Error abriendo el fichero de hosts: ', e

    return (hosts, opts.doc_name)


def main():
    hosts, doc_name = parse_program_options()

    doc = doc_func.create(doc_name)

    if hosts:
        for host in hosts:
            ip, user, pwd = host
            ssh_conn = sshConnection(ip, user, pwd)
            code = ssh_conn.connect()
            if code == 1:
                i = 1
                while code == 1 and i<=2:
                    pwd = getpass.getpass("Introduzca password para %s@%s\n" % (user,ip))
                    code = ssh_conn.connect()
                    i+=1
            if code == 0:
                doc.add_heading('Pruebas sobre %s' % ip, level=1)
                try:
                    while(1):
                        select_test(ssh_conn, doc)
                except KeyboardInterrupt:
                    ssh_conn.disconnect()

            ssh_conn.disconnect()
    else:
        while(1):
            print 'Press CTRL+C to stop.'
            ip = raw_input("Introduzca IP remota \n")
            user = raw_input("Introduzca el usuario \n")
            pwd = getpass.getpass("Introduzca password \n")

            ssh_conn = sshConnection(ip, user, pwd)
            code = ssh_conn.connect()
            if code == 1:
                i = 1
                while code == 1 and i<=2:
                    pwd = getpass.getpass("Introduzca password para %s@%s\n" % (user,ip))
                    code = ssh_conn.connect()
                    i+=1
            if code == 0:
                doc.add_heading('Pruebas sobre %s' % ip, level=1)
                try:
                    while(1):
                        select_test(ssh_conn, doc)
                except KeyboardInterrupt:
                    ssh_conn.disconnect()

            ssh_conn.disconnect()

    doc_func.save_doc(doc, doc_name)

if __name__ == '__main__':
    main()
