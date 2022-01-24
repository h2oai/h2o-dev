#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# This file is auto-generated by h2o-3/h2o-bindings/bin/gen_python.py
# Copyright 2016 H2O.ai;  Apache License Version 2.0 (see LICENSE for details)
#

from h2o.estimators.estimator_base import H2OEstimator
from h2o.exceptions import H2OValueError
from h2o.frame import H2OFrame
from h2o.utils.typechecks import assert_is_type, Enum, numeric


class H2OExtendedIsolationForestEstimator(H2OEstimator):
    """
    Extended Isolation Forest

    Builds an Extended Isolation Forest model. Extended Isolation Forest generalizes its predecessor algorithm, 
    Isolation Forest. The original Isolation Forest algorithm suffers from bias due to tree branching. Extension of the 
    algorithm mitigates the bias by adjusting the branching, and the original algorithm becomes just a special case.
    Extended Isolation Forest's attribute "extension_level" allows leveraging the generalization. The minimum value is 0 and
    means the Isolation Forest's behavior. Maximum value is (numCols - 1) and stands for full extension. The rest of the 
    algorithm is analogical to the Isolation Forest algorithm. Each iteration builds a tree that partitions the sample 
    observations' space until it isolates observation. The length of the path from root to a leaf node of the resulting tree
    is used to calculate the anomaly score. Anomalies are easier to isolate, and their average
    tree path is expected to be shorter than paths of regular observations. Anomaly score is a number between 0 and 1. 
    A number closer to 0 is a normal point, and a number closer to 1 is a more anomalous point.
    """

    algo = "extendedisolationforest"
    supervised_learning = False

    def __init__(self,
                 model_id=None,  # type: Optional[Union[None, str, H2OEstimator]]
                 training_frame=None,  # type: Optional[Union[None, str, H2OFrame]]
                 ignored_columns=None,  # type: Optional[List[str]]
                 ignore_const_cols=True,  # type: bool
                 categorical_encoding="auto",  # type: Literal["auto", "enum", "one_hot_internal", "one_hot_explicit", "binary", "eigen", "label_encoder", "sort_by_response", "enum_limited"]
                 score_each_iteration=False,  # type: bool
                 score_tree_interval=0,  # type: int
                 ntrees=100,  # type: int
                 sample_size=256,  # type: int
                 extension_level=0,  # type: int
                 seed=-1,  # type: int
                 ):
        """
        :param model_id: Destination id for this model; auto-generated if not specified.
               Defaults to ``None``.
        :type model_id: Union[None, str, H2OEstimator], optional
        :param training_frame: Id of the training data frame.
               Defaults to ``None``.
        :type training_frame: Union[None, str, H2OFrame], optional
        :param ignored_columns: Names of columns to ignore for training.
               Defaults to ``None``.
        :type ignored_columns: List[str], optional
        :param ignore_const_cols: Ignore constant columns.
               Defaults to ``True``.
        :type ignore_const_cols: bool
        :param categorical_encoding: Encoding scheme for categorical features
               Defaults to ``"auto"``.
        :type categorical_encoding: Literal["auto", "enum", "one_hot_internal", "one_hot_explicit", "binary", "eigen", "label_encoder",
               "sort_by_response", "enum_limited"]
        :param score_each_iteration: Whether to score during each iteration of model training.
               Defaults to ``False``.
        :type score_each_iteration: bool
        :param score_tree_interval: Score the model after every so many trees. Disabled if set to 0.
               Defaults to ``0``.
        :type score_tree_interval: int
        :param ntrees: Number of Extended Isolation Forest trees.
               Defaults to ``100``.
        :type ntrees: int
        :param sample_size: Number of randomly sampled observations used to train each Extended Isolation Forest tree.
               Defaults to ``256``.
        :type sample_size: int
        :param extension_level: Maximum is N - 1 (N = numCols). Minimum is 0. Extended Isolation Forest with
               extension_Level = 0 behaves like Isolation Forest.
               Defaults to ``0``.
        :type extension_level: int
        :param seed: Seed for pseudo random number generator (if applicable)
               Defaults to ``-1``.
        :type seed: int
        """
        super(H2OExtendedIsolationForestEstimator, self).__init__()
        self._parms = {}
        self._id = self._parms['model_id'] = model_id
        self.training_frame = training_frame
        self.ignored_columns = ignored_columns
        self.ignore_const_cols = ignore_const_cols
        self.categorical_encoding = categorical_encoding
        self.score_each_iteration = score_each_iteration
        self.score_tree_interval = score_tree_interval
        self.ntrees = ntrees
        self.sample_size = sample_size
        self.extension_level = extension_level
        self.seed = seed

    @property
    def training_frame(self):
        """
        Id of the training data frame.

        Type: ``Union[None, str, H2OFrame]``.

        :examples:

        >>> cars = h2o.import_file("https://s3.amazonaws.com/h2o-public-test-data/smalldata/junit/cars_20mpg.csv")
        >>> predictors = ["displacement","power","weight","acceleration","year"]
        >>> cars_eif = H2OExtendedIsolationForestEstimator(seed = 1234, 
        ...                                                sample_size = 256, 
        ...                                                extension_level = cars.dim[1] - 1)
        >>> cars_eif.train(x = predictors,
        ...                training_frame = cars)
        >>> print(cars_eif)
        """
        return self._parms.get("training_frame")

    @training_frame.setter
    def training_frame(self, training_frame):
        self._parms["training_frame"] = H2OFrame._validate(training_frame, 'training_frame')

    @property
    def ignored_columns(self):
        """
        Names of columns to ignore for training.

        Type: ``List[str]``.
        """
        return self._parms.get("ignored_columns")

    @ignored_columns.setter
    def ignored_columns(self, ignored_columns):
        assert_is_type(ignored_columns, None, [str])
        self._parms["ignored_columns"] = ignored_columns

    @property
    def ignore_const_cols(self):
        """
        Ignore constant columns.

        Type: ``bool``, defaults to ``True``.

        :examples:

        >>> cars = h2o.import_file("https://s3.amazonaws.com/h2o-public-test-data/smalldata/junit/cars_20mpg.csv")
        >>> predictors = ["displacement","power","weight","acceleration","year","const_1","const_2"]
        >>> cars["const_1"] = 6
        >>> cars["const_2"] = 7
        >>> train, valid = cars.split_frame(ratios = [.8], seed = 1234)
        >>> cars_eif = H2OExtendedIsolationForestEstimator(seed = 1234,
        ...                                                ignore_const_cols = True)
        >>> cars_eif.train(x = predictors,
        ...               training_frame = cars)
        >>> cars_eif.model_performance()
        """
        return self._parms.get("ignore_const_cols")

    @ignore_const_cols.setter
    def ignore_const_cols(self, ignore_const_cols):
        assert_is_type(ignore_const_cols, None, bool)
        self._parms["ignore_const_cols"] = ignore_const_cols

    @property
    def categorical_encoding(self):
        """
        Encoding scheme for categorical features

        Type: ``Literal["auto", "enum", "one_hot_internal", "one_hot_explicit", "binary", "eigen", "label_encoder",
        "sort_by_response", "enum_limited"]``, defaults to ``"auto"``.

        :examples:

        >>> airlines= h2o.import_file("https://s3.amazonaws.com/h2o-public-test-data/smalldata/airlines/allyears2k_headers.zip")
        >>> predictors = ["Origin", "Dest", "Year", "UniqueCarrier",
        ...               "DayOfWeek", "Month", "Distance", "FlightNum"]
        >>> encoding = "one_hot_explicit"
        >>> airlines_eif = H2OExtendedIsolationForestEstimator(categorical_encoding = encoding,
        ...                                                    seed = 1234)
        >>> airlines_eif.train(x = predictors,
        ...                   training_frame = airlines)
        >>> airlines_eif.model_performance()
        """
        return self._parms.get("categorical_encoding")

    @categorical_encoding.setter
    def categorical_encoding(self, categorical_encoding):
        assert_is_type(categorical_encoding, None, Enum("auto", "enum", "one_hot_internal", "one_hot_explicit", "binary", "eigen", "label_encoder", "sort_by_response", "enum_limited"))
        self._parms["categorical_encoding"] = categorical_encoding

    @property
    def score_each_iteration(self):
        """
        Whether to score during each iteration of model training.

        Type: ``bool``, defaults to ``False``.
        """
        return self._parms.get("score_each_iteration")

    @score_each_iteration.setter
    def score_each_iteration(self, score_each_iteration):
        assert_is_type(score_each_iteration, None, bool)
        self._parms["score_each_iteration"] = score_each_iteration

    @property
    def score_tree_interval(self):
        """
        Score the model after every so many trees. Disabled if set to 0.

        Type: ``int``, defaults to ``0``.
        """
        return self._parms.get("score_tree_interval")

    @score_tree_interval.setter
    def score_tree_interval(self, score_tree_interval):
        assert_is_type(score_tree_interval, None, int)
        self._parms["score_tree_interval"] = score_tree_interval

    @property
    def ntrees(self):
        """
        Number of Extended Isolation Forest trees.

        Type: ``int``, defaults to ``100``.

        :examples:

        >>> titanic = h2o.import_file("https://s3.amazonaws.com/h2o-public-test-data/smalldata/gbm_test/titanic.csv")
        >>> predictors = titanic.columns
        >>> tree_num = [20, 50, 80, 110, 140, 170, 200]
        >>> label = ["20", "50", "80", "110", "140", "170", "200"]
        >>> for key, num in enumerate(tree_num):
        ...     titanic_eif = H2OExtendedIsolationForestEstimator(ntrees = num,
        ...                                                       seed = 1234,
        ...                                                       extension_level = titanic.dim[1] - 1)
        ...     titanic_eif.train(x = predictors,
        ...                      training_frame = titanic) 
        """
        return self._parms.get("ntrees")

    @ntrees.setter
    def ntrees(self, ntrees):
        assert_is_type(ntrees, None, int)
        self._parms["ntrees"] = ntrees

    @property
    def sample_size(self):
        """
        Number of randomly sampled observations used to train each Extended Isolation Forest tree.

        Type: ``int``, defaults to ``256``.

        :examples:

        >>> train = h2o.import_file("http://s3.amazonaws.com/h2o-public-test-data/smalldata/anomaly/ecg_discord_train.csv")
        >>> eif_model = H2OExtendedIsolationForestEstimator(sample_size = 5,
        ...                                                 ntrees=7)
        >>> eif_model.train(training_frame = train)
        >>> print(eif_model)
        """
        return self._parms.get("sample_size")

    @sample_size.setter
    def sample_size(self, sample_size):
        assert_is_type(sample_size, None, int)
        self._parms["sample_size"] = sample_size

    @property
    def extension_level(self):
        """
        Maximum is N - 1 (N = numCols). Minimum is 0. Extended Isolation Forest with extension_Level = 0 behaves like
        Isolation Forest.

        Type: ``int``, defaults to ``0``.

        :examples:

        >>> train = h2o.import_file("http://s3.amazonaws.com/h2o-public-test-data/smalldata/anomaly/single_blob.csv")
        >>> eif_model = H2OExtendedIsolationForestEstimator(extension_level = 1,
        ...                                                 ntrees=7)
        >>> eif_model.train(training_frame = train)
        >>> print(eif_model)
        """
        return self._parms.get("extension_level")

    @extension_level.setter
    def extension_level(self, extension_level):
        assert_is_type(extension_level, None, int)
        self._parms["extension_level"] = extension_level

    @property
    def seed(self):
        """
        Seed for pseudo random number generator (if applicable)

        Type: ``int``, defaults to ``-1``.

        :examples:

        >>> airlines= h2o.import_file("https://s3.amazonaws.com/h2o-public-test-data/smalldata/airlines/allyears2k_headers.zip")
        >>> predictors = ["Origin", "Dest", "Year", "UniqueCarrier",
        ...               "DayOfWeek", "Month", "Distance", "FlightNum"]
        >>> eif_w_seed = H2OExtendedIsolationForestEstimator(seed = 1234) 
        >>> eif_w_seed.train(x = predictors,
        ...                        training_frame = airlines)
        >>> eif_wo_seed = H2OExtendedIsolationForestEstimator()
        >>> eif_wo_seed.train(x = predictors,
        ...                         training_frame = airlines)
        >>> print(eif_w_seed)
        >>> print(eif_wo_seed)
        """
        return self._parms.get("seed")

    @seed.setter
    def seed(self, seed):
        assert_is_type(seed, None, int)
        self._parms["seed"] = seed


