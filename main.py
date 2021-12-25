from image_combinations import ImageCombinator

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
