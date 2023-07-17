from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from sw_vectorize.config.ConfigStore import *
from sw_vectorize.udfs.UDFs import *

def Reformat_1(spark: SparkSession, in0: DataFrame) -> DataFrame:
    return in0.select(
        col("page_id"), 
        col("page_last_update"), 
        col("section_num"), 
        concat(lit("sw:"), col("page_id"), lit("-"), col("section_num"), lit(":"), col("chunk_window")).alias("doc_id"), 
        concat(lit("From: "), col("section_name"), lit(":\n\n"), concat_ws("\n", col("text_chunks")))\
          .alias("chunk_text")
    )
