from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from sw_vectorize.config.ConfigStore import *
from sw_vectorize.udfs.UDFs import *

def RollingWindows(spark: SparkSession, in0: DataFrame) -> DataFrame:
    return in0.select(
        col("title"), 
        col("page_id"), 
        col("page_last_update"), 
        col("section_num"), 
        col("section_name"), 
        col("section_text"), 
        rolling_arr_window(col("result_chunks"), lit(2)).alias("result_chunks_window")
    )
