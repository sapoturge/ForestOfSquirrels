import os


class Item(type):
    items = []
    categories = {}

    def __new__(mcs, filename):
        d = {}
        with open(filename) as itemfile:
            d['name'] = itemfile.readline().strip()
            d['image'] = itemfile.readline().strip()
            for line in itemfile.readlines():
                if line.startswith("USE:"):
                    d['use'] = line[4:].strip()
                elif line.startswith("CATEGORY:"):
                    d['category'] = line[9:].strip()
                elif line.startswith("PRICE:"):
                    d['price'] = line[6:].strip()
                elif line.startswith("WEAR:"):
                    d['wearable'] = bool(line[5:].strip())
        item = type.__new__(mcs, d['name'].replace(" ", ""), (object,), d)
        Item.items.append(item)
        if d['category'] not in Item.categories:
            Item.categories[d['category']] = []
        Item.categories[d['category']].append(item)


if not Item.items:
    path, dirs, files = os.walk("forestofsquirrels/items").next()
    for item in files:
        Item(os.path.join(path, item))

all_items = Item.items
categories = Item.categories
print categories.keys()
