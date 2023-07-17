from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from sw_bulk_import.config.ConfigStore import *
from sw_bulk_import.udfs.UDFs import *

def OnlyPages(spark: SparkSession, in0: DataFrame) -> DataFrame:
    return in0.filter(((col("ns") == lit(0)) & col("redirect").isNull()))
