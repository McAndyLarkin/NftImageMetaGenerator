from psd_tools import PSDImage
from counter import MultyDimCounter
import os
import random
import json


class ImageCombinator:
    def __init__(self, file_name):
        self.file = None
        self.psd = None
        self.ids = None

        self.selected_layers = []
        self.selected_groups = []

        self.openPsd(file_name)

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
                    print(member.name, "group", *member.descendants())
                    self.selected_groups.append(member)
                else:
                    print(member.name, "layer")
                    self.selected_layers.append(member)

    def generateInvariants(self, image_template="export", meta_template="meta", exp="png", maximum=float("inf")):
        while(True):
            combinations_with_report = self.getCombinations(int(maximum))

            print('Report:',
                  '\n\tDifference: ', combinations_with_report[1],
                  '\n\tFound combinations: ', combinations_with_report[2])
            if combinations_with_report[1] > .2 and combinations_with_report[2] < .9:
                print("-- Rebuild!")
            else:
                combinations = combinations_with_report[0]
                break

        for i in range(len(combinations)):
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

            export_name = image_template + str(N) + '#' + str(absolute_shine) + "." + exp
            print("export:" + export_name)
            img_path = "/".join(export_name.split('/')[:-1]) + '/'
            meta_path = "/".join(meta_template.split('/')[:-1]) + '/'
            if not os.path.exists(img_path):
                os.mkdir(img_path)
            if not os.path.exists(meta_path):
                os.mkdir(meta_path)
            print('metadata:', metadata)
            print("img_path = ", img_path)
            print("meta_path = ", meta_path)
            self.export(export_name)

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

            metadata = {
                "name": "Snail №" + str(N),
                "description": "Snails collection",
                "seller_fee_basis_points": 1000,#1000 - 10%
                "external_url": 1000,#https - project site adress
                "edition": N,
                "collection": {
                    "name": "Snail",
                    "family": "Snails Party"
                },
                "image": export_name,
                "attributes": metadata,
                "properties": {
                    "creators": {
                        "address": "",  #cryptowallet
                        "share": 100
                    }
                },
                "compiler": "MCAL"
            }
            self.save_meta(metadata, meta_template + str(N))

    def getCombinations(self, limit: int):
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
        print(absolute_groups_max_and_min_shine)

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
                        absolute_shine = self.getShine(layer)
                        absolute_min_shine = absolute_groups_max_and_min_shine[group.layer_id]['min']
                        absolute_max_shine = absolute_groups_max_and_min_shine[group.layer_id]['max']

                        max_shine = absolute_max_shine - absolute_min_shine
                        shine = absolute_shine - absolute_min_shine
                        shine = shine / max_shine
                        print(layer.name, " - shine - ", shine)
                        combination_shine['real'] += shine
                        combination_shine['absolute'] += absolute_shine
                    else:
                        print(layer.name, " - shine - 0")
                    combination.append(layer.layer_id)

                print(combination)
                combination_shine['real'] /= len(combination)
                combination_shine['absolute'] /= len(combination)
                print("Combination shine - ", combination_shine)

                found_combinations += 1
                if limit_coef <= 1:
                    security_coeff = 5

                    difference = min(limit - len(combinations), len(lost_combinations))
                    if not self.getRandomBool(limit_coef * security_coeff) and self.getRandomBool(
                            combination_shine['real']) and not self.getRandomBool((difference / limit) * security_coeff):
                        print("add right now")
                        combinations.append((combination, combination_shine))
                    else:
                        print("add to reserve")
                        lost_combinations.append((combination, combination_shine))
                else:
                    print("add right now")
                    combinations.append((combination, combination_shine))

                counter.increase()

                step += 1

        difference = min(limit - len(combinations), len(lost_combinations))
        print("difference -- ", difference)
        if difference > 0:
            # lost_combinations.sort(key=lambda combo: combo[1])
            random.shuffle(lost_combinations)
            for _ in range(difference):
                combinations.append(lost_combinations.pop(0))
        print("Found combinations: all")
        return combinations, difference / limit, 1


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
        print('priority_coef = ', priority_coef, rand)
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