"""
networkx_to_neo4j
========

networkx_to_neo4j是一个将networkx.MultiDiGraph图导入neo4j数据库的python工具包。

使用详情见使用示例。
"""

from .tools.neo4j_clear import autorun_clear
from .tools.neo4j_add_nodes import autorun_add_nodes
from .tools.neo4j_add_edges import autorun_add_edges
from .tools.other_tools.my_matplotlib_plot import plot_directed_with_plt

__version__ = "0.0.4"

# 当其他模块使用 from module import * 导入模块时，只会导入 all 列表中指定的接口，而不会导入其他未在列表中的接口。
__all__ = [
    # autorun_clear,
    # autorun_add_nodes,
    # autorun_add_edges,
    plot_directed_with_plt,
]

# These are imported in order as listed
# from networkx_to_neo4j import tools
# from networkx_to_neo4j.tools import *


# from networkx.lazy_imports import _lazy_import
#
# from networkx.exception import *
#
# from networkx import utils
#
# from networkx import classes
# from networkx.classes import filters
# from networkx.classes import *
# from networkx.classes import _dispatch
#
# from networkx import convert
# from networkx.convert import *
#
# from networkx import convert_matrix
# from networkx.convert_matrix import *
