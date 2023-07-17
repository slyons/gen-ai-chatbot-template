from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from sw_update_vectordb.config.ConfigStore import *
from sw_update_vectordb.udfs.UDFs import *

def UpdateSections(spark: SparkSession, in0: DataFrame, in1: DataFrame, ) -> DataFrame:
    return in0\
        .alias("in0")\
        .join(
          in1.alias("in1"),
          ((col("in0.doc_id") == col("in1.doc_id")) & (col("in0.page_last_update") > col("in1.page_last_update"))),
          "inner"
        )\
        .select(col("in0.doc_id").alias("doc_id"), col("in0.page_id").alias("page_id"), col("in0.page_last_update").alias("page_last_update"), col("in0.section_num").alias("section_num"), col("in0.embedding").alias("embedding"), col("in0.chunk_text").alias("chunk_text"))
