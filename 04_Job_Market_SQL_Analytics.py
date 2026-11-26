# Databricks notebook source
# MAGIC %sql
# MAGIC SELECT
# MAGIC     COUNT(*) AS total_jobs,
# MAGIC     COUNT(DISTINCT company) AS total_companies,
# MAGIC     COUNT(DISTINCT job_title) AS total_job_roles,
# MAGIC     COUNT(DISTINCT location) AS total_locations,
# MAGIC     ROUND(AVG(salary_lpa), 2) AS average_salary,
# MAGIC     MAX(salary_lpa) AS highest_salary
# MAGIC FROM workspace.job_market.jobs_silver;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT skill, job_count
# MAGIC FROM workspace.job_market.skills_demand
# MAGIC ORDER BY job_count DESC
# MAGIC LIMIT 10;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT job_title, avg_salary, job_count
# MAGIC FROM workspace.job_market.salary_analysis
# MAGIC ORDER BY avg_salary DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT location, job_count, avg_salary
# MAGIC FROM workspace.job_market.location_analysis
# MAGIC ORDER BY job_count DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT company, job_count
# MAGIC FROM workspace.job_market.company_analysis
# MAGIC ORDER BY job_count DESC
# MAGIC LIMIT 10;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT experience, job_count
# MAGIC FROM workspace.job_market.experience_analysis
# MAGIC ORDER BY job_count DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT work_mode, job_count
# MAGIC FROM workspace.job_market.work_mode_analysis
# MAGIC ORDER BY job_count DESC;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     DATE_FORMAT(posted_date, 'yyyy-MM') AS month,
# MAGIC     COUNT(*) AS job_count
# MAGIC FROM workspace.job_market.jobs_silver
# MAGIC GROUP BY DATE_FORMAT(posted_date, 'yyyy-MM')
# MAGIC ORDER BY month;

# COMMAND ----------

# MAGIC %sql
# MAGIC SELECT
# MAGIC     skill,
# MAGIC     COUNT(*) AS job_count
# MAGIC FROM workspace.job_market.jobs_silver
# MAGIC LATERAL VIEW EXPLODE(skills_array) e AS skill
# MAGIC WHERE job_title = 'Data Engineer'
# MAGIC GROUP BY skill
# MAGIC ORDER BY job_count DESC;

# COMMAND ----------

