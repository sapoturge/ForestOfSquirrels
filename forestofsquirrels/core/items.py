import os


class ItemType(type):
    def __new__(mcs, name, bases, d):
        filename = d.get("filename", "null.item")
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
        return item


class Item(object):
    items = []
    categories = {}


class Acorn(Item):
    __metaclass__ = ItemType
    filename = os.path.abspath("forestofsquirrels/items/.base/acorn.item")


def create_item(filename):
    if "acorn" in filename:
        bases = (Acorn,)
    else:
        bases = (Item,)
    return ItemType("a", bases, {"filename": filename})


all_items = []
categories = {}
if not Item.items:
    path, dirs, files = os.walk("forestofsquirrels/items").next()
    for item in files:
        i = create_item(os.path.join(path, item))
        all_items.append(i)
        categories[i.category].append(i)
