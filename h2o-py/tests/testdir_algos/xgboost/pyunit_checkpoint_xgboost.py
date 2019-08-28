from __future__ import print_function
from builtins import range
import sys
sys.path.insert(1,"../../../")
import h2o
from tests import pyunit_utils
import os
import random
from h2o.estimators.xgboost import H2OXGBoostEstimator
from h2o.exceptions import H2OResponseError
 
def xgboost_checkpoint():

  milsong_train = h2o.upload_file(pyunit_utils.locate("bigdata/laptop/milsongs/milsongs-train.csv.gz"))
  milsong_valid = h2o.upload_file(pyunit_utils.locate("bigdata/laptop/milsongs/milsongs-test.csv.gz"))
  distribution = "gaussian"

  # build first model
  ntrees1 = 2
  max_depth1 = 2
  min_rows1 = 10
  print("ntrees model 1: {0}".format(ntrees1))
  print("max_depth model 1: {0}".format(max_depth1))
  print("min_rows model 1: {0}".format(min_rows1))


  model1 = H2OXGBoostEstimator(
    ntrees=ntrees1,
    max_depth=max_depth1,
    min_rows=min_rows1,
    distribution=distribution
  )
  model1.train(
    x=list(range(1,milsong_train.ncol)),
    y=0,
    training_frame=milsong_train,
    validation_frame=milsong_valid)

  # save the model, then load the model
  path = pyunit_utils.locate("results")

  assert os.path.isdir(path), "Expected save directory {0} to exist, but it does not.".format(path)
  model_path = h2o.save_model(model1, path=path, force=True)

  assert os.path.isfile(model_path), "Expected load file {0} to exist, but it does not.".format(model_path)
  restored_model = h2o.load_model(model_path)

  # continue building the model
  ntrees2 = ntrees1 + 1
  max_depth2 = max_depth1
  min_rows2 = min_rows1
  print("ntrees model 2: {0}".format(ntrees2))
  print("max_depth model 2: {0}".format(max_depth2))
  print("min_rows model 2: {0}".format(min_rows2))

  model2 = H2OXGBoostEstimator(
    ntrees=ntrees1,
    max_depth=max_depth2,
    min_rows=min_rows2,
    distribution=distribution,
    checkpoint=restored_model.model_id)
  try:
      model2.train(
        y=0, x=list(range(1,milsong_train.ncol)),
        training_frame=milsong_train,
        validation_frame=milsong_valid)
  except H2OResponseError as e:
    assert "_ntrees: If checkpoint is specified then requested ntrees must be higher than 3" in e.args[0].msg

  model2.ntrees = ntrees2
  model2.train(
    y=0, x=list(range(1,milsong_train.ncol)),
    training_frame=milsong_train,
    validation_frame=milsong_valid)
    
  assert model2.ntrees == ntrees2

if __name__ == "__main__":
  pyunit_utils.standalone_test(xgboost_checkpoint)
else:
  xgboost_checkpoint()
