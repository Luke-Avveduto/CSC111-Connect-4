import numpy as np
from scipy.signal import convolve2d
import matplotlib.pyplot as plt
import networkx as nx
import random
from networkx.drawing.nx_agraph import write_dot, graphviz_layout

# G = nx.DiGraph()
#
# G.add_node("ROOT")
#
# for i in range(5):
#     G.add_node("Child_%i" % i)
#     G.add_node("Grandchild_%i" % i)
#     G.add_node("Greatgrandchild_%i" % i)
#
#     G.add_edge("ROOT", "Child_%i" % i)
#     G.add_edge("Child_%i" % i, "Grandchild_%i" % i)
#     G.add_edge("Grandchild_%i" % i, "Greatgrandchild_%i" % i)

# write dot file to use with graphviz
# run "dot -Tpng test.dot >test.png"


# same layout using matplotlib with no labels



def hierarchy_pos(G, root=None, width=1., vert_gap=0.2, vert_loc=0, xcenter=0.5):
    '''
    From Joel's answer at https://stackoverflow.com/a/29597209/2966723.
    Licensed under Creative Commons Attribution-Share Alike

    If the graph is a tree this will return the positions to plot this in a
    hierarchical layout.

    G: the graph (must be a tree)

    root: the root node of current branch
    - if the tree is directed and this is not given,
      the root will be found and used
    - if the tree is directed and this is given, then
      the positions will be just for the descendants of this node.
    - if the tree is undirected and not given,
      then a random choice will be used.

    width: horizontal space allocated for this branch - avoids overlap with other branches

    vert_gap: gap between levels of hierarchy

    vert_loc: vertical location of root

    xcenter: horizontal location of root
    '''
    if not nx.is_tree(G):
        raise TypeError('cannot use hierarchy_pos on a graph that is not a tree')

    if root is None:
        if isinstance(G, nx.DiGraph):
            root = next(
                iter(nx.topological_sort(G)))  # allows back compatibility with nx version 1.11
        else:
            root = random.choice(list(G.nodes))

    def _hierarchy_pos(G, root, width=1., vert_gap=0.2, vert_loc=0.0, xcenter=0.5, pos=None,
                       parent=None):
        '''
        see hierarchy_pos docstring for most arguments

        pos: a dict saying where all nodes go if they have been assigned
        parent: parent of this branch. - only affects it if non-directed

        '''

        if pos is None:
            pos = {root: (xcenter, vert_loc)}
        else:
            pos[root] = (xcenter, vert_loc)
        children = list(G.neighbors(root))
        if not isinstance(G, nx.DiGraph) and parent is not None:
            children.remove(parent)
        if len(children) != 0:
            dx = width / len(children)
            nextx = xcenter - width / 2 - dx / 2
            for child in children:
                nextx += dx
                pos = _hierarchy_pos(G, child, width=dx, vert_gap=vert_gap,
                                     vert_loc=vert_loc - vert_gap, xcenter=nextx,
                                     pos=pos, parent=root)
        return pos

    return _hierarchy_pos(G, root, width, vert_gap, vert_loc, xcenter)


# plt.title('draw_networkx')
# pos = hierarchy_pos(G, 'ROOT')
# nx.draw(G, pos=pos, with_labels=True, arrows=True)
# plt.show()

# board = [
#     [0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0],
#     [0, 0, 0, 0, 0, 0, 0],
#     [1, 1, 1, -1, 0, 0, 0],
# ]
#
# fast_board = np.array(board)
#
# horizontal_kernel = np.array([[1, 1, 1, 1]])
# vertical_kernel = np.transpose(horizontal_kernel)
# diag1_kernel = np.eye(4, dtype=np.uint8)
# diag2_kernel = np.fliplr(diag1_kernel)
# detection_kernels = [horizontal_kernel, vertical_kernel, diag1_kernel, diag2_kernel]
#
# # for kernel in detection_kernels:
# #     print(np.any(convolve2d(fast_board, kernel, mode='valid') == 4))
# #
# # print(fast_board.clip(min=0, max=1))
# # print(fast_board)
#
# print(diag1_kernel * -1)
