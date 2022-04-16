import json
import random
import sys

from gui.repository import get_project_file_name
from image_combinations import ImageCombinator

from gui.window import launchWindow

# def main():
#     filename = "/Users/maksim/Pictures/Final_Snale_to_Generation_with_var_items.psd"
#     # filename = "/Users/maksim/Pictures/max_proj.psd"
#     exportname = "Turbo Snail #"
#
#     combinator = ImageCombinator(filename)
#     # combinator.export("/Users/maksim/Pictures/" + exportname + "full" + ".png")
#
#     top = combinator.getTopGroups()
#
#     print(*top, sep='\n', end="\n\n")
#
#     print("Max , layers -- ", *combinator.getAllLayers(), sep="\n", end="\n\n")
#
#     # combinator.hideDirectlyByOrder([1,2,3,4,5])
#     # combinator.hideDirectlyById([80, 58])
#     # combinator.hideDirectlyByName(["Poster 3"])
#
#     combinator.setCombinable([i[0] for i in top])
#
#     path = "/Users/maksim/Pictures/nfts/"
#
#
#     # print(
#     #     *[str(combination) for combination in combinator.generateInvariants(exportname, "png")],
#     #     sep='\n', end="\n\n")
#     # PSDImage.new().
#
#     # with open("/Users/maksim/Pictures/cloud.json", 'r+') as file:
#     #     data = json.load(file)
#     #     print("combos", len(data[0]))
#     #     combinator.generateInvariants(image_template=path + 'images/' + exportname,
#     #                                   meta_template=path + 'metadata/' + exportname + "_meta_",
#     #                                   exp="png", maximum=1000, combinations=data)
#
#     combinator.generateInvariants(image_template=path + 'images/' + exportname,
#                                   meta_template=path + 'metadata/' + exportname + "_meta_",
#                                   exp="png", maximum=1000)
#
def launch(argv):
    if len(argv) <= 1:
        launchWindow()
    else:
        with open(argv[1], 'r') as file:
            config = json.load(file)
        if config is not None:
            mode = config["mode"]
            cloud = config["cloud"]
            source = config["source"]
            destiny = config["destiny"]
            name = config["name"]
            meta = config["meta"]
            count = int(config["count"])

            if source is None:
                print("Pizdec")
                return

            combinator = ImageCombinator(source)

            combinations = None

            if (mode == "calc" or mode is None) and source is not None and destiny is not None and name is not None:
                top = combinator.getTopGroups()
                print("Groups:", *top, sep='\n', end="\n\n")
                print("All layers -- ", *combinator.getAllLayers(), sep="\n", end="\n\n")

                combinator.setCombinable([i[0] for i in top])

                combinations, file = combinator.getCombinations(count, print, save_file_path=destiny, config={
                        "Source": source,
                        "GenName": name
                    })

            if mode == "gen" or mode is None:
                if combinations is None and cloud is not None:
                    with open(cloud, "r") as f:
                        combinations = json.load(f)["Combos"], -1, -1

                if combinations is not None and name is not None and destiny is not None \
                        and name is not None and meta is not None:
                    combinations = combinations[0]

                    export_name = get_project_file_name(content={
                        "Source": source,
                        "Generation": name,
                        "Count": len(combinations)
                    })
                    path = destiny + '/' + export_name + '/'

                    combinator.generateImages(combinations=combinations, image_template=name + '_n',
                                              path=path, exp="png",
                                              maximum=len(combinations), prepared_meta=meta, updateMsg=print)



if __name__ == '__main__':
    launch(sys.argv)