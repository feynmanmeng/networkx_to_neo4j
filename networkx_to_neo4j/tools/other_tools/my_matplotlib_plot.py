import matplotlib.pyplot as plt
import networkx as nx
import pandas as pd

from ..get_logger import logger

...
'''
# 从Pandas.DataFrame中导入
# https://www.osgeo.cn/networkx/reference/generated/networkx.convert_matrix.from_pandas_edgelist.html
G = nx.convert_matrix.from_pandas_edgelist(sub_df_edge, 'src', 'dst', ['timestamp','amount','issar'])
# 将networkx图转为DataFrame，以边的形式保存
df_edge_kcore = nx.convert_matrix.to_pandas_edgelist(G, 'src', 'dst')

4种类型：
| Networkx Class | Type       | Self-loops allowed | Parallel edges allowed |
| :------------- | :--------- | :----------------- | :--------------------- |
| Graph          | undirected | Yes                | No                     |
| DiGraph        | directed   | Yes                | No                     |
| MultiGraph     | undirected | Yes                | Yes                    |
| MultiDiGraph   | directed   | Yes                | Yes                    |


Layout:
    circular_layout：节点在一个圆环上均匀分布
    random_layout：节点随机分布
    shell_layout：节点在同心圆上分布
    spring_layout： 用Fruchterman-Reingold算法排列节点(多中心放射状)
    spectral_layout：根据图的拉普拉斯特征向量排列节
'''


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
        circular_layout：节点在一个圆环上均匀分布
        random_layout：节点随机分布
        shell_layout：节点在同心圆上分布
        spring_layout： 用Fruchterman-Reingold算法排列节点(多中心放射状)
        spectral_layout：根据图的拉普拉斯特征向量排列节

    '''
    plt.figure(dpi=dpi, figsize=figsize)

    # plt.rcParams['font.serif'] = ['Times New Roman']  # 用来正常显示中文标签

    if layout is None:
        pos = nx.spring_layout(G)
    elif layout == 'circular':
        pos = nx.circular_layout(G)
    elif layout == 'random':
        pos = nx.random_layout(G)
    elif layout == 'shell':
        pos = nx.shell_layout(G)
    elif layout == 'spectral':
        pos = nx.spectral_layout(G)
    elif layout == 'spring':
        pos = nx.spring_layout(G)
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
