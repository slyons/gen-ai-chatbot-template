from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from starwars_ingest.config.ConfigStore import *
from starwars_ingest.udfs.UDFs import *

def SQLStatement_1(spark: SparkSession, in0: DataFrame) -> (DataFrame):

    try:
        registerUDFs(spark)
    except NameError:
        print("registerUDFs not working")

    in0.createOrReplaceTempView("in0")
    df1 = spark.sql(
        "SELECT title, page_id, section_num, section_name, posexplode(result_chunks_window) AS (chunk_window, text_chunks) FROM in0"
    )

    return df1
