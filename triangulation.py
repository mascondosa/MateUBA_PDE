import dmsh


class Triangulation:
    def __init__(self, points, cells):
        self.points = points
        self.simplices = cells
        self.neighbors = self.computeNeighbors()

    def computeNeighbors(self):
        Tneighbours = np.zeros([len(self.cells), 3]) - 1
        for i in range(len(self.cells)):
            cell = self.cells[i]
            for j in range(len(self.cells)):
                if j != i:
                    celln = self.cells[j]
                    if cell[0] in celln and cell[1] in celln:
                        Tneighbours[i, 0] = j
                        break
            for j in range(len(self.cells)):
                if j != i:
                    celln = self.cells[j]
                    if cell[0] in celln and cell[2] in celln:
                        Tneighbours[i, 1] = j
                        break
            for j in range(len(self.cells)):
                if j != i:
                    celln = self.cells[j]
                    if cell[2] in celln and cell[1] in celln:
                        Tneighbours[i, 2] = j
                        break
        return Tneighbours


def polygonTriangulation(borderPoints, edge_size):
    points, cells = dmsh.generate(dmsh.Polygon(borderPoints), edge_size)
    return Triangulation(points, cells)


def sartenTriangulation(size, edge_size):
    c = dmsh.Circle([0, 0], size)
    r = dmsh.Rectangle(-2.5*size, -size*0.9, -size/8, size/8)

    geo = dmsh.Union([c, r])
    points, cells = dmsh.generate(geo, edge_size)
    return Triangulation(points, cells)
