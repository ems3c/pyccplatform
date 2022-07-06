import requests
import urllib.parse
from urllib.parse import urlparse

def get_ngrok_info(ip):
  return requests.get(ip).json()

def get_url(ip):
    addr = 'http://' + str(ip) + ':4020/api/tunnels'
    url = get_ngrok_info(addr)
    ip_url =  url['tunnels'][0]['public_url']
    p = urlparse(ip_url)
    return 'ssh admin@'  + p.hostname + ' -p ' +  str(p.port)
