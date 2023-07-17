from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from sw_sectionize.config.ConfigStore import *
from sw_sectionize.udfs.UDFs import *

def sw_silver_sectionized(spark: SparkSession, in0: DataFrame):
    if spark.catalog._jcatalog.tableExists(f"scottaidemo.sw_silver_sectionized"):
        from delta.tables import DeltaTable, DeltaMergeBuilder
        DeltaTable\
            .forName(spark, f"scottaidemo.sw_silver_sectionized")\
            .alias("target")\
            .merge(
              in0.alias("source"),
              (
                (col("source.page_id") == col("target.page_id"))
                & (col("source.section_num") == col("target.section_num"))
              )
            )\
            .whenMatchedUpdateAll()\
            .whenNotMatchedInsertAll()\
            .execute()
    else:
        in0.write.format("delta").mode("overwrite").saveAsTable(f"scottaidemo.sw_silver_sectionized")
