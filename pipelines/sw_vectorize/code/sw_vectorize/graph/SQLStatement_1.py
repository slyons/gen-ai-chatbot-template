from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from sw_vectorize.config.ConfigStore import *
from sw_vectorize.udfs.UDFs import *

def SQLStatement_1(spark: SparkSession, in0: DataFrame) -> (DataFrame):

    try:
        registerUDFs(spark)
    except NameError:
        print("registerUDFs not working")

    in0.createOrReplaceTempView("in0")
    df1 = spark.sql(
        "SELECT \n    title, \n    page_id, \n    page_last_update,\n    section_num, \n    section_name, \n    posexplode(result_chunks_window) AS (chunk_window, text_chunks) \nFROM \n    in0"
    )

    return df1
