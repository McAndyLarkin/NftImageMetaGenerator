from psd_tools import PSDImage
from counter import MultyDimCounter
import os
import random


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

    def generateInvariants(self, export_template="export", exp="png", maximum=float("inf")):
        combinations = []
        while(True):
            _combinations = self.getCombinations(int(maximum))

            print('Report:',
                  '\n\tDifference: ', _combinations[1],
                  '\n\tFound combinations: ', _combinations[2])
            if _combinations[1] > .2 and _combinations[2] < .9:
                print("-- Rebuild!")
            else:
                combinations = _combinations[0]
                break

        for i in range(len(combinations)):
            if i == maximum:
                break

            combo = combinations[i]
            for member in self.psd.descendants():
                if not member.is_group():
                    member.visible = combo.__contains__(member.layer_id)
                    if member.visible:
                        print("visible: ", member.name)

            export_name = "/Users/maksim/Pictures/" + export_template + str(i) \
                          + '_#' + str(int(combo[1] * 100)) + "." + exp
            print("export:" + export_name)
            path = "/".join(export_name.split('/')[:-1])
            if not os.path.exists(path):
                os.mkdir(path)
            self.export(export_name)

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

        while step < count_variations:
            for i in range(len(selected_groups)):
                if len(combinations) >= limit:
                    return combinations, 0, found_combinations / count_variations

                combination = []
                combination_shine = 0

                for j in range(len(selected_groups)):
                    layer = selected_groups[j][counter.get_counter()[j]]

                    if limit_coef < 1 and self.isShine(layer):
                        shine = self.getShine(layer)
                        print(layer.name, " - shine - ", shine)
                        combination_shine += shine
                    else:
                        print(layer.name, " - shine - 0")
                        combination_shine += 0
                    combination.append(layer.layer_id)

                print(combination)
                combination_shine /= len(combination)
                print("Combination shine - ", combination_shine)

                found_combinations += 1
                if limit_coef <= 1:
                    security_coeff = 5

                    difference = min(limit - len(combinations), len(lost_combinations))
                    if not self.getRandomBool(limit_coef * security_coeff) and self.getRandomBool(
                            combination_shine) and not self.getRandomBool((difference / limit) * security_coeff):
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