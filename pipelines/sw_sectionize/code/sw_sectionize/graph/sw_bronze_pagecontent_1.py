from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from sw_sectionize.config.ConfigStore import *
from sw_sectionize.udfs.UDFs import *

def sw_bronze_pagecontent_1(spark: SparkSession) -> DataFrame:
    return spark.read.table(f"scottaidemo.sw_bronze_pagecontent")
