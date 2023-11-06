import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

from ..get_logger import logger

def plot_directed_with_plt(
        G: {nx.Graph, nx.DiGraph, nx.MultiGraph, nx.MultiDiGraph},
        df_edges: pd.DataFrame = None,
        layout: str = None,
        dpi=300,
        figsize=(10, 8),
        node_size=60,
        node_shape='o',
        edge_width=0.5,
        font_size=6
):
    if df_edges is not None:
        if df_edges.shape[1] < 2:
            logger.error("df_edges should have at least 2 columns")
            return

        if 'src' or 'dst' not in df_edges.columns.values.tolist():
            logger.warning("df_edges should have columns named 'src' and 'dst', rename first two columns...")
            colnames = df_edges.columns.values.tolist()
            colnames[0] = 'src'
            colnames[1] = 'dst'
            df_edges.columns = colnames

        logger.info("df_edges will be converted to nx.MultiDiGraph")
        G = nx.convert_matrix.from_pandas_edgelist(df_edges, 'src', 'dst', create_using=nx.MultiDiGraph)

    # 绘图
    _plot_nx_mdg(G, layout, dpi, figsize, node_size, node_shape, edge_width, font_size)


def _plot_graph_multi(g):
    # 箭头指向有问题
    plt.figure()
    pos = nx.spring_layout(g)
    nx.draw_networkx_nodes(g, pos, node_color='black', node_size=100, alpha=1)
    ax = plt.gca()
    for e in g.edges:
        ax.annotate("",
                    xy=pos[e[0]], xycoords='data',
                    xytext=pos[e[1]], textcoords='data',
                    arrowprops=dict(arrowstyle="->", color="0.5",
                                    shrinkA=5, shrinkB=5,
                                    patchA=None, patchB=None,
                                    connectionstyle="arc3,rad=rrr".replace('rrr', str(0.3 * e[2])
                                                                           ),
                                    ),
                    )
    plt.axis('off')
    plt.show()


def _plot_nx_mdg(
        G: nx.MultiDiGraph,
        layout: str = None,
        dpi=300,
        figsize=(10, 8),
        node_size=60,
        node_shape='o',
        edge_width=0.5,
        font_size=4
):
    '''
    Layout:
        spring_layout
            弹簧布局算法是一种基于力导向的布局方法。它模拟了节点之间的弹簧和斥力，使得节点之间的距离趋于平衡，从而形成一个相对均匀的布局。
        circular_layout
            环形布局算法将节点按照圆形排列，使得节点之间的距离相等，节点在环上均匀分布。
        random_layout
            随机布局算法是一种简单的布局方法，它随机地将节点放置在图的平面上，没有特定的布局结构。
        shell_layout
            类似于环形布局的布局算法，但是节点会被分为多层。每一层都是一个环，节点按照环的顺序排列。
        kamada_kawai_layout
            基于牛顿迭代法的布局算法，它通过最小化节点之间的势能来确定节点的位置。该算法考虑了节点之间的连接关系和距离，以使得图的结构更加清晰。
        fruchterman_reingold_layout
            基于牛顿迭代法的布局算法，它通过模拟节点之间的斥力和弹簧力来确定节点的位置。该算法通过最小化节点之间的总能量来达到平衡状态。
        spectral_layout
            基于图的特征向量的布局算法，它使用图的拉普拉斯矩阵的特征向量来确定节点的位置。该算法考虑了节点之间的相似性和连接关系。
        planar_layout
            基于欧拉回路的平面布局算法，它将图投影到二维平面上，并保持节点之间的连接关系和边的交叉数最小化。该算法可以用于可平面图的布局。

    '''
    plt.figure(dpi=dpi, figsize=figsize)

    # plt.rcParams['font.serif'] = ['Times New Roman']  # 用来正常显示中文标签

    if layout is None:
        pos = nx.spring_layout(G)
    elif layout == 'spring':
        pos = nx.spring_layout(G)
    elif layout == 'circular':
        pos = nx.circular_layout(G)
    elif layout == 'random':
        pos = nx.random_layout(G)
    elif layout == 'shell':
        pos = nx.shell_layout(G)
    elif layout == 'kamada_kawai':
        pos = nx.kamada_kawai_layout(G)
    elif layout == 'fruchterman_reingold':
        pos = nx.fruchterman_reingold_layout(G)
    elif layout == 'spectral':
        pos = nx.spectral_layout(G)
    elif layout == 'planar':
        pos = nx.planar_layout(G)
    else:
        logger.error("wrong layout")
        return

    nx.draw_networkx_nodes(G,
                           pos,
                           # cmap=plt.get_cmap('jet'),  # https://blog.csdn.net/lly1122334/article/details/88535217
                           node_size=node_size,  # 600
                           node_color='lightblue',
                           node_shape=node_shape,  # 节点的形状（默认是圆形，用字符串'o'标识）
                           # alpha=0.1,
                           )  # 绘制节点
    # labels = g.
    nx.draw_networkx_labels(G,
                            pos,
                            # labels = labels,
                            font_size=font_size,  # 8
                            font_color='black'
                            )  # 节点label

    nx.draw_networkx_edges(G,
                           pos,
                           # edgelist=x,
                           edge_color='r',  # r
                           width=edge_width,  # weights,
                           arrows=True
                           )  # 绘制边，带箭头

    # edge_labels = dict()
    # for u, v, c in G.edges.data():
    #     edge_labels[(u, v)] = round(c['amount'], 1)
    #     # edge_labels[(u, v)] = c['step']
    # nx.draw_networkx_edge_labels(G,
    #                              pos,
    #                              edge_labels=edge_labels,
    #                              font_size=font_size, #6
    #                              # alpha=1
    #                              ) # 绘制图中边的权重

    # 去掉边框
    plt.axis('off')
    plt.tight_layout()
    plt.show()
