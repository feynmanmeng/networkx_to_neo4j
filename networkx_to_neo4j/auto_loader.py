import traceback

import networkx as nx
import pandas as pd
import py2neo
from my_networkx.convert import nx_to_nodes_edges
from py2neo import Graph

from tools.get_logger import logger
from tools.neo4j_add_edges import autorun_add_edges
from tools.neo4j_add_nodes import autorun_add_nodes
from tools.neo4j_clear import autorun_clear


class AutoLoader:
    '''
    说明：
     - 连接neo4j数据库
        connect_to_neo4j(username, password, database, port)

     - 将 G:nx.MultiDiGraph导入到neo4j数据库
        load_to_neo4j(G, nodes, edges, n_label, r_label, n_thread, batch_size)

     - 在neo4j中执行cyhper语句
        run_cyhper(cyhper, ret_data)
    '''

    def __init__(self):
        self.config = {
            'USERNAME': 'neo4j',
            'PASSWORD': 'Feynmanmeng',
            'DATABASE': 'neo4j',
            'PORT': '7442'
        }
        self.graph = None

    def run_cyhper(self, cyhper, ret_data=False):
        res = self.graph.run(cyhper)
        if ret_data:
            return res.data()
        else:
            return res

    def connect_to_neo4j(self, username, password, database, port):
        '''
        USERNAME = 'neo4j'
        PASSWORD = 'Feynmanmeng'
        DATABASE = 'neo4j'
        PORT = '7442'
        '''
        self.graph = Graph(f"neo4j://localhost:{port}/", auth=(username, password), name=database)
        try:
            self.graph.nodes.match().first()  # 测试连接
            logger.info('连接成功')
        except py2neo.errors.ServiceUnavailable as e:
            logger.error(traceback.format_exc())  # print("捕获到ServiceUnavailable异常:", e)
            logger.error('连接失败')
            return -1

        self.config = {
            'USERNAME': username,
            'PASSWORD': password,
            'DATABASE': database,
            'PORT': port
        }

    def load_to_neo4j(self, G: nx.MultiDiGraph = None, nodes: pd.DataFrame = None, edges: pd.DataFrame = None,
                      n_label='ACCOUNT', r_label='TRANS', n_thread=200, batch_size=50):
        '''
            说明：
                将 G:nx.MultiDiGraph在 Neo4j数据库中可视化
                将需要导入的全量数据拆分为多份，由不同线程去执行

            config = {
                'USERNAME': 'neo4j', # 一般默认都是这个
                'PASSWORD': 'xxxx', # 在neo4j中创建DBMS的时候要求输入一个超过8位密码
                'DATABASE': 'neo4j', # 默认数据库
                'PORT': '1234' # 找这个server.bolt.listen_address=:1234
            }

            要求：
                节点：第一列名字叫 id，其他属性
                边：第一列 src，第二列 dst，第三列建议是 id，其他属性

            连接：
                Gephi <- neo4j-import
                    neo4j://localhost:7687/
                    neo4j
                    neo4j
                    feynmanneo4j

            '''
        # 判断输入
        if isinstance(G, nx.MultiDiGraph):
            logger.info('从nx.MultiDiGraph导入')
            nodes, edges = nx_to_nodes_edges(G)
        elif isinstance(G, (nx.Graph, nx.DiGraph, nx.MultiGraph)):
            logger.info('从nx.Graph、nx.DiGraph或nx.MultiGraph导入，将其转换为nx.MultiDiGraph')
            G = nx.MultiDiGraph(G)
            nodes, edges = nx_to_nodes_edges(G)
        elif isinstance(nodes, pd.DataFrame) and isinstance(edges, pd.DataFrame):
            logger.info('从nodes edges的pandas.DataFrame导入')
            if nodes.columns[0] != 'id':
                logger.warning("建议nodes的第一列叫['id']")
            if edges.columns[0] != 'src' or edges.columns[1] != 'dst' or edges.columns[2] != 'id':
                logger.warning("建议edges的前三列分别叫['src', 'dst', 'id']")
        else:
            logger.error('输入数据格式错误')
            return

        logger.info('计划导入数据：')
        logger.info(f"节点数量：{G.number_of_nodes()}")
        logger.info(f"边数量：{G.number_of_edges()}")
        logger.info(f"总数量：{G.number_of_nodes() + G.number_of_edges()}")

        # 1. 清空数据库
        autorun_clear(self.graph)
        # 2. 加载节点
        autorun_add_nodes(self.graph, data=nodes,
                          n_label=n_label, r_label=r_label, n_thread=n_thread, batch_size=batch_size)
        # 3. 加载边
        autorun_add_edges(self.graph, data=edges,
                          n_label=n_label, r_label=r_label, n_thread=n_thread, batch_size=batch_size)

        logger.info(f'导入流程结束。\n'
                    f'计划导入节点数量：{G.number_of_nodes()}，实际导入节点数量：{self.graph.nodes.match().count()}\n'
                    f'计划导入边数量：{G.number_of_edges()}，实际导入边数量：{self.graph.relationships.match().count()}')
