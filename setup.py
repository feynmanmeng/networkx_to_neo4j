from setuptools import setup, find_packages

VERSION = '0.0.3'
DESCRIPTION = 'networkx_to_neo4j'

'''
python setup.py bdist_wheel sdist
pip uninstall networkx-to-neo4j --yes
pip install dist/networkx_to_neo4j-0.0.3-py3-none-any.whl
'''

setup(
    name="networkx-to-neo4j",  # 包名称
    version=VERSION,  # 包名称
    author="feynman.meng",  # 程序的作者
    author_email="feynman.meng@gmail.com",  # 程序的作者的邮箱地址
    description=DESCRIPTION,  # 程序的简单描述
    # long_description_content_type="text/markdown",  # 程序的详细描述
    # long_description=open('README.md', encoding="UTF8").read(),
    packages=find_packages(),  # 需要处理的包目录（通常为包含init.py的文件央）
    install_requires=['networkx','neo4j','py2neo'],  # 程序运行所依赖的包
    keywords=['a', 'aa', 'aaa'],  # 程序的关键字列表
    url="xxxxx",  # 程序的官网地址
    license="MIT",  # 程序的授权信息

    # data_files=[('cut_video', ['cut_video/clip_to_erase.json'])], # 程序的数据文件列表

    # entry_points={
    # 'console_scripts': [
    #     'cut_video = cut_video.main:main'
    # ]
    # }, # 动态发现服务和插件，下面详细讲

    # scripts=['cut_video/cut_video.py'],  # 指定可执行脚本，安装时脚本会被安装到系统 PATH 路径下

    # classifiers=[
    #     "Development Status :: 3 - Alpha",
    #     "Intended Audience :: Developers",
    #     "Programming Language :: Python :: 3",
    #     "Operating System :: Microsoft :: Windows"
    # ]  # 程序的所属分类列表
)
