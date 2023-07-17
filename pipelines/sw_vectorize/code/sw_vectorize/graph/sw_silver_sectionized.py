from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from sw_vectorize.config.ConfigStore import *
from sw_vectorize.udfs.UDFs import *

def sw_silver_sectionized(spark: SparkSession) -> DataFrame:
    return spark.read.table(f"scottaidemo.sw_silver_sectionized")
