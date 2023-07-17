from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from sw_vectorize.config.ConfigStore import *
from sw_vectorize.udfs.UDFs import *

def rename(spark: SparkSession, in0: DataFrame) -> DataFrame:
    return in0.select(
        col("doc_id"), 
        col("page_id"), 
        col("page_last_update"), 
        col("section_num"), 
        col("openai_embedding").alias("embedding"), 
        col("chunk_text")
    )
