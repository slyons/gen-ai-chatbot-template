from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from chatbot_live.config.ConfigStore import *
from chatbot_live.udfs.UDFs import *

def SchemaTransform_1(spark: SparkSession, in0: DataFrame) -> DataFrame:
    return in0.withColumn(
        "answer",
        ((lit("Is \"") + col("answer")) + lit("\" a positive sentence or a negative sentence?"))
    )
