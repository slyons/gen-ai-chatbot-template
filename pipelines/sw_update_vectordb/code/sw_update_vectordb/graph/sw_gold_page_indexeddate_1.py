from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from sw_update_vectordb.config.ConfigStore import *
from sw_update_vectordb.udfs.UDFs import *

def sw_gold_page_indexeddate_1(spark: SparkSession) -> DataFrame:
    return spark.read.table(f"scottaidemo.sw_gold_page_indexeddate")
