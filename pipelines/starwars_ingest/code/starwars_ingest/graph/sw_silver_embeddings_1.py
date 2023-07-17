from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from starwars_ingest.config.ConfigStore import *
from starwars_ingest.udfs.UDFs import *

def sw_silver_embeddings_1(spark: SparkSession) -> DataFrame:
    return spark.read.table(f"scottaidemo.sw_silver_embeddings")
