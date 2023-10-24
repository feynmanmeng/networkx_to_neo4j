import pandas
import time
import os

import py2neo
from tqdm import tqdm
from collections import defaultdict
from functools import partial
from py2neo import Node, Relationship, Graph, NodeMatcher, RelationshipMatcher
from multiprocessing import Pool as Pool


# from pathos.multiprocessing import ProcessingPool as Pool


# 查询节点
def match_node(graph, label, attrs):
    matcher = NodeMatcher(graph)
    return matcher.match(label).where(id=attrs["id"]).first()


def create_relationship(graph, label1, attrs1, label2, attrs2, r_label, r_attrs):
    n1 = match_node(graph, "ACCOUNT", attrs1)
    n2 = match_node(graph, "ACCOUNT", attrs2)
    if n1 is None or n2 is None:
        return False
    r = Relationship(n1, "TRANS", n2, **r_attrs)
    # graph.create(r)
    return r


# %
if __name__ == "__main__":
    # 连接数据库
    graph = Graph("neo4j://localhost:7695/", auth=("neo4j", "feynmanneo4j"), name="neo4j")
    # 清空数据库
    graph.delete_all()

    src_attrs = {"id": 1, "issar": True}
    src = Node("ACCOUNT", **src_attrs)
    graph.create(src)

    dst_attrs = {"id": 2, "issar": True}
    dst = Node("ACCOUNT", **dst_attrs)
    graph.create(dst)

    # MATCH (a1:ACCOUNT {id: 1})
    # MATCH (a2:ACCOUNT {id: 2})
    # CREATE (a1)-[:TRANS {amount: 100}]->(a2)

    src = match_node(graph, "ACCOUNT", src_attrs)
    dst = match_node(graph, "ACCOUNT", dst_attrs)

    e1_attrs = {"id": 1, "amount": 100}
    r1 = Relationship(src, "TRANS", dst, **e1_attrs)
    # graph.create(r1)
    # graph.run(
    #     "MATCH (a:ACCOUNT),(b:ACCOUNT) WHERE a.id = 1 AND b.id = 2 CREATE (a)-[r:TRANS {id:$id, amount:$amount}]->(b)",
    #     id=e1_attrs['id'], amount=e1_attrs['amount'])

    e2_attrs = {"id": 2, "amount": 200}
    r2 = Relationship(src, "TRANS", dst, **e2_attrs)
    # graph.create(r2)
    # graph.run(
    #     "MATCH (a:ACCOUNT),(b:ACCOUNT) WHERE a.id = 1 AND b.id = 2 CREATE (a)-[r:TRANS {id:$id, amount:$amount}]->(b)",
    #     id=e2_attrs['id'], amount=e2_attrs['amount'])




    print("end")


