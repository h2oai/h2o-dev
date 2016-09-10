from __future__ import print_function
import sys
sys.path.insert(1,"../../")
import h2o
import time
from tests import pyunit_utils
#----------------------------------------------------------------------
# PUBDEV-3359: verify that we can parse thousands of files correctly or
# identify it if not.  Split the airlines_all datasets in to 1999 files
# each with 50000 lines of data.  Total data frame should contain 100000000
# rows.  Check and make sure our parser can handle this.
#
#----------------------------------------------------------------------


def hdfs_orc_parser():

    # Check if we are running inside the H2O network by seeing if we can touch
    # the namenode.
    hadoop_namenode_is_accessible = pyunit_utils.hadoop_namenode_is_accessible()

    if hadoop_namenode_is_accessible:
        hdfs_name_node = pyunit_utils.hadoop_namenode()

        if pyunit_utils.cannaryHDFSTest(hdfs_name_node, "/datasets/orc_parser/orc/orc_split_elim.orc"):
            print("Your hive-exec version is too old.  Orc parser test {0} is "
                  "skipped.".format("pyunit_INTERNAL_HDFS_hexdex_29_import_types_orc.py"))
            pass
        else:
            hdfs_csv_file = "/datasets/hexdev_3359"
            url_csv = "hdfs://{0}{1}".format(hdfs_name_node, hdfs_csv_file)

            h2oframe_csv = h2o.import_file(url_csv)

            # compare the two frames
            if not(h2oframe_csv.nrow == 100000000):
                print("Data should contain 100000000 rows but we parsed: {0} rows!".format(h2oframe_csv.nrow))
            assert h2oframe_csv.nrow==100000000, "H2O frame parsed incorrectly!  Number of rows != 100000000."

    else:
        raise EnvironmentError


if __name__ == "__main__":
    pyunit_utils.standalone_test(hdfs_orc_parser)
else:
    hdfs_orc_parser()