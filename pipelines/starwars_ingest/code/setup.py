from setuptools import setup, find_packages
setup(
    name = 'starwars_ingest',
    version = '1.0',
    packages = find_packages(include = ('starwars_ingest*', )) + ['prophecy_config_instances'],
    package_dir = {'prophecy_config_instances' : 'configs/resources/config'},
    package_data = {'prophecy_config_instances' : ['*.json', '*.py', '*.conf']},
    description = 'workflow',
    install_requires = [
'prophecy-spark-ai==0.1.7', 'mwparserfromhell==0.6.4', 'wikitextparser==0.53.0', 'prophecy-libs==1.5.6'],
    entry_points = {
'console_scripts' : [
'main = starwars_ingest.pipeline:main'], },
    data_files = [(".prophecy", [".prophecy/workflow.latest.json"])],
    extras_require = {
'test' : ['pytest', 'pytest-html'], }
)
