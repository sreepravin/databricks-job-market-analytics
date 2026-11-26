# Databricks notebook source
from pyspark.sql import functions as F

silver_df = spark.table(
    "workspace.job_market.jobs_silver"
)

display(silver_df)

# COMMAND ----------

skills_df = silver_df.withColumn(
    "skill", F.explode("skills_array")
)

skills_demand = skills_df.groupBy("skill").agg(
    F.countDistinct("job_id").alias("job_count")
).orderBy(F.desc("job_count"))

display(skills_demand)

# COMMAND ----------

skills_demand.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("workspace.job_market.skills_demand")

# COMMAND ----------

salary_analysis = silver_df.groupBy("job_title").agg(
    F.round(F.avg("salary_lpa"), 2).alias("avg_salary"),
    F.min("salary_lpa").alias("min_salary"),
    F.max("salary_lpa").alias("max_salary"),
    F.count("*").alias("job_count")
).orderBy(F.desc("avg_salary"))

display(salary_analysis)

# COMMAND ----------

salary_analysis.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("workspace.job_market.salary_analysis")

# COMMAND ----------

location_analysis = silver_df.groupBy("location").agg(
    F.count("*").alias("job_count"),
    F.round(F.avg("salary_lpa"), 2).alias("avg_salary")
).orderBy(F.desc("job_count"))

display(location_analysis)

# COMMAND ----------

location_analysis.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("workspace.job_market.location_analysis")

# COMMAND ----------

company_analysis = silver_df.groupBy("company").agg(
    F.count("*").alias("job_count"),
    F.round(F.avg("salary_lpa"), 2).alias("avg_salary")
).orderBy(F.desc("job_count"))

display(company_analysis)

# COMMAND ----------

company_analysis.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("workspace.job_market.company_analysis")

# COMMAND ----------

experience_analysis = silver_df.groupBy("experience").agg(
    F.count("*").alias("job_count"),
    F.round(F.avg("salary_lpa"), 2).alias("avg_salary")
).orderBy(F.desc("job_count"))

display(experience_analysis)

# COMMAND ----------

experience_analysis.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("workspace.job_market.experience_analysis")

# COMMAND ----------

work_mode_analysis = silver_df.groupBy("work_mode").agg(
    F.count("*").alias("job_count"),
    F.round(F.avg("salary_lpa"), 2).alias("avg_salary")
).orderBy(F.desc("job_count"))

display(work_mode_analysis)

# COMMAND ----------

display(
    spark.sql("SHOW TABLES IN workspace.job_market")
)

# COMMAND ----------

work_mode_analysis = silver_df.groupBy("work_mode").agg(
    F.count("*").alias("job_count"),
    F.round(F.avg("salary_lpa"), 2).alias("avg_salary")
)

work_mode_analysis.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("workspace.job_market.work_mode_analysis")

display(work_mode_analysis)

# COMMAND ----------

display(
    spark.sql("SHOW TABLES IN workspace.job_market")
)