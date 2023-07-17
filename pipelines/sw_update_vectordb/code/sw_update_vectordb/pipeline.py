from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from sw_update_vectordb.config.ConfigStore import *
from sw_update_vectordb.udfs.UDFs import *
from prophecy.utils import *
from sw_update_vectordb.graph import *

def pipeline(spark: SparkSession) -> None:
    df_sw_gold_embeddings_2 = sw_gold_embeddings_2(spark)
    df_sw_gold_page_indexeddate_1 = sw_gold_page_indexeddate_1(spark)
    df_NewSections = NewSections(spark, df_sw_gold_embeddings_2, df_sw_gold_page_indexeddate_1)
    df_UpdateSections = UpdateSections(spark, df_sw_gold_embeddings_2, df_sw_gold_page_indexeddate_1)
    df_UnionIndexChanges = UnionIndexChanges(spark, df_UpdateSections, df_NewSections)
    df_Limit_1 = Limit_1(spark, df_UnionIndexChanges)
    df_IndexDate = IndexDate(spark, df_Limit_1)
    vector_db(spark, df_Limit_1)
    sw_gold_page_indexeddate(spark, df_IndexDate)

def main():
    spark = SparkSession.builder\
                .config("spark.default.parallelism", "4")\
                .config("spark.sql.legacy.allowUntypedScalaUDF", "true")\
                .enableHiveSupport()\
                .appName("Prophecy Pipeline")\
                .getOrCreate()\
                .newSession()
    Utils.initializeFromArgs(spark, parse_args())
    spark.conf.set("prophecy.metadata.pipeline.uri", "pipelines/sw_update_vectordb")
    registerUDFs(spark)
    
    MetricsCollector.start(spark = spark, pipelineId = "pipelines/sw_update_vectordb")
    pipeline(spark)
    MetricsCollector.end(spark)

if __name__ == "__main__":
    main()
