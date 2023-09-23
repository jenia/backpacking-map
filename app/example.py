from socket import getaddrinfo


def resolve_postgres(service, port):
    element = 0
    ip_port = 4
    ip_index_in_tuple = 0
    return getaddrinfo(service, port)[element][ip_port][ip_index_in_tuple]
