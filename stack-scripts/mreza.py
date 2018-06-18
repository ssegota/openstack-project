#!/usr/bin/env python
from os import environ as env
import novaclient.client
from neutronclient.v2_0 import client as neutronclient
from credentials import get_creds, get_nova_creds

try:
    nova = novaclient.client.Client("2", **get_nova_creds())
    neutron = neutronclient.Client(**get_creds())
    network_name = 'ssegota_net'
except:
    print "Greska kod autentifikacije"

try:
    #net
    body_net = {'network': {'name': network_name,
                'admin_state_up': True}}
    netw = neutron.create_network(body=body_net)
    net_dict = netw['network']
    network_id = net_dict['id']
    print('Network %s created' % network_id)
    #subnet
    body_subnet = {'subnets': [{'name':'ssegota_subnet1',
                    'cidr':'10.20.1.0/24',
                    'ip_version': 4,
                    'dns_nameservers': ['8.8.4.4', '8.8.8.8'],
                    'network_id': network_id}]}
    
    subnet = neutron.create_subnet(body=body_subnet)
    print('\nCreated subnet %s\n' % subnet)

except:
    print "Greska kod stvaranja mreze"

try:
    public_network_id = nova.networks.find(label='public').id
    body_router = {'router': {'name': 'ssegota_router',
    'admin_state_up': True}}
    router = neutron.create_router(body=body_router)
    router_id = router['router']['id']
    body_port = {'port': {
                'admin_state_up': True,
                'network_id': network_id,
                'fixed_ips': [{"ip_address": "10.20.1.1"}]
    }}
    port = neutron.create_port(body=body_port)
    port_id = port['port']['id']
    neutron.add_gateway_router(router=router_id, body={"network_id":
    public_network_id})
    neutron.add_interface_router(router=router_id, body={"port_id": port_id})
    print("\nExecution Completed\n")
    
except:
    print "Greska kod stvaranja mreze"