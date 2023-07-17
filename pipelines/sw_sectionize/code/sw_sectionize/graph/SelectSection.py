from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from sw_sectionize.config.ConfigStore import *
from sw_sectionize.udfs.UDFs import *

def SelectSection(spark: SparkSession, in0: DataFrame) -> DataFrame:
    return in0.select(
        col("title"), 
        col("page_id"), 
        col("last_update"), 
        col("section_num"), 
        col("section")[0].alias("section_name"), 
        col("section")[1].alias("section_text")
    )
