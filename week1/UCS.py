from week1.Algorithm import Algorithm


class UCS(Algorithm):
    NAME = "UC"
    count = 0

    def nextIteration(self):
        print(f"Iteration: {self.count}")
        if self.count != 100:
            self.count += 1
            return True
        else:
            self.count = 0
            return False

    def hasNextIteration(self):
        return self.count != 100