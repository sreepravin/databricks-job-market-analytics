# Databricks notebook source
print("Intelligent Job Market Analytics Pipeline")
print("Databricks project started successfully")

# COMMAND ----------

import random
from datetime import datetime, timedelta

random.seed(42)

job_roles = {
    "Data Engineer": ["Python", "SQL", "PySpark", "Databricks", "AWS"],
    "Data Analyst": ["Python", "SQL", "Excel", "Power BI"],
    "Data Scientist": ["Python", "Machine Learning", "SQL", "Statistics"],
    "ML Engineer": ["Python", "TensorFlow", "PyTorch", "Docker"],
    "Software Developer": ["Java", "Python", "Git", "SQL"],
    "Cloud Engineer": ["AWS", "Azure", "Docker", "Kubernetes"],
    "Business Analyst": ["Excel", "SQL", "Power BI", "Tableau"]
}

companies = [
    "TCS", "Infosys", "Wipro", "Accenture",
    "Tiger Analytics", "Cognizant", "IBM",
    "Microsoft", "Amazon", "Google"
]

locations = [
    "Chennai", "Bangalore", "Hyderabad",
    "Mumbai", "Pune", "Coimbatore", "Delhi"
]

experience = ["0-2 years", "2-5 years", "5+ years"]

work_modes = ["Remote", "Hybrid", "On-site"]

data = []

for i in range(1, 5001):

    role = random.choice(list(job_roles.keys()))

    skills = ", ".join(
        random.sample(job_roles[role], 3)
    )

    data.append((
        i,
        role,
        random.choice(companies),
        random.choice(locations),
        round(random.uniform(3, 25), 2),
        skills,
        random.choice(experience),
        random.choice(work_modes),
        (datetime.now() - timedelta(
            days=random.randint(0, 365)
        )).strftime("%Y-%m-%d")
    ))

columns = [
    "job_id", "job_title", "company",
    "location", "salary_lpa", "skills",
    "experience", "work_mode", "posted_date"
]

df = spark.createDataFrame(data, columns)

display(df)

# COMMAND ----------

print("Total Records:", df.count())

print("Total Columns:", len(df.columns))

df.printSchema()

# COMMAND ----------

spark.sql("""
    SELECT current_catalog(), current_schema()
""").show()

# COMMAND ----------

spark.sql("CREATE SCHEMA IF NOT EXISTS job_market")

spark.sql("USE SCHEMA job_market")

# COMMAND ----------

from pyspark.sql.functions import current_timestamp, lit

bronze_df = df.withColumn(
    "ingestion_timestamp", current_timestamp()
).withColumn(
    "data_source", lit("synthetic_job_dataset")
)

display(bronze_df)

# COMMAND ----------

bronze_df.write \
    .format("delta") \
    .mode("overwrite") \
    .saveAsTable("job_market.jobs_bronze")

print("Bronze table created successfully")

# COMMAND ----------

bronze_table = spark.table("job_market.jobs_bronze")

print("Total Records:", bronze_table.count())
print("Total Columns:", len(bronze_table.columns))

display(bronze_table)

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT * FROM job_market.jobs_bronze
# MAGIC LIMIT 10;

# COMMAND ----------

# MAGIC %sql
# MAGIC DESCRIBE DETAIL job_market.jobs_bronze;

# COMMAND ----------



# COMMAND ----------

display(spark.table("workspace.job_market.jobs_bronze"))