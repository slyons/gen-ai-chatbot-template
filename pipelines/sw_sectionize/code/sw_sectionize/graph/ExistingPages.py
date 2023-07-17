from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from sw_sectionize.config.ConfigStore import *
from sw_sectionize.udfs.UDFs import *

def ExistingPages(spark: SparkSession, in0: DataFrame, in1: DataFrame, ) -> DataFrame:
    return in0\
        .alias("in0")\
        .join(
          in1.alias("in1"),
          ((col("in0.page_id") == col("in1.page_id")) & (col("in0.timestamp") > col("in1.last_update"))),
          "inner"
        )\
        .select(col("in0.page_content").alias("page_content"), col("in0.title").alias("title"), col("in0.page_id").alias("page_id"), col("in0.timestamp").alias("timestamp"))
