#!/usr/bin/env python

import ssl
import socket
import logging

logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s:%(levelname)s:%(message)s"
    )

NAMESERVER = '1.1.1.1' #CloudFlare DNS server
NAMESERVER_PORT = 853
PROXY_ADDR = '0.0.0.0'
PROXY_PORT = 53
BUFFER_SIZE = 1024

def encrypt_send(request_data, nameserver, port, buffer_size):

    try:

        context = ssl.SSLContext(ssl.PROTOCOL_TLS_CLIENT)
        context.load_verify_locations('/etc/ssl/cert.pem')

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM, 0) as client_sock:
            with context.wrap_socket(client_sock, server_hostname=nameserver) as sec_sock:

                try:
                    sec_sock.settimeout(5)
                    sec_sock.connect((nameserver, port))
                    sec_sock.send(request_data)
                    logging.info('request sent via encrypted channel')
                    response_ns = sec_sock.recv(buffer_size)
                    logging.info('received response from Nameserver %s' % response_ns)

                except Exception as e:
                    logging.error('encountered exception %s', str(e))


    except Exception as e:
        logging.error('cannot connect to the server: %s', str(e))
        return False

    return response_ns

if __name__ == '__main__':

    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_address = (PROXY_ADDR, PROXY_PORT)
    logging.info('starting server listening on %s port %s' % server_address)
    sock.bind(server_address)
    sock.listen(1)

    while True:
        logging.info('waiting for a connection')
        connection, client_address = sock.accept()

        try:
            logging.info('connection from %s', client_address)

            while True:
                request_data = connection.recv(BUFFER_SIZE) # Data from client to Proxy
                logging.info('received "%s"' % request_data)

                if request_data:
                    logging.info('received request_data from the client')
                    response_data = encrypt_send(request_data, NAMESERVER, NAMESERVER_PORT, BUFFER_SIZE) # Data from Cloudflare to Proxy
                    if response_data:
                        connection.sendall(response_data)

                else:
                    logging.info('no more data from %s', client_address)
                    break

        except Exception as e:
            logging.error(e)

        finally:
            connection.close()