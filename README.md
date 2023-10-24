# networkx_to_neo4j

将networkx中的图导入到neo4j。



示例：

```python
import networkx as nx

from networkx_to_neo4j.auto_loader import AutoLoader

USERNAME = 'neo4j' # 一般默认都是这个
PASSWORD = 'xxxx' # 在neo4j中创建DBMS的时候要求输入一个超过8位密码
DATABASE = 'neo4j' # 默认数据库
PORT = '1234' # 找这个server.bolt.listen_address=:1234

G = nx.MultiDiGraph()
G.add_edges_from(
    [(1, 2, {'weight': 0}),
     (1, 2, {'weight': 1}),
     (1, 2, {'weight': 2}),
     (4, 1, {'weight': 0}),
     (2, 3, {'weight': 0}),
     (3, 4, {'weight': 0})]
)
al = AutoLoader()
# 导入数据
al.connect_to_neo4j(username=USERNAME, password=PASSWORD, database=DATABASE, port=PORT)
al.load_to_neo4j(G=G)
# 查询节点1和2之间的所有边
cypher = ("match relationships=(n1)--(n2) "
          "where n1.id=1 and n2.id=2 "
          "return relationships")
res = al.run_cyhper(cypher, ret_data=True)


assert str(res) == "[{'relationships': Path(Node('ACCOUNT', id=1), TRANS(Node('ACCOUNT', id=1), Node('ACCOUNT', id=2), weight=2))}, {'relationships': Path(Node('ACCOUNT', id=1), TRANS(Node('ACCOUNT', id=1), Node('ACCOUNT', id=2), weight=1))}, {'relationships': Path(Node('ACCOUNT', id=1), TRANS(Node('ACCOUNT', id=1), Node('ACCOUNT', id=2), weight=0))}]"
```

```
2023-10-24 20:35:58,523 INFO auto_loader.py [line:35] 连接成功
2023-10-24 20:36:01,603 INFO auto_loader.py [line:79] 从nx.MultiDiGraph导入
2023-10-24 20:36:01,608 INFO auto_loader.py [line:87] 计划导入数据：
2023-10-24 20:36:01,610 INFO auto_loader.py [line:88] 节点数量：4
2023-10-24 20:36:01,611 INFO auto_loader.py [line:89] 边数量：6
2023-10-24 20:36:01,611 INFO auto_loader.py [line:90] 总数量：10
2023-10-24 20:36:01,621 INFO neo4j_clear.py [line:13] 【已清空】
4it [00:00, 3997.43it/s]
2023-10-24 20:36:01,960 INFO neo4j_add_nodes.py [line:41] thread: t111 is processing... 0 left
2023-10-24 20:36:01,992 INFO neo4j_add_nodes.py [line:122] 退出主线程
2023-10-24 20:36:01,992 INFO neo4j_add_nodes.py [line:125] 【节点导入】耗时：0.3694896697998047 s
6it [00:00, 11881.88it/s]
thread: t123 is processing... 0 left
2023-10-24 20:36:02,359 INFO neo4j_add_edges.py [line:154] 退出主线程
2023-10-24 20:36:02,359 INFO neo4j_add_edges.py [line:157] 【边导入】耗时：0.3656890392303467 s
2023-10-24 20:36:02,359 INFO auto_loader.py [line:101] 导入流程结束
```

