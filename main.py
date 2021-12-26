from image_combinations import ImageCombinator
from psd_creation import getProjectFrom

def main():
    filename = "/Users/maksim/Pictures/max_proj.psd"
    exportname = "output_"

    combinator = ImageCombinator(filename)
    # combinator.export("/Users/maksim/Pictures/" + exportname + "full" + ".png")

    top = combinator.getTopGroups()

    print(*top, sep='\n', end="\n\n")

    print(*combinator.getAllLayers(), sep="\n", end="\n\n")

    # combinator.hideDirectlyByOrder([1,2,3,4,5])
    # combinator.hideDirectlyById([80, 58])
    # combinator.hideDirectlyByName(["Poster 3"])

    combinator.setCombinable([top[0][0], top[1][0], top[2][0]])

    path = "/Users/maksim/Pictures/max_proj_output/"

    combinator.generateInvariants(image_template=path + 'images/' + exportname + "image_",
                                  meta_template=path + 'metadata/' + exportname + "meta_",
                                  exp="png", maximum=10)

    # print(
    #     *[str(combination) for combination in combinator.generateInvariants(exportname, "png")],
    #     sep='\n', end="\n\n")
    # PSDImage.new().


if __name__ == '__main__':
    main()
    # psd = getProjectFrom(['/Users/maksim/Pictures/red_back.png', '/Users/maksim/Pictures/green_smile.png'])
    # psd.save('/Users/maksim/Pictures/fromImages.psd')
