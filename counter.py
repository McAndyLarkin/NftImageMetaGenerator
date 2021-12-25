
class MultyDimCounter:
    """
        Creates Multi dimension counter from pairs array.
        Dict (or pairs array) has to have pairs of start and finish values for each dimension.
    """
    def __init__(self, bounds: list, include_finish: bool):
        self.counter = [(dim[0], dim[0], dim[1]) for dim in bounds]
        self.include_finish = include_finish

    def increase(self):
        for i in range(len(self.counter)-1, -1, -1):
            if self.counter[i][1] + int(not self.include_finish) == self.counter[i][2]:
                self.counter[i] = self.counter[i][0], self.counter[i][0], self.counter[i][2]
            else:
                self.counter[i] = self.counter[i][0], self.counter[i][1] + 1, self.counter[i][2]
                break

    def get_counter(self):
        return [dim[1] for dim in self.counter]
