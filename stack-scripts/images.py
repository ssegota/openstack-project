#!/usr/bin/env python
from os import environ as env
import keystoneclient.v2_0.client as ksclient
import glanceclient.v2.client as glclient
from credentials import get_creds

try:
    keystone = ksclient.Client(**get_creds())
    glance_endpoint = keystone.service_catalog.url_for(service_type='image')
    glance = glclient.Client(glance_endpoint, token=keystone.auth_token)

except:
    print "Neuspjesna autentifikacija prema Glance"

try:
    # kreacija prve slike
    image_frontend = glance.images.create(name="ssegota_frontend_server",
    disk_format="qcow2",
    container_format="bare")
    # upload slike diska za prvu sliku
    glance.images.upload(image_frontend.id, open('ssegota_frontend.vdi', 'rb'))

except:
    print "Neuspjesna kreacija prve slike"

try:
    # kreacija druge
    image_hdfs = glance.images.create(name="ssegota_hdfs_server",
    disk_format="qcow2",
    container_format="bare")
    # upload slike diska za drugu sliku
    glance.images.upload(image_frontend.id, open('ssegota_hdfs.vdi', 'rb'))
except:
    print "Neuspjesna kreacija druge slike"