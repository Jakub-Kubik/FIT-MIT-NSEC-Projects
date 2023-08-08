from pyspark.sql import SparkSession, types, functions


schema_type = (types.StructType, types.StringType, types.DoubleType)


def task_1(data: schema_type, hdfs: str) -> None:
	"""
	data a hodnoty nejmenšího a největšího kurzu pro každou z měn v souboru, 
	hodnotu průměrného kurzu za celé sledované období pro každou z měn v souboru,

	"""
	# get and compute average values for all currencies
	results_avg_value = data.groupBy("currency").avg("obs_value")

	# get global max value for all currencies
	max_value = data.groupBy("currency").agg(functions.max("obs_value").alias("max_row")).distinct()
	condition = [data.obs_value == max_value.max_row, data.currency == max_value.currency]
	results_max_value = data.join(max_value, condition, "leftsemi").dropDuplicates(["currency"])

	# get global min value for all currencies
	min_value = data.groupBy("currency").agg(functions.min("obs_value").alias("min_row")).distinct()
	condition = [data.obs_value == min_value.min_row, data.currency == min_value.currency]
	results_min_value = data.join(min_value, condition, "leftsemi").dropDuplicates(["currency"])

	# save results to csv files
	results_max_value.write.format("com.databricks.spark.csv").option("header", "true").mode("overwrite").save(hdfs+"max")
	results_min_value.write.format("com.databricks.spark.csv").option("header", "true").mode("overwrite").save(hdfs+"min")
	results_avg_value.write.format("com.databricks.spark.csv").option("header", "true").mode("overwrite").save(hdfs+"avg")


def task_4(data: schema_type, hdfs: str) -> None:
	"""
	Názvy měn s největším a nejměnším kruzem z celého souboru.

	"""
	# get global minimal value from all obs_value
	glob_min = data.select(functions.min("obs_value").alias("min_currency"))
	condition = [data.obs_value == glob_min.min_currency]
	results_glob_min = data.join(glob_min, condition, "leftsemi")

	# get global maximal value from all obs_value
	glob_max_currency = data.select(functions.max("obs_value").alias("glob_max_currency"))
	condition = [data.obs_value == glob_max_currency.glob_max_currency]
	results_glob_max = data.join(glob_max_currency, condition, "leftsemi")

	# # write results to csv format and save to hdfs
	results_glob_min.write.format("com.databricks.spark.csv").option("header", "true").mode("overwrite").save(hdfs+"min_global")
	results_glob_max.write.format("com.databricks.spark.csv").option("header", "true").mode("overwrite").save(hdfs+"max_global")


def main():
	hdfs_address = "hdfs://127.0.0.2:8020/user/demo/"
	spark = SparkSession.builder.master("local").appName("hdfs_test").getOrCreate()
	data_schema = types.StructType().add("currency", types.StringType()).add("time_period", types.DateType()).add("obs_value", types.DoubleType())

	# read csv from HDFS
	data=spark.read.csv(hdfs_address+"eurofxref-sdmx.csv", header=True, schema=data_schema)

	task_1(data, hdfs_address)
	task_4(data, hdfs_address)


if __name__ == '__main__':
    main()
