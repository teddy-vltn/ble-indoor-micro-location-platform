sudo ip route add 192.168.1.0/24 via 192.168.1.5
sudo iptables -t nat -A POSTROUTING -o wlp0s20f3 -j MASQUERADE
