from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.utils import *
from prophecy.libs import typed_lit
from chatbot_live.config.ConfigStore import *
from chatbot_live.udfs.UDFs import *

def MoodEnhancer(spark: SparkSession, in0: DataFrame) -> DataFrame:
    import random
    from pyspark.sql.functions import col
    moods = ["in a grumpy way", "in a bubbly way", "in a quiet way", "in a depressed way", "in a distracted way",
             "in a panicked way", "in an annoyed tone", "in an overly nice way",
             "like you have a secret to share"]
    rand_mood = random.choice(moods)
    mood_msg = f"\n\nAnswer {rand_mood}."
    out0 = in0.withColumn("input", col("input") + lit(mood_msg))

    return out0
