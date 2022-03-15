import csv


class DataSet:
    def __init__(self, fileName):
        self.data = self.readFile(fileName)

    def __len__(self):
        return len(self.data)

    def __getitem__(self, index):
        return self.data[index]

    def readFile(self, fileName):
        data = []

        with open(fileName, "r") as csvfile:

            for row in csv.DictReader(csvfile):
                data.append(row)

        return data
