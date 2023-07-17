from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from sw_vectorize.config.ConfigStore import *
from sw_vectorize.udfs.UDFs import *
from prophecy.utils import *
from sw_vectorize.graph import *

def pipeline(spark: SparkSession) -> None:
    df_sw_silver_sectionized = sw_silver_sectionized(spark)
    df_sw_gold_embeddings_1 = sw_gold_embeddings_1(spark)
    df_UpdateSections = UpdateSections(spark, df_sw_silver_sectionized, df_sw_gold_embeddings_1)
    df_NewSections = NewSections(spark, df_sw_silver_sectionized, df_sw_gold_embeddings_1)
    df_UnionSectionChanges = UnionSectionChanges(spark, df_UpdateSections, df_NewSections)
    df_chunkify = chunkify(spark, df_UnionSectionChanges)
    df_RollingWindows = RollingWindows(spark, df_chunkify)
    df_SQLStatement_1 = SQLStatement_1(spark, df_RollingWindows)
    df_Reformat_1 = Reformat_1(spark, df_SQLStatement_1)
    df_vectorize = vectorize(spark, df_Reformat_1)
    df_clean = clean(spark, df_vectorize)
    df_rename = rename(spark, df_clean)
    sw_gold_embeddings(spark, df_rename)

def main():
    spark = SparkSession.builder\
                .config("spark.default.parallelism", "4")\
                .config("spark.sql.legacy.allowUntypedScalaUDF", "true")\
                .enableHiveSupport()\
                .appName("Prophecy Pipeline")\
                .getOrCreate()\
                .newSession()
    Utils.initializeFromArgs(spark, parse_args())
    spark.conf.set("prophecy.metadata.pipeline.uri", "pipelines/sw_vectorize")
    registerUDFs(spark)
    
    MetricsCollector.start(spark = spark, pipelineId = "pipelines/sw_vectorize")
    pipeline(spark)
    MetricsCollector.end(spark)

if __name__ == "__main__":
    main()
