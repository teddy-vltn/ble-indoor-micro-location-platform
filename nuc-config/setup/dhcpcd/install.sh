#!/bin/bash

# Vérifiez si l'utilisateur est root
if [ "$(id -u)" != "0" ]; then
   echo "Ce script doit être exécuté en tant que root" 1>&2
   exit 1
fi

# Définissez le nom de l'interface réseau
INTERFACE="eno1"
INTERFACE_WIFI=$(ip route | grep default | sed -e "s/^.*dev.//" -e "s/.proto.*//")

# Obtenez l'adresse IP actuelle de l'interface
IP_ACTUELLE=$(ip -4 addr show $INTERFACE | grep -oP '(?<=inet\s)\d+(\.\d+){3}')

# Nom du fichier de configuration Netplan
#FICHIER_NETPLAN="/etc/netplan/01-netcfg.yaml"
FICHIER_NETPLAN="/etc/netplan/50-cloud-init.yaml"

# Vérifiez si le fichier de configuration Netplan existe
if [ ! -f "$FICHIER_NETPLAN" ]; then
    echo "Le fichier $FICHIER_NETPLAN n'existe pas."
    exit 1
fi

# Ajoutez ou modifiez la configuration
cat > "$FICHIER_NETPLAN" <<EOL
network:
  version: 2
  ethernets:
    $INTERFACE:
      dhcp4: no
      addresses:
        - $IP_ACTUELLE/24
EOL

# Appliquez la configuration avec netplan
netplan apply

# Activez le routage IP
sysctl -w net.ipv4.ip_forward=1

# Rendez la modification permanente
echo "net.ipv4.ip_forward=1" >> /etc/sysctl.conf

# Mettez à jour les paquets et installez iptables si ce n'est pas déjà fait
apt update
apt install -y iptables

# Configurez iptables pour masquer les adresses IP
iptables -t nat -A POSTROUTING -o $INTERFACE_WIFI -j MASQUERADE

# Sauvegardez la configuration iptables
sh -c "iptables-save > /etc/iptables.rules"

# Ajoutez la route (pas sur)
# ip route add 192.168.1.0/24 via $IP_ACTUELLE
