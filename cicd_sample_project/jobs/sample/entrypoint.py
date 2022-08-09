from pyspark.sql.functions import col

from cicd_sample_project.common import Job


class SampleJob(Job):
    def init_adapter(self):
        if self.conf:
            return

        self.logger.info(
            "Init configuration was not provided, using configuration from default_init method"
        )
        self.conf = {
            "output_format": "delta",
            "output_path": "dbfs:/dbx/tmp/test/interactive/cicd_sample_project",
        }

    def read_data(self):
        return self.spark.range(0, 1000)

    def calculate_even_vs_odd(self, df):
        return df.withColumn("isEven", col("id") % 2 != 0).groupBy("isEven").count()

    def write(self, df):
        (  
            df
                .write
                .format(self.conf["output_format"])
                .mode("overwrite")
                .save(self.conf["output_path"])
        )

    def launch(self):
        self.logger.info("Launching sample job")

        df = self.read_data()
        df = self.calculate_even_vs_odd(df)
        
        self.write(df)

        self.logger.info("Sample job finished!")


if __name__ == "__main__":
    job = SampleJob()
    job.launch()
