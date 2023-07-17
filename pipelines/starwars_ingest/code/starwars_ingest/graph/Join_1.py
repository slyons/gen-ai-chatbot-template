from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from starwars_ingest.config.ConfigStore import *
from starwars_ingest.udfs.UDFs import *

def Join_1(spark: SparkSession, in0: DataFrame, in1: DataFrame, ) -> DataFrame:
    return in0\
        .alias("in0")\
        .join(in1.alias("in1"), (col("in0.page_id") == col("in1.page_id")), "left_anti")\
        .select(col("in0.title").alias("title"), col("in0.page_id").alias("page_id"), col("in0.section_num").alias("section_num"), col("in0.section_name").alias("section_name"), col("in0.section_text").alias("section_text"))
