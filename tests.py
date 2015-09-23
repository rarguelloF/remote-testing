#!/usr/bin/python

from scapy.all import send, IP, ICMP

import doc_func

###########################################
#                TESTS                    #
###########################################

def custom_test(conn, doc_obj):
    '''
    Prueba generica para introducir cualquier otro comando.
    '''
    #Se envia para que muestre la salida de una vez y no haya que pulsar espacio
    resp = conn.send_command('terminal length 0')
    print resp
    cmd = raw_input("Introduzca comando: \n")
    resp = conn.send_command(cmd)
    print resp
    return resp
     
def OSPF_test(conn, doc_obj):
    doc_func.write(doc_obj, "Comprobar OSPF", 'tituloprueba', 'garamond', 16, 
        {'all_caps': True})
    doc_func.write(doc_obj, "OBJETIVO", 'tituloprueba2', 'garamond', 12, 
        {'all_caps': True, 'bold': True, 'underline': True})
    doc_func.write(doc_obj, "Comprobar que la sesion de OSPF se ha establecido", 'normal2', 'garamond', 12)
    doc_func.write(doc_obj, "Pasos a realizar", 'tituloprueba2', 'garamond', 12,
        {'all_caps': True, 'bold': True, 'underline': True})
    doc_func.write(doc_obj, "1 Introducir el comando show ip ospf neighbor y comprobar que el estado es FULL", 'normal2', 'garamond', 12)

    resp = conn.send_command('show ip ospf neighbor')
    doc_func.write(doc_obj, resp, 'normal1', 'courier new', 9)
    print resp

    doc_func.write(doc_obj, "Conclusiones", 'tituloprueba2', 'garamond', 12, 
        {'bold': True, 'underline': True, 'all_caps': True})
    if 'FULL' in resp:
        doc_func.write(doc_obj, "La sesion se ha establecido correctamente", 'normal2', 'garamond', 12)
        doc_func.write(doc_obj, "Resultado", 'tituloprueba2', 'garamond', 12, 
            {'bold': True, 'underline': True, 'all_caps': True})
        doc_func.write(doc_obj, "OK", 'ok', 'garamond', 12, 
            {'bold': True, 'color': 'green'})
    else:
        doc_func.write(doc_obj, "La sesion no se ha establecido correctamente", 'normal2', 'garamond', 12)
        doc_func.write(doc_obj, "Resultado", 'tituloprueba2', 'garamond', 12, 
            {'bold': True, 'underline': True, 'all_caps': True})
        doc_func.write(doc_obj, "NOK", 'ok', 'garamond', 12, 
            {'bold': True, 'color': 'red'})

    return 0
     
def Comprobar_Contador_ACL(conn, doc_obj):
    doc_func.write(doc_obj, "Comprobar_Contador_ACL", 'tituloprueba', 'garamond', 16, 
        {'all_caps': True})
    doc_func.write(doc_obj, "OBJETIVO", 'tituloprueba2', 'garamond', 12, 
        {'all_caps': True, 'bold': True, 'underline': True})
    doc_func.write(doc_obj, "Comprobar que la ACL matchea el trafico", 'normal2', 'garamond', 12)
    doc_func.write(doc_obj, "Pasos a realizar", 'tituloprueba2', 'garamond', 12,
        {'all_caps': True, 'bold': True, 'underline': True})
    doc_func.write(doc_obj, "Enviar trafico con scapy", 'normal2', 'garamond', 12)
    
    ip_src = raw_input("Introduzca IP origen \n")
    ip_dst = raw_input("Introduzca IP destino \n")
    
    print "packet = IP(src=%s, dst=%s)/ICMP()" % (ip_src, ip_dst)
    print "send(packet*3)"

    doc_func.write(doc_obj, "packet = IP(src=%s, dst=%s)/ICMP()" % (ip_src, ip_dst), 'normal2', 'garamond', 12)
    doc_func.write(doc_obj, "send(packet*3)", 'normal2', 'garamond', 12)

    packet = IP(src=ip_src, dst=ip_dst)/ICMP()
    send(packet*3)

    #Una vez enviado el trafico enviamos el comando show ip access-list a la consola del router
    resp = conn.send_command('show ip ospf neighbor')
    doc_func.write(doc_obj, resp, 'normal1', 'courier new', 9)
    print resp

    doc_func.write(doc_obj, "Conclusiones", 'conclusiones', 'garamond', 12, 
        {'bold': True, 'underline': True, 'all_caps': True})
    if '3' in resp:
        doc_func.write(doc_obj, "La ACL matchea correctamente los paquetes enviados", 'normal2', 'garamond', 12)
        doc_func.write(doc_obj, "Resultado", 'conclusiones', 'garamond', 12, 
            {'bold': True, 'underline': True, 'all_caps': True})
        doc_func.write(doc_obj, "OK", 'ok', 'garamond', 12, 
            {'bold': True, 'color': 'green'})
    else:
        #Si no encuentra la palabra FULL
        doc_func.write(doc_obj, "La ACL no matchea correctamente los paquetes enviados", 'normal2', 'garamond', 12)
        doc_func.write(doc_obj, "Resultado", 'conclusiones', 'garamond', 12, 
            {'bold': True, 'underline': True, 'all_caps': True})
        doc_func.write(doc_obj, "NOK", 'ok', 'garamond', 12, 
            {'bold': True, 'color': 'red'})

    return 0