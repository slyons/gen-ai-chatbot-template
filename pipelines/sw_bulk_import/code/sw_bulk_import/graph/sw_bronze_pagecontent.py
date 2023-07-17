from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from sw_bulk_import.config.ConfigStore import *
from sw_bulk_import.udfs.UDFs import *

def sw_bronze_pagecontent(spark: SparkSession, in0: DataFrame):
    if spark.catalog._jcatalog.tableExists(f"scottaidemo.sw_bronze_pagecontent"):
        from delta.tables import DeltaTable, DeltaMergeBuilder
        DeltaTable\
            .forName(spark, f"scottaidemo.sw_bronze_pagecontent")\
            .alias("target")\
            .merge(in0.alias("source"), (col("source.page_id") == col("target.page_id")))\
            .whenMatchedUpdateAll()\
            .whenNotMatchedInsertAll()\
            .execute()
    else:
        in0.write\
            .format("delta")\
            .option("overwriteSchema", True)\
            .mode("overwrite")\
            .saveAsTable(f"scottaidemo.sw_bronze_pagecontent")
