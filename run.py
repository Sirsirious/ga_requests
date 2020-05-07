#! /usr/bin/env python3
import os
import requests
import argparse
from requests.exceptions import HTTPError

def do_request(url, data):
    response = requests.post(url, data=data)
    if response.status_code >= 400:
        raise HTTPError("Unable to post data correctily. Response code:{}".format(response.status_code))

def prepare_data(file_path):
    data = {}
    with open(file_path) as file:
        data['title'] = file.readline().replace('\n','')
        data['name'] = file.readline().replace('\n','')
        data['date'] = file.readline().replace('\n','')
        data['feedback'] = file.readline().replace('\n','')
    return data

parser = argparse.ArgumentParser(description='Reads files and sends them over server.')
parser.add_argument('files_path', metavar='path', type=str,
                   help='The path for the review files.')
parser.add_argument('ip_address', metavar='ip_address', type=str,
                   help='The ip address of the review server.')
parser.add_argument('-d', dest='debug', action='store_const', const=True,
                   help='Enables debug mode - no request sent, but data is printed to stdout instead.')
args = parser.parse_args()
files_path = args.files_path
server_ip = args.ip_address
debug = args.debug
files = os.listdir(files_path)
if debug:
    print("Debugging info - retrieved files:", files,"\n\n")
data = [prepare_data(files_path+"/"+file) for file in files]
url = 'http://'+server_ip+'/feedback'
if debug:
    print("Debugging info - retrieved data:", data,"\n\n")
for d in data:
    if debug:
        print("Debugging info - attempting to send data:", d,"\n")
    else:
        do_request(url, d)
