# Tarpit SSH

Tarpit SSH is a simple software to waste the time of SSH attackers. Basically
everythinga apart from my own and users of my systems port 22 is nothing you
want to connect to either way. I got tired of connections from random places
on the globe connecting to my port 22 and I moved the SSH port to another port
in the 1-1024 scope. The tarpitssh package binds to 0.0.0.0 port 8022. You can
do the follwing on Linux machines:

> /usr/sbin/iptables -A FORWARD -p tcp -d 0.0.0.0 --dport 22 -m state --state NEW,ESTABLISHED,RELATED -j ACCEPT

> /usr/sbin/iptables -A PREROUTING -i eth0 -p tcp --dport 22 -j DNAT --to-destination &lt;your ip-address here&gt;:8022

And thing should work.

