from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from sw_vectorize.config.ConfigStore import *
from sw_vectorize.udfs.UDFs import *

def sw_gold_embeddings(spark: SparkSession, in0: DataFrame):
    if spark.catalog._jcatalog.tableExists(f"scottaidemo.sw_gold_embeddings"):
        from delta.tables import DeltaTable, DeltaMergeBuilder
        DeltaTable\
            .forName(spark, f"scottaidemo.sw_gold_embeddings")\
            .alias("target")\
            .merge(in0.alias("source"), (col("source.doc_id") == col("target.doc_id")))\
            .whenMatchedUpdateAll()\
            .whenNotMatchedInsertAll()\
            .execute()
    else:
        in0.write.format("delta").mode("overwrite").saveAsTable(f"scottaidemo.sw_gold_embeddings")
