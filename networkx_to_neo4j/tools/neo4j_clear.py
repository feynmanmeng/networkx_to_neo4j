import traceback

from .get_logger import logger


class NeoClear():
    def __init__(self, graph):
        self.graph = graph

    def process(self):
        # 清除neo4j里面的所有数据
        self.graph.delete_all()
        logger.info("【已清空】")


def autorun_clear(graph):
    is_success = True
    try:
        nc = NeoClear(graph)
        nc.process()
    except Exception as e:
        logger.error(traceback.format_exc())
        is_success = False
    finally:
        return is_success


# %%
if __name__ == '__main__':
    autorun_clear()
    pass
