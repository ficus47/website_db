import socket

def get_local_ip_address():
    # Créer une socket
    s = socket.socket(socket.AF_INET, socket.SOCK_DGRAM)

    try:
        # Connexion à un serveur extérieur
        s.connect(("8.8.8.8", 80))
        local_ip_address = s.getsockname()[0]
    finally:
        s.close()

    return local_ip_address

def get_server_address(port):
    local_ip_address = get_local_ip_address()
    return f"ws://{local_ip_address}:{port}"

# Port sur lequel votre serveur WebSocket écoute
port = 8765

# Obtenir l'adresse du serveur WebSocket
server_address = get_server_address(port)
print("Adresse du serveur WebSocket:", server_address)
