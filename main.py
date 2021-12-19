from psd_tools import PSDImage
import os

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
        combinations = self.getCombinations()
        for i in range(len(combinations)):
            if i == maximum:
                break

            combo = combinations[i]
            for member in self.psd.descendants():
                if not member.is_group():
                    member.visible = combo.__contains__(member.layer_id)
                    if member.visible:
                        print("visible: ", member.name)

            export_name = "/Users/maksim/Pictures/" + export_template + str(i) + "." + exp
            print("export:" + export_name)
            path = "/".join(export_name.split('/')[:-1])
            if not os.path.exists(path):
                os.mkdir(path)
            self.export(export_name)

    def getCombinations(self):
        selected_groups = self.selected_groups
        selected_layers = self.selected_layers

        combinations = []

        if selected_groups is not None:
            count_variations = self.countVariations(selected_groups)
            print("Variations: ", count_variations)

            counter = [(0, len(group)) for group in selected_groups]

            k = 0
            step = 0

            while step < count_variations:
                for i in range(len(selected_groups)):
                    combinations.append([selected_groups[j][counter[j][0]].layer_id for j in range(len(selected_groups))])

                    if counter[i][0] == counter[i][1] - 1:
                        counter[i] = 0, counter[i][1]
                    else:
                        counter[i] = counter[i][0] + 1, counter[i][1]

                    step += 1
        return combinations


    def countVariations(self, groups):
        count = 1
        for group in groups:
            count *= len(group)

        return count

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


def main():
    filename = "/Users/maksim/Pictures/max_proj.psd"
    exportname = "max_proj_output/output_"

    combinator = ImageCombinator(filename)
    combinator.export("/Users/maksim/Pictures/" + exportname + "full" + ".png")

    top = combinator.getTopGroups()

    print(*top, sep='\n', end="\n\n")

    print(*combinator.getAllLayers(), sep="\n", end="\n\n")

    # combinator.hideDirectlyByOrder([1,2,3,4,5])
    # combinator.hideDirectlyById([80, 58])
    # combinator.hideDirectlyByName(["Poster 3"])

    combinator.setCombinable([top[0][0], top[1][0], top[2][0]])

    combinator.generateInvariants(exportname, "png")

    # print(
    #     *[str(combination) for combination in combinator.generateInvariants(exportname, "png")],
    #     sep='\n', end="\n\n")
    # PSDImage.new().


if __name__ == '__main__':
    main()
