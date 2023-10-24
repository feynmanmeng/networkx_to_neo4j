import queue
import threading
import time
import traceback

from py2neo import NodeMatcher
from tqdm import tqdm

from .get_logger import logger

exitFlag = False
thread_lock = threading.Lock()
queue_work = queue.Queue()


class Py2Neo4j(threading.Thread):
    def __init__(self, graph, name, q: queue.Queue, n_label, r_label):
        threading.Thread.__init__(self)
        self.graph = graph
        self.name = name
        self.q = q
        self.n_label = n_label
        self.r_label = r_label

    def match_node(self, graph, label, attrs):
        '''
        在连接边之前首先检查两端的节点是否存在
        '''
        matcher = NodeMatcher(graph)
        return matcher.match(label).where(id=attrs["id"]).first()

    def write(self, graph, n_label, r_label, sub_r_attrs):
        for r_attrs in sub_r_attrs:
            # 使用 Relationship创建，存在无法创建多重边的问题
            # n_attrs1 = {'id': r_attrs['src']}
            # n_attrs2 = {'id': r_attrs['dst']}
            #
            # del r_attrs['src']
            # del r_attrs['dst']
            #
            # # 使用 graph.create创建
            # n1 = self.match_node(graph, n_label, n_attrs1)
            # n2 = self.match_node(graph, n_label, n_attrs2)
            # if n1 is None or n2 is None:
            #     return False
            # r = Relationship(n1, r_label, n2, **r_attrs)
            # graph.create(r)

            # 使用 cypher语句创建，可以创建多重边
            src_id = r_attrs['src']
            dst_id = r_attrs['dst']
            del r_attrs['src']
            del r_attrs['dst']

            _sig = "'"
            string_attr_dict = "{" + ", ".join(
                [f"{key}:{value if isinstance(value, (int, float, bool)) else _sig + value + _sig}" for key, value in
                 r_attrs.items()]) + "}"

            cyhper = f"MATCH (src:{n_label}),(dst:{n_label}) " \
                     f"WHERE src.id = {src_id} AND dst.id = {dst_id} " \
                     f"CREATE (src)-[r:{r_label} {string_attr_dict}]->(dst)"

            graph.run(cyhper)

    def process(self, thread_name, q: queue.Queue):

        while not exitFlag:
            thread_lock.acquire()
            if not queue_work.empty():
                sub_r_attrs = q.get()
                thread_lock.release()
                print("thread: {} is processing... {} left".format(thread_name, queue_work.qsize()))
                # 执行那个数据录入
                self.write(self.graph, self.n_label, self.r_label, sub_r_attrs)
            else:
                thread_lock.release()

    def run(self):
        global exitFlag
        try:
            self.process(self.name, self.q)
        except Exception as e:
            logger.error(traceback.format_exc())
            # 终止线程
            exitFlag = True


def gen_lst_data(nodes):
    lst_data = list()
    for i, row in tqdm(nodes.iterrows()):
        lst_data.append(row.to_dict())
    return lst_data


def sep_data(data, queue_work: queue.Queue, batch_size=50, src=0):
    '''
    将数据集分割成小块，并交给queue
    '''
    n_samples = len(data)
    src = 0
    dst = src + batch_size
    n_samples_left = n_samples - src
    while n_samples_left > 0:
        sub_data = data[src:dst]
        queue_work.put(sub_data)
        # 更新
        src += batch_size
        dst += batch_size
        n_samples_left -= batch_size

    return queue_work


def autorun_add_edges(graph, data, n_label='ACCOUNT', r_label='TRANS', n_thread=16, batch_size=50):
    global exitFlag
    global thread_lock
    global queue_work

    t1 = time.time()

    exitFlag = False

    # database = 'neo4j'
    # n_label = 'ACCOUNT'
    # n_thread = 200
    thread_name_list = ['t' + str(i) for i in list(range(0, n_thread))]

    # 启动线程，监视queue_work，只要里面有数据就会开始执行
    threads = []
    for thread_name in thread_name_list:
        thread = Py2Neo4j(graph, thread_name, queue_work, n_label, r_label)
        thread.start()
        threads.append(thread)

    # 要导入的数据
    # nodes = pandas.read_pickle(r'data/infomap_demo_nodes')

    # 转化为一条条样本
    lst_nodes = gen_lst_data(data)

    # 分割数据
    thread_lock.acquire()
    queue_work = sep_data(lst_nodes, queue_work, batch_size=batch_size)
    thread_lock.release()

    # 一直运行，直到所有数据全部导入
    while not queue_work.empty():
        exitFlag = True  # 正常终止所有线程

    # 等待所有线程完成
    for t in threads:
        t.join()
    logger.info("退出主线程")

    t2 = time.time()
    logger.info("【边导入】耗时：{0} s".format((t2 - t1) * 1))


# %%
if __name__ == '__main__':
    pass
    # while True:
    #     key = input()
    #     if key == 'q':
    #         flag_stop = True
    #         break
