from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from sw_bulk_import.config.ConfigStore import *
from sw_bulk_import.udfs.UDFs import *

def starwars_wiki_xml(spark: SparkSession) -> DataFrame:
    return spark.read\
        .format("xml")\
        .option("rowTag", "page")\
        .schema(
          StructType([
            StructField("id", LongType(), True), StructField("ns", LongType(), True), StructField("redirect", StructType([
              StructField("_VALUE", StringType(), True), StructField("_title", StringType(), True)
            ]), True), StructField("revision", StructType([
              StructField("comment", StringType(), True), StructField("contributor", StructType([
                StructField("id", LongType(), True), StructField("ip", StringType(), True), StructField("username", StringType(), True)
              ]), True), StructField("format", StringType(), True), StructField("id", LongType(), True), StructField("minor", StringType(), True), StructField("model", StringType(), True), StructField("origin", LongType(), True), StructField("parentid", LongType(), True), StructField("sha1", StringType(), True), StructField("text", StructType([
                StructField("_VALUE", StringType(), True), StructField("_bytes", LongType(), True), StructField("_sha1", StringType(), True), StructField("_xml:space", StringType(), True)
              ]), True), StructField("timestamp", TimestampType(), True)
            ]), True), StructField("title", StringType(), True)
        ])
        )\
        .load("dbfs:/Prophecy/scott@prophecy.io/starwars_pages_current.xml")
