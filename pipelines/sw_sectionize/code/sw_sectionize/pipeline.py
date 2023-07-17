from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from sw_sectionize.config.ConfigStore import *
from sw_sectionize.udfs.UDFs import *
from prophecy.utils import *
from sw_sectionize.graph import *

def pipeline(spark: SparkSession) -> None:
    df_sw_bronze_pagecontent_1 = sw_bronze_pagecontent_1(spark)
    df_sw_silver_sectionized_1 = sw_silver_sectionized_1(spark)
    df_ExistingPages = ExistingPages(spark, df_sw_bronze_pagecontent_1, df_sw_silver_sectionized_1)
    df_NewPages = NewPages(spark, df_sw_bronze_pagecontent_1, df_sw_silver_sectionized_1)
    df_UnionChanges = UnionChanges(spark, df_ExistingPages, df_NewPages)
    df_ParseSubsections = ParseSubsections(spark, df_UnionChanges)
    df_SectionNum = SectionNum(spark, df_ParseSubsections)
    df_SelectSection = SelectSection(spark, df_SectionNum)
    sw_silver_sectionized(spark, df_SelectSection)

def main():
    spark = SparkSession.builder\
                .config("spark.default.parallelism", "4")\
                .config("spark.sql.legacy.allowUntypedScalaUDF", "true")\
                .enableHiveSupport()\
                .appName("Prophecy Pipeline")\
                .getOrCreate()\
                .newSession()
    Utils.initializeFromArgs(spark, parse_args())
    spark.conf.set("prophecy.metadata.pipeline.uri", "pipelines/sw_sectionize")
    registerUDFs(spark)
    
    MetricsCollector.start(spark = spark, pipelineId = "pipelines/sw_sectionize")
    pipeline(spark)
    MetricsCollector.end(spark)

if __name__ == "__main__":
    main()
