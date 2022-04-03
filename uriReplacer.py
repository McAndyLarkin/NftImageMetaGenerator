import sys
import os
import json

import counter
from hashlib import sha1
import time



def replace(path):
    dnas = set()
    CNTR = counter.MultyDimCounter([(0, 10000000)], False)
    print(len(os.listdir(path)))
    for item in os.listdir(path):
        with open(path + '/' + item, 'r+') as file:
            print(file.name)
            if not file.name.split('.')[-1] == 'json':
                continue
            data = json.load(file)

            external_url: str = "https://twitter.com/SnailsTurbo"
            description: str = "A project for collecting turbo shells based on a cartoon character. The snail can be of different power and speed. Collect all the engines in the collection. Each picture gives you the right to be in the turbo community and participate in speed races."
            collection_name: str = "Turbo Snails"
            collection_family: str = "Turbo Snails"
            image_url: str = "ipfs://QmcrWeYcwqsiAti8FD9vATdswEtq3QtSdf1MV3p25bgUM8"
            properties_creators_address: str = "0xeA816fec681cF3Bc3D36e167B6CE41628162f788"#cryptowallet

            dna = sha1(str(data['attributes'].copy()).encode()).hexdigest()
            print(dna)
            dnas.add(dna)
            data['dna'] = dna
            data['date'] = round(time.time() * 1000)
            data['image'] = image_url + '/' + '_'.join(''.join(data['image'].split('/')[-1].split('#')).split(' '))
            data['description'] = description
            data["collection"] = {
                    "name": collection_name,
                    "family": collection_family
                }
            data['external_url'] = external_url
            data['properties']['creators']['address'] = properties_creators_address
            # data['attributes'] = data['attributes'][:-2]

            file.seek(0)  # <--- should reset file position to the beginning.
            json.dump(data, file, indent=4)
            file.truncate()  # remove remaining parts
            CNTR.increase()
            #need to change: external_url, description, collection, image, address
    print(CNTR.get_counter())
    print(len(dnas))
paths = [
    # "/Users/maksim/NTF_Projects/NftTurboSnailsData/metadata/1thnd"
    # "/Users/maksim/NTF_Projects/NftTurboSnailsData/metadata/2thnd"
    # "/Users/maksim/NTF_Projects/NftTurboSnailsData/metadata/3thnd"
    # "/Users/maksim/NTF_Projects/NftTurboSnailsData/metadata/4thnd"
    # "/Users/maksim/NTF_Projects/NftTurboSnailsData/metadata/5thnd"
    "/Users/maksim/NTF_Projects/NftTurboSnailsData/metadata/full"
]
for path in paths:
    replace(path)
