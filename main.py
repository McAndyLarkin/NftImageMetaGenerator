import json
import random

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
#     #     data = sorted(data[0], key=lambda _: random.random()), data[1], data[2]
#     #     combinator.generateInvariants(image_template=path + 'images/' + exportname,
#     #                                   meta_template=path + 'metadata/' + exportname + "_meta_",
#     #                                   exp="png", maximum=1000, combinations=data)
#
#     combinator.generateInvariants(image_template=path + 'images/' + exportname,
#                                   meta_template=path + 'metadata/' + exportname + "_meta_",
#                                   exp="png", maximum=1000)
#

if __name__ == '__main__':
    launchWindow()
