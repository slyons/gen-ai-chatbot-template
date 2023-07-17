from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from starwars_ingest.config.ConfigStore import *
from starwars_ingest.udfs.UDFs import *
from prophecy.utils import *
from starwars_ingest.graph import *

def pipeline(spark: SparkSession) -> None:
    df_sw_silver_sections_1 = sw_silver_sections_1(spark)
    df_sw_silver_embeddings_1 = sw_silver_embeddings_1(spark)
    df_Join_1 = Join_1(spark, df_sw_silver_sections_1, df_sw_silver_embeddings_1)
    df_chunkify = chunkify(spark, df_Join_1)
    df_RollingWindows = RollingWindows(spark, df_chunkify)
    df_SQLStatement_1 = SQLStatement_1(spark, df_RollingWindows)
    df_Reformat_1 = Reformat_1(spark, df_SQLStatement_1)
    df_vectorize = vectorize(spark, df_Reformat_1)
    df_clean = clean(spark, df_vectorize)
    df_rename = rename(spark, df_clean)
    sw_silver_embeddings(spark, df_rename)

def main():
    spark = SparkSession.builder\
                .config("spark.default.parallelism", "4")\
                .config("spark.sql.legacy.allowUntypedScalaUDF", "true")\
                .enableHiveSupport()\
                .appName("Prophecy Pipeline")\
                .getOrCreate()\
                .newSession()
    Utils.initializeFromArgs(spark, parse_args())
    spark.conf.set("prophecy.metadata.pipeline.uri", "pipelines/starwars_ingest")
    registerUDFs(spark)
    
    MetricsCollector.start(spark = spark, pipelineId = "pipelines/starwars_ingest")
    pipeline(spark)
    MetricsCollector.end(spark)

if __name__ == "__main__":
    main()
