import itertools

import numpy as np

from level_annotations import level_ab

def variations(img):
    for rot in range(4):  # add connections for all
        for _ in range(2):
            yield img
            img = np.fliplr(img)
        img = np.rot90(img)

class Image:
    def __init__(self, img_as_txt: str):
        name, *img = img_as_txt.split("\n")
        self.id = int(name.replace("Tile ", "")[:-1])
        self.img = (np.array([list(i) for i in img]) == '#').astype(int)
        self.corners = {tuple(var[0]) for var in variations(self.img)}
        self.neigh = set()
        self.pos_neigh = dict()
        self.visited = False

    def edge(self, i: complex) -> np.array:
        if i == -1:
            return self.img[0]
        elif i == 1:
            return self.img[-1]
        elif i == -1j:
            return self.img[:, 0]
        elif i == 1j:
            return self.img[:, -1]

    def visit(self, pos=None, must_match=None):
        if self.pos_neigh:
            return  # will bet set in visiting
        elif pos:  # rotate until we match
            for v in variations(self.img):
                self.img = v
                if (self.edge(pos) == must_match).all():
                    break
        for pos in [1j ** i for i in range(4)]:
            for neigh in self.neigh:
                if tuple(self.edge(pos)) in neigh.corners:
                    self.pos_neigh[-pos] = neigh
                    neigh.visit(-pos, must_match=self.edge(pos))

    def walk(self, direction: complex):
        yield self
        if direction in self.pos_neigh:
            yield from self.pos_neigh[direction].walk(direction)

@level_ab(20, sep="\n\n")
def solve(data, method=0):
    images = [Image(img_as_txt) for img_as_txt in data]
    for curr, other in itertools.permutations(images, 2):
        if set(curr.corners).intersection(other.corners):
            curr.neigh.add(other)
    if not method:
        images = sorted(images, key=lambda i: len(i.neigh))
        return np.prod([i.id for i in images[:4]])
    center = max(images, key=lambda img: len(img.neigh))
    center.visit()
    top_left = list(list(center.walk(1))[-1].walk(1j))[-1]
    field = np.vstack([np.hstack([row.img[1:-1, 1:-1] for row in col.walk(-1j)]) for col in top_left.walk(-1)])
    monster = """                  # 
#    ##    ##    ###
 #  #  #  #  #  #   """
    mask = (np.array([list(line) for line in monster.split("\n")]) == "#").astype(int)

    for fieldv in variations(field):  # for all field-variations and mask shifts
        fcnt = 0
        fx, fy = field.shape
        mx, my = mask.shape
        for i, j in itertools.product(range(fx - mx), range(fx - my)):
            fcnt += (fieldv[i:i + mx, j:j + my] & mask == mask).all()
        if fcnt:
            return fieldv.sum() - mask.sum() * fcnt
