import subprocess
import sys 
import json 
from copy import deepcopy  

img_path = sys.argv[1]
metadata_path = sys.argv[2]

print("img_path: ", img_path)

node_path = '/usr/bin/node'

jwt_token = 'eyJhbGciOiJIUzI1NiIsInR5cCI6IkpXVCJ9.eyJ1c2VySW5mb3JtYXRpb24iOnsiaWQiOiJlNGU0ZWJkMS1iNGNkLTQyODktYWJiZC02MWQzYmIyYjc0MTkiLCJlbWFpbCI6ImFuc2FyaW5mb3RlY2g0MUBnbWFpbC5jb20iLCJlbWFpbF92ZXJpZmllZCI6dHJ1ZSwicGluX3BvbGljeSI6eyJyZWdpb25zIjpbeyJpZCI6IkZSQTEiLCJkZXNpcmVkUmVwbGljYXRpb25Db3VudCI6MX1dLCJ2ZXJzaW9uIjoxfSwibWZhX2VuYWJsZWQiOmZhbHNlfSwiYXV0aGVudGljYXRpb25UeXBlIjoic2NvcGVkS2V5Iiwic2NvcGVkS2V5S2V5IjoiODkwODMzNzQ0OGIzYWMyYjI5ZmIiLCJzY29wZWRLZXlTZWNyZXQiOiI5Y2E3NjYzMDc0M2Y3ODgwYjdiYWM5YTQ4YjcwMzVmMTc0ZjQyZTlmNWZkYzYzMmU0ZWJjZDZkYWVmMzdiODYyIiwiaWF0IjoxNjQ1NjMzMzc5fQ.86c3mIusbfZGVXDMxt4W2vxyUkWHsAuSTZT122kUAL4'
base_metadata = json.load(open(metadata_path))
metadata_hashes = json.load(open('./metadata_hashes.json'))
metadata_hashes[img_path] = []

def pin_img_to_pinata(img_path):
    ipfs_hash = subprocess.check_output([f'{node_path}','./_pinImgToPinata.js', img_path])
    return ipfs_hash.decode().strip()

def pin_metadata_to_pinata(img_ipfs_hash, edition_index):
    metadata = deepcopy(base_metadata)
    metadata['image'] = base_metadata['image'] + img_ipfs_hash
    metadata['attributes'].append({'display_type': 'number', 'trait_type': 'Edition', 'max_value': 10, 'value': edition_index + 1})
    metadata_ipfs_hash = subprocess.check_output([node_path, './_pinMetadataToPinata.js', json.dumps(metadata), str(edition_index+1)])
    return metadata_ipfs_hash.decode().strip()

img_ipfs_hash = pin_img_to_pinata(img_path)

for i in range(0, base_metadata['total_editions']):
    metadata_hash = pin_metadata_to_pinata(img_ipfs_hash, i)
    metadata_hashes[img_path].append(metadata_hash)
    print(f'Edition: {i+1}; Metadata Hash: {metadata_hash}')

json.dump(metadata_hashes, open('./metadata_hashes.json', 'w'))
print("Done")
    