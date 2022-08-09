import unittest
import tempfile
import os
import shutil
import pandas as pd

from cicd_sample_project.jobs.sample.entrypoint import SampleJob
from pyspark.sql import SparkSession
from unittest.mock import MagicMock

class SampleJobUnitTest(unittest.TestCase):
    def setUp(self):
        tmp_dir = tempfile.TemporaryDirectory()
        self.test_dir = tmp_dir.name
        self.spark = SparkSession.builder.master("local[1]").getOrCreate()
        self.test_config = {
            "output_format": "parquet",
            "output_path": os.path.join(self.test_dir, "output"),
        }
        self.job = SampleJob(spark=self.spark, init_conf=self.test_config)

    def test_calculate_even_vs_odd(self):
        expected = {
            "isEven": [False, True], 
            "count": [250, 250]
        }

        expected_df = pd.DataFrame(data=expected)

        df = self.spark.range(0, 500)
        actual_df = self.job.calculate_even_vs_odd(df).toPandas()

        assert expected_df.equals(actual_df) is True

    def test_write(self):
        df = self.spark.range(0, 500)

        self.job.write(df)

        output_count = (
            self.spark.read.format(self.test_config["output_format"])
            .load(self.test_config["output_path"])
            .count()
        )

        self.assertGreater(output_count, 0)

    def tearDown(self):
        shutil.rmtree(self.test_dir, ignore_errors=True)


if __name__ == "__main__":
    print("This is a test!")
    unittest.main()
