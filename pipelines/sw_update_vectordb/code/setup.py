from setuptools import setup, find_packages
setup(
    name = 'sw_update_vectordb',
    version = '1.0',
    packages = find_packages(include = ('sw_update_vectordb*', )) + ['prophecy_config_instances'],
    package_dir = {'prophecy_config_instances' : 'configs/resources/config'},
    package_data = {'prophecy_config_instances' : ['*.json', '*.py', '*.conf']},
    description = 'workflow',
    install_requires = [
'prophecy-spark-ai==0.1.7', 'prophecy-libs==1.5.6'],
    entry_points = {
'console_scripts' : [
'main = sw_update_vectordb.pipeline:main'], },
    data_files = [(".prophecy", [".prophecy/workflow.latest.json"])],
    extras_require = {
'test' : ['pytest', 'pytest-html'], }
)
