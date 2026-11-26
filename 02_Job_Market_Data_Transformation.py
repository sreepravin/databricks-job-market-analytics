# Databricks notebook source
bronze_df = spark.table(
    "workspace.job_market.jobs_bronze"
)

display(bronze_df)

# COMMAND ----------

from pyspark.sql import functions as F

display(
    bronze_df.select([
        F.count(
            F.when(F.col(c).isNull(), 1)
        ).alias(c)
        for c in bronze_df.columns
    ])
)

# COMMAND ----------

total_records = bronze_df.count()

unique_records = bronze_df.dropDuplicates(
    ["job_id"]
).count()

print("Total Records:", total_records)
print("Unique Records:", unique_records)
print("Duplicate Records:", total_records - unique_records)

# COMMAND ----------

silver_df = bronze_df.dropDuplicates(["job_id"])

silver_df = silver_df.dropna(
    subset=["job_id", "job_title", "salary_lpa",
            "location", "skills"]
)

silver_df = silver_df.filter(
    F.col("salary_lpa") > 0
)

silver_df = silver_df.withColumn(
    "job_title", F.trim(F.col("job_title"))
).withColumn(
    "company", F.trim(F.col("company"))
).withColumn(
    "location", F.trim(F.col("location"))
).withColumn(
    "posted_date", F.to_date("posted_date")
).withColumn(
    "salary_lpa", F.round("salary_lpa", 2)
).withColumn(
    "skills_array", F.split(F.col("skills"), ", ")
).withColumn(
    "processed_timestamp", F.current_timestamp()
)

display(silver_df)

# COMMAND ----------

silver_df.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("workspace.job_market.jobs_silver")

print("Silver table created successfully")

# COMMAND ----------

silver_table = spark.table(
    "workspace.job_market.jobs_silver"
)

print("Bronze Records:", bronze_df.count())
print("Silver Records:", silver_table.count())
print("Silver Columns:", len(silver_table.columns))

silver_table.printSchema()

display(silver_table)