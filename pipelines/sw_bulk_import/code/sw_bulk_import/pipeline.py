from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from sw_bulk_import.config.ConfigStore import *
from sw_bulk_import.udfs.UDFs import *
from prophecy.utils import *
from sw_bulk_import.graph import *

def pipeline(spark: SparkSession) -> None:
    df_starwars_wiki_xml = starwars_wiki_xml(spark)
    df_OnlyPages = OnlyPages(spark, df_starwars_wiki_xml)
    df_OnlyPageContent = OnlyPageContent(spark, df_OnlyPages)
    sw_bronze_pagecontent(spark, df_OnlyPageContent)

def main():
    spark = SparkSession.builder\
                .config("spark.default.parallelism", "4")\
                .config("spark.sql.legacy.allowUntypedScalaUDF", "true")\
                .enableHiveSupport()\
                .appName("Prophecy Pipeline")\
                .getOrCreate()\
                .newSession()
    Utils.initializeFromArgs(spark, parse_args())
    spark.conf.set("prophecy.metadata.pipeline.uri", "pipelines/sw_bulk_import")
    registerUDFs(spark)
    
    MetricsCollector.start(spark = spark, pipelineId = "pipelines/sw_bulk_import")
    pipeline(spark)
    MetricsCollector.end(spark)

if __name__ == "__main__":
    main()
