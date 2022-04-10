import datetime
import math
import time

from psd_tools import PSDImage
from counter import MultyDimCounter
import os
import random
import json
from hashlib import sha1

from gui.repository import save_cloud_content


class ImageCombinator:
    def __init__(self, file_name):
        self.file = None
        self.psd = None
        self.ids = None

        self.selected_layers = []
        self.selected_groups = []

        self.openPsd(file_name)

        self.layer_id_to_name_and_group_id = dict()
        self.group_id_to_name = dict()


    def openPsd(self, file_name):
        self.file = file_name
        self.psd = PSDImage.open(file_name)

    def reopenFile(self):
        self.psd = PSDImage.open(self.file)

    def export(self, export_name):
        self.psd.composite(force=True).save(export_name)

    def getAllLayers(self):
        layers = []
        for member in self.psd.descendants():
            layers.append((member.layer_id, member.name))
        return layers

    def getTopLayers(self):
        free_layers = []
        for member in self.psd:
            entity = (member.layer_id, member.name)
            if not member.is_group():
                free_layers.append(entity)
        return free_layers

    def getTopGroups(self):
        groups = []
        for member in self.psd:
            entity = (member.layer_id, member.name)
            if member.is_group():
                groups.append(entity)
        return groups

    def hideDirectlyByName(self, layer_names):
        for layer in self.psd.descendants():
            if layer_names.__contains__(layer.name):
                layer.visible = False

    def hideDirectlyById(self, layer_ids):
        for layer in self.psd.descendants():
            if layer_ids.__contains__(layer.layer_id):
                layer.visible = False

    def hideDirectlyByOrder(self, orders):
        for order in orders:
            self.psd.descendants[order].visible = False

    def setCombinable(self, ids_list):
        for member in self.psd:
            if ids_list.__contains__(member.layer_id):
                if member.is_group():
                    self.selected_groups.append(member)
                else:
                    self.selected_layers.append(member)
        self.fill_id_to_name()

    def generateImages(self, combinations, image_template, meta_template, exp, maximum, updateMsg, meta={}):
        print("generateImages for: ", combinations)
        for i in range(len(combinations)):
            updateMsg("Generating .. {}%".format(round((i / len(combinations)) * 100, 1)))
            if i == maximum:
                break

            metadata = []

            combo = combinations[i]
            print('combination: ', combo)
            for member in self.psd.descendants():
                if not member.is_group():
                    member.visible = combo[0].__contains__(member.layer_id)
                    if member.visible:
                        print("visible: ", member.name)
                        metadata.append(
                            {
                                'trait_type': member.parent.name,
                                'value': member.name
                            }
                        )
            N = i+1

            real_shine = int(combo[1]['real'] * 100)
            absolute_shine = int(combo[1]['absolute'] * 100)

            export_name = image_template + str(N) + "." + exp
            # print("export:" + export_name)
            img_path = "/".join(export_name.split('/')[:-1]) + '/'
            meta_path = "/".join(meta_template.split('/')[:-1]) + '/'
            if not os.path.exists(img_path):
                os.makedirs(img_path)
            if not os.path.exists(meta_path):
                os.makedirs(meta_path)
            # print('metadata:', metadata)
            # print("img_path = ", img_path)
            # print("meta_path = ", meta_path)
            self.export(export_name)
            self.reopenFile()

            metadata.append(
                {
                    'trait_type': "real_shine",
                    'value': real_shine
                }
            )
            metadata.append(
                {
                    'trait_type': "absolute_shine",
                    'value': absolute_shine
                }
            )

            # metadata = {
            #     "dna": sha1(str(metadata.copy()).encode()).hexdigest(),
            #     "date": round(time.time() * 1000),
            #     "name": "Turbo Snail #" + str(N),
            #     "description": "A project for collecting turbo shells based on a cartoon character. The snail can be of different power and speed. Collect all the engines in the collection. Each picture gives you the right to be in the turbo community and participate in speed races.",
            #     "seller_fee_basis_points": 1000,#1000 - 10%
            #     "external_url": "https://twitter.com/SnailsTurbo",#https - project site adress
            #     "edition": N,
            #     "collection": {
            #         "name": "Turbo Snails",
            #         "family": "Turbo Snails"
            #     },
            #     "image": export_name,
            #     "attributes": metadata,
            #     "properties": {
            #         "creators": {
            #             "address": "0xeA816fec681cF3Bc3D36e167B6CE41628162f788",  #cryptowallet
            #             "share": 100
            #         }
            #     },
            #     "compiler": "MCAL"
            # }

            metadata = {
                "dna": sha1(str(metadata.copy()).encode()).hexdigest(),
                "date": round(time.time() * 1000),
                "edition": N,
                "image": export_name, # TODO need to update image
                "attributes": metadata,
            }
            if meta.keys().__contains__("name"):
                print("There is Name")
                metadata["name"] = meta["name"] + " #" + str(N)
            else:
                print("There is not Name")

            if meta.keys().__contains__("collection/name"):
                if not metadata.keys().__contains__("collection"):
                    metadata["collection"] = {}
                metadata["collection"]["name"] = meta["collection/name"]

            if meta.keys().__contains__("collection/family"):
                if not metadata.keys().__contains__("collection"):
                    metadata["collection"] = {}
                metadata["collection"]["family"] = meta["collection/family"]

            if meta.keys().__contains__("properties/creators/address"):
                if not metadata.keys().__contains__("properties"):
                    metadata["properties"] = {}
                if not metadata["properties"].keys().__contains__("creators"):
                    metadata["properties"]["creators"] = {}
                metadata["properties"]["creators"]["address"] = meta["properties/creators/address"]

            if meta.keys().__contains__("properties/creators/share"):
                if not metadata.keys().__contains__("properties"):
                    metadata["properties"] = {}
                if not metadata["properties"].keys().__contains__("creators"):
                    metadata["properties"]["creators"] = {}
                metadata["properties"]["creators"]["share"] = meta["properties/creators/share"]



            for meta_e_k, meta_e_v in meta.items():
                key_array = meta_e_k.split('/')
                if len(key_array) == 1:
                    metadata[key_array[0]] = meta_e_v
                elif len(key_array) > 1:
                    pass
                    # TODO Need to paste complex path metadata fields]


            self.save_meta(metadata, meta_template + str(N))

    def generateInvariants(self, image_template="export", meta_template="meta", exp="png", maximum=float("inf"), combinations = None, start=0, end=-1):
        # while(True):
        #     combinations_with_report = self.getCombinations(int(maximum))
        #
        #     print('Report:',
        #           '\n\tDifference: ', combinations_with_report[1],
        #           '\n\tFound combinations: ', combinations_with_report[2])
        #     if combinations_with_report[1] > .2 and combinations_with_report[2] < .9:
        #         print("-- Rebuild!")
        #     else:
        #         combinations = combinations_with_report[0]
        #         break

        if combinations is None:
            combinations = self.getCombinations(int(maximum))

            combinations = sorted(combinations[0], key=lambda _: random.random()), combinations[1], combinations[2]
            self.save_cloud(combinations[0])


        self.generateImages(combinations,image_template, meta_template, exp, maximum, start, end)

    def getCombinations(self, limit: int, updateProgressMsg):
        selected_groups = self.selected_groups
        selected_layers = self.selected_layers

        combinations = []
        lost_combinations = []
        found_combinations = 0

        assert selected_groups is not None

        count_variations = self.countVariations(selected_groups)
        limit_coef = limit / count_variations
        print("Variations: ", count_variations)

        counter = MultyDimCounter([(0, len(group)) for group in selected_groups], False)

        step = 0

        absolute_groups_max_and_min_shine = {}

        MAX_SHINE = 100

        for group in selected_groups:
            current_group_max_shine = 0
            current_group_min_shine = MAX_SHINE
            for layer in group:
                if self.isShine(layer):
                    current_group_max_shine = max(current_group_max_shine, self.getShine(layer))
                    current_group_min_shine = min(current_group_min_shine, self.getShine(layer))
            absolute_groups_max_and_min_shine[group.layer_id] = {
                'max': current_group_max_shine,
                'min': current_group_min_shine
            }

        saved = MultyDimCounter([(0, 10000)], False)

        while step < count_variations:
            for i in range(len(selected_groups)):
                if len(combinations) >= limit:
                    return combinations, 0, found_combinations / count_variations

                combination = []
                combination_shine = 0
                combination_shine = {
                    'absolute': 0,
                    'real': 0
                }

                for j in range(len(selected_groups)):
                    group = selected_groups[j]
                    layer = group[counter.get_counter()[j]]

                    if limit_coef < 1 and self.isShine(layer):
                        #85, 97
                        absolute_shine = self.getShine(layer)
                        absolute_min_shine = absolute_groups_max_and_min_shine[group.layer_id]['min']
                        absolute_max_shine = absolute_groups_max_and_min_shine[group.layer_id]['max']

                        max_shine = absolute_max_shine - absolute_min_shine
                        shine = absolute_shine - absolute_min_shine
                        # print(layer.layer_id)
                        if max_shine != 0:
                            shine = shine / max_shine
                        # print(layer.name, " - shine - ", shine)
                        combination_shine['real'] += shine
                        combination_shine['absolute'] += absolute_shine
                    else:
                        # print(layer.name, " - shine - 0")
                        pass
                    combination.append(layer.layer_id)

                # print(combination)]                                                                                       ----
                combination_shine['real'] /= len(combination)
                combination_shine['absolute'] /= len(combination)
                # print("Combination shine - ", combination_shine)

                found_combinations += 1
                if limit_coef <= 1:
                    security_coeff = 5

                    difference = min(limit - len(combinations), len(lost_combinations))
                    if not self.getRandomBool(limit_coef * 1.7) and self.getRandomBool(
                            combination_shine['real']) and not self.getRandomBool((difference / limit) * 1):
                        # print("add right now")
                        combinations.append((combination, combination_shine))
                    else:
                        # print("add to reserve")
                        lost_combinations.append((combination, combination_shine))
                else:
                    # print("add right now")
                    combinations.append((combination, combination_shine))
                saved.increase()
                if saved.get_counter()[0] == 1:
                    updateProgressMsg("Calculating .. {}%".format(round((found_combinations / count_variations) * 100, 1)))
                    print("I want - ", f"{(limit / count_variations):.{6}f}", "I have - ", f"{(len(combinations) / found_combinations):.{6}f}", "progress: ",
                          f"{((found_combinations / count_variations) * 100):.{3}f}", '%')

                counter.increase()

                step += 1

        print("Combinations generated: ", len(combinations))
        print("Lost combinations", len(lost_combinations))
        difference = min(limit - len(combinations), len(lost_combinations))
        print("Will be restored -- ", difference)

        if difference > 0:
            lost_combinations = sorted(lost_combinations, key=lambda _: random.random())
            for combin_n in range(0, difference):
                combinations.append(lost_combinations.pop(0))

        print("Found combinations:", len(combinations))
        return combinations, difference / limit, 1

    def save_cloud(self, combinations, configure, path):
        return save_cloud_content(path, self.prepare_cloud(combinations, configure), self.show_message)

    def show_message(msg):
        print(msg)

    def prepare_cloud(self, combinations, configure):
        invariants = dict()

        for group in self.selected_groups:
            invariants[group.name] = dict()
            for layer in group:
                invariants[group.name][layer.name] = 0

        for combo in combinations:
            for layer_id in combo[0]:
                member_data = self.layer_id_to_name_and_group_id[layer_id]
                member_group_name = self.group_id_to_name[member_data["group_id"]]
                member_name = member_data["name"]
                invariants[member_group_name][member_name] += 1

        combos_count = len(combinations)

        for gr_key in invariants:
            for lay_key in invariants[gr_key]:
                cnt = invariants[gr_key][lay_key]
                invariants[gr_key][lay_key] = {
                 "pieces": cnt,
                 "frequency": cnt / combos_count
              }

        now = datetime.datetime.now()
        return {
           "Count": combos_count,
           "Date": now.strftime("%d.%m.%Y %H:%M"),
           "Source": configure["Source"],
           "Generation": configure["GenName"],
           "Summary": invariants,
           "Combos": combinations
        }

    def countVariations(self, groups):
        count = 1
        for group in groups:
            count *= len(group)

        return count

    """
        Returns value that shows, how cool this layer, where 1 - very cool, 0 - very suck
    """
    def getShine(self, layer):
        return int(layer.name.split('#')[-1]) / 100

    def isShine(self, layer):
        name_array = layer.name.split('#')
        return len(name_array) > 1 and name_array[-1].isnumeric()

    def getRandomBool(self, aspect):
        epsilon = 10000
        rand = random.randint(0, epsilon)
        priority_coef = max(0, min(aspect * epsilon, epsilon))
        # print('priority_coef = ', priority_coef, rand)
        return rand >= priority_coef

    def save_meta(self, metadata, name):
        with open(name + ".json", "w") as write_file:
            json.dump(metadata, write_file)


        # selected_groups = self.selected_groups
        # selected_layers = self.selected_layers
        # for _ in range(len(selected_groups) + len(selected_layers)):
        #     if not (len(selected_groups) == 0):
        #         for _ in range(len(selected_groups.pop(0))):
        #             the_layer = []
        #
        #
        #     elif not (len(selected_layers) == 0):
        #         the_layer = selected_layers.pop(0)
        #         for _ in range(2):
        #             the_layer

    def fill_id_to_name(self):
        for group in self.selected_groups:
            self.group_id_to_name[group.layer_id] = group.name
            for layer in group:
                self.layer_id_to_name_and_group_id[layer.layer_id] = {
                    "name": layer.name,
                    "group_id": group.layer_id
                }
