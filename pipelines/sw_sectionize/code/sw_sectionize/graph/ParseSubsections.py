from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from sw_sectionize.config.ConfigStore import *
from sw_sectionize.udfs.UDFs import *

def ParseSubsections(spark: SparkSession, in0: DataFrame) -> DataFrame:
    return in0.select(
        parse_subsections(col("page_content"), col("title")).alias("sections"), 
        col("title"), 
        col("page_id"), 
        col("timestamp").alias("last_update")
    )
