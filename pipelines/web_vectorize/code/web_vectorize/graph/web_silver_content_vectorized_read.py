from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.libs import typed_lit
from prophecy.transpiler import call_spark_fcn
from prophecy.transpiler.fixed_file_schema import *
from web_vectorize.config.ConfigStore import *
from web_vectorize.udfs.UDFs import *

def web_silver_content_vectorized_read(spark: SparkSession) -> DataFrame:
    return spark.read.table(f"prophecy_data.web_silver.content_vectorized")