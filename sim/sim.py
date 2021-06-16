import copy
import math
import random

from sim.draw import animate

def chunks(L, n): return [L[x: x+n] for x in range(0, len(L), n)]

class GraphSim():
  def __init__(self, agents=3, n=9):
    self.DEBUG = False
    self.n = n
    self.agents = [0 for x in range(agents)]
    self.edges = [[0 for x in range(self.n)] for x in range(self.n)]
    self.nodes = [1 for x in range(self.n)]

  def _print_stats(self):
    print('nodes', self.n)
    print('agents', self.agents)

  def _print_edges(self):
    for row in self.edges:
      print((' ').join([str(x) for x in row]))

  def _clean(self):
    self.rec = []
    moves = self._get_moves()
    while (not self._is_done()):
      self._choose_moves(moves)

  def _get_moves(self):
    return [[_ for _, v in enumerate(tmp) if v == 1] for tmp in self.edges]

  def _choose_moves(self, m):
    tmp = copy.deepcopy(self.nodes)
    xed = [[0 for x in range(self.n)] for x in range(self.n)]
    for i, v in enumerate(self.agents):
      w = random.choice(m[v])
      xed[v][w] = 1
      xed[w][v] = 1
      self.agents[i] = w
      self.nodes[w] = 0
    for i in [_ for _, v in enumerate(tmp) if v == 1]:
      for j in m[i]:
        if j not in self.agents and xed[i][j] == 0:
          self.nodes[j] = 1
    if self.DEBUG:
      self._print_graph()
    self.rec.append([copy.deepcopy(self.nodes), copy.deepcopy(self.agents)])

  def _is_done(self):
    return True if sum(self.nodes) == 0 else False

  def _print_graph(self):
    print('print function')

class GridSim(GraphSim):
  def __init__(self, agents=3, dim=[3,3]):
    super().__init__(agents=agents, n=math.prod(dim))
    if self.DEBUG:
      self._print_stats()
    self.dim = dim
    self.init_grid()

  def init_grid(self):
    for x in range(self.n):
      i = math.floor(x / self.dim[1])
      j = x % self.dim[1]
      self.edges[x][x] = 1
      if i > 0:
        r = x-self.dim[1]
        self.edges[r][x] = 1
        self.edges[x][r] = 1
      if i+1 < self.dim[0]:
        r = x + self.dim[1]
        self.edges[r][x] = 1
        self.edges[x][r] = 1
      if j+1 < self.dim[1]:
        self.edges[x][x+1] = 1
        self.edges[x+1][x] = 1
      if j > 0:
        self.edges[x][x-1] = 1
        self.edges[x-1][x] = 1

    if self.DEBUG:
      self._print_edges()
      self._print_graph()

    assert self._is_done() == False

  def _print_graph(self):
    r, c = self.dim
    for i in range(r):
      print(('').join([str(x) for x in self.nodes[i*c:(i+1)*c]]))

  def run(self):
    self._clean()
    self._post_process()

  def _post_process(self):
    for i, v in enumerate(self.rec):
      n = self.rec[i]
      for j in n[1]:
        n[0][j] = 2
      self.rec[i] = chunks(n[0], self.dim[1])
    animate(self.dim[0], self.rec[-10:])
