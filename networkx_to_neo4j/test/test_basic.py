# @pytest.mark.parametrize("ensemble", [True, False])
import networkx as nx

from key import neo4j_connect_config
from networkx_to_neo4j.auto_loader import AutoLoader
from ..tools.other_tools.my_matplotlib_plot import plot_directed_with_plt

USERNAME = neo4j_connect_config['USERNAME']
PASSWORD = neo4j_connect_config['PASSWORD']
DATABASE = neo4j_connect_config['DATABASE']
PORT = neo4j_connect_config['PORT']

# 示例用图
G = nx.MultiDiGraph()
G.add_edges_from(
    [(1, 2, {'weight': 0}),
     (1, 2, {'weight': 1}),
     (1, 2, {'weight': 2}),
     (4, 1, {'weight': 0}),
     (2, 3, {'weight': 0}),
     (3, 4, {'weight': 0})]
)

def test_demo():
    al = AutoLoader()
    al.connect_to_neo4j(username=USERNAME, password=PASSWORD, database=DATABASE, port=PORT)
    assert 100 == 100


def test_networkx_to_neo4j():
    al = AutoLoader()
    # 导入数据
    al.connect_to_neo4j(username=USERNAME, password=PASSWORD, database=DATABASE, port=PORT)
    al.load_to_neo4j(G=G)
    # 查询节点1和2之间的所有边
    cypher = ("match relationships=(n1)--(n2) "
              "where n1.id=1 and n2.id=2 "
              "return relationships")
    res = al.run_cyhper(cypher, ret_data=True)
    assert str(
        res) == "[{'relationships': Path(Node('ACCOUNT', id=1), TRANS(Node('ACCOUNT', id=1), Node('ACCOUNT', id=2), weight=2))}, {'relationships': Path(Node('ACCOUNT', id=1), TRANS(Node('ACCOUNT', id=1), Node('ACCOUNT', id=2), weight=1))}, {'relationships': Path(Node('ACCOUNT', id=1), TRANS(Node('ACCOUNT', id=1), Node('ACCOUNT', id=2), weight=0))}]"

def test_plot_matplotlib():
    plot_directed_with_plt(G, layout='spring')