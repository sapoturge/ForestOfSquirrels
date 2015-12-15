import os


class Item(object):
    items = []
    categories = {}

    def __init__(self, filename):
        with open(filename) as itemfile:
            self.name = itemfile.readline().strip()
            self.image = itemfile.readline().strip()
            for line in itemfile.readlines():
                if line.startswith("USE:"):
                    self.use = line[4:].strip()
                elif line.startswith("CATEGORY:"):
                    self.category = line[9:].strip()
                elif line.startswith("PRICE:"):
                    self.category = line[6:].strip()
                    if not self.category in Item.categories:
                        Item.categories[self.category] = []
                    Item.categories[self.category].append(self)
                elif line.startswith("WEAR:"):
                    self.wearable = bool(line[5:].strip())
        Item.items.append(self)


if not Item.items:
    path, dirs, files = os.walk("forestofsquirrels/items").next()
    for item in files:
        Item(os.path.join(path, item))
