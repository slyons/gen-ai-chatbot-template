from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from sw_update_vectordb.config.ConfigStore import *
from sw_update_vectordb.udfs.UDFs import *

def sw_gold_page_indexeddate(spark: SparkSession, in0: DataFrame):
    if spark.catalog._jcatalog.tableExists(f"scottaidemo.sw_gold_page_indexeddate"):
        from delta.tables import DeltaTable, DeltaMergeBuilder
        DeltaTable\
            .forName(spark, f"scottaidemo.sw_gold_page_indexeddate")\
            .alias("target")\
            .merge(in0.alias("source"), (col("source.doc_id") == col("target.doc_id")))\
            .whenMatchedUpdateAll()\
            .whenNotMatchedInsertAll()\
            .execute()
    else:
        in0.write.format("delta").mode("overwrite").saveAsTable(f"scottaidemo.sw_gold_page_indexeddate")
