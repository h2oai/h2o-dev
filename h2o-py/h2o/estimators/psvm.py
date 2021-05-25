#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# This file is auto-generated by h2o-3/h2o-bindings/bin/gen_python.py
# Copyright 2016 H2O.ai;  Apache License Version 2.0 (see LICENSE for details)
#
from __future__ import absolute_import, division, print_function, unicode_literals

from h2o.estimators.estimator_base import H2OEstimator
from h2o.exceptions import H2OValueError
from h2o.frame import H2OFrame
from h2o.utils.typechecks import assert_is_type, Enum, numeric


class H2OSupportVectorMachineEstimator(H2OEstimator):
    """
    PSVM

    """

    algo = "psvm"

    def __init__(self,
                 model_id=None,  # type: str
                 training_frame=None,  # type: H2OFrame
                 validation_frame=None,  # type: H2OFrame
                 response_column=None,  # type: str
                 ignored_columns=None,  # type: List[str]
                 ignore_const_cols=True,  # type: bool
                 hyper_param=1.0,  # type: float
                 kernel_type="gaussian",  # type: Literal["gaussian"]
                 gamma=-1.0,  # type: float
                 rank_ratio=-1.0,  # type: float
                 positive_weight=1.0,  # type: float
                 negative_weight=1.0,  # type: float
                 disable_training_metrics=True,  # type: bool
                 sv_threshold=0.0001,  # type: float
                 fact_threshold=1e-05,  # type: float
                 feasible_threshold=0.001,  # type: float
                 surrogate_gap_threshold=0.001,  # type: float
                 mu_factor=10.0,  # type: float
                 max_iterations=200,  # type: int
                 seed=-1,  # type: int
                 ):
        """
        :param model_id: Destination id for this model; auto-generated if not specified. (default:None).
        :type model_id: str, optional
        :param training_frame: Id of the training data frame. (default:None).
        :type training_frame: H2OFrame, optional
        :param validation_frame: Id of the validation data frame. (default:None).
        :type validation_frame: H2OFrame, optional
        :param response_column: Response variable column. (default:None).
        :type response_column: str, optional
        :param ignored_columns: Names of columns to ignore for training. (default:None).
        :type ignored_columns: List[str], optional
        :param ignore_const_cols: Ignore constant columns. (default:True).
        :type ignore_const_cols: bool, optional
        :param hyper_param: Penalty parameter C of the error term (default:1.0).
        :type hyper_param: float, optional
        :param kernel_type: Type of used kernel (default:"gaussian").
        :type kernel_type: Literal["gaussian"], optional
        :param gamma: Coefficient of the kernel (currently RBF gamma for gaussian kernel, -1 means 1/#features)
               (default:-1.0).
        :type gamma: float, optional
        :param rank_ratio: Desired rank of the ICF matrix expressed as an ration of number of input rows (-1 means use
               sqrt(#rows)). (default:-1.0).
        :type rank_ratio: float, optional
        :param positive_weight: Weight of positive (+1) class of observations (default:1.0).
        :type positive_weight: float, optional
        :param negative_weight: Weight of positive (-1) class of observations (default:1.0).
        :type negative_weight: float, optional
        :param disable_training_metrics: Disable calculating training metrics (expensive on large datasets)
               (default:True).
        :type disable_training_metrics: bool, optional
        :param sv_threshold: Threshold for accepting a candidate observation into the set of support vectors
               (default:0.0001).
        :type sv_threshold: float, optional
        :param fact_threshold: Convergence threshold of the Incomplete Cholesky Factorization (ICF) (default:1e-05).
        :type fact_threshold: float, optional
        :param feasible_threshold: Convergence threshold for primal-dual residuals in the IPM iteration (default:0.001).
        :type feasible_threshold: float, optional
        :param surrogate_gap_threshold: Feasibility criterion of the surrogate duality gap (eta) (default:0.001).
        :type surrogate_gap_threshold: float, optional
        :param mu_factor: Increasing factor mu (default:10.0).
        :type mu_factor: float, optional
        :param max_iterations: Maximum number of iteration of the algorithm (default:200).
        :type max_iterations: int, optional
        :param seed: Seed for pseudo random number generator (if applicable) (default:-1).
        :type seed: int, optional
        """
        sig_params = {k:v for k, v in locals().items() if k != 'self' and not k.startswith('__')}
        super(H2OSupportVectorMachineEstimator, self).__init__()
        self._parms = {}
        for pname, pvalue in sig_params.items():
            if pname == 'model_id':
                self._id = self._parms['model_id'] = pvalue
            else:
                # Using setattr(...) will invoke type-checking of the arguments
                setattr(self, pname, pvalue)

    @property
    def training_frame(self):
        """
        Id of the training data frame.

        Type: ``H2OFrame``.

        :examples:

        >>> splice = h2o.import_file("http://h2o-public-test-data.s3.amazonaws.com/smalldata/splice/splice.svm")
        >>> train, valid = splice.split_frame(ratios=[0.8])
        >>> svm = H2OSupportVectorMachineEstimator(disable_training_metrics=False)
        >>> svm.train(y="C1", training_frame=train)
        >>> svm.mse()
        """
        return self._parms.get("training_frame")

    @training_frame.setter
    def training_frame(self, training_frame):
        self._parms["training_frame"] = H2OFrame._validate(training_frame, 'training_frame')

    @property
    def validation_frame(self):
        """
        Id of the validation data frame.

        Type: ``H2OFrame``.

        :examples:

        >>> splice = h2o.import_file("http://h2o-public-test-data.s3.amazonaws.com/smalldata/splice/splice.svm")
        >>> train, valid = splice.split_frame(ratios=[0.8])
        >>> svm = H2OSupportVectorMachineEstimator(disable_training_metrics=False)
        >>> svm.train(y="C1", training_frame=train, validation_frame=valid)
        >>> svm.mse()
        """
        return self._parms.get("validation_frame")

    @validation_frame.setter
    def validation_frame(self, validation_frame):
        self._parms["validation_frame"] = H2OFrame._validate(validation_frame, 'validation_frame')

    @property
    def response_column(self):
        """
        Response variable column.

        Type: ``str``.
        """
        return self._parms.get("response_column")

    @response_column.setter
    def response_column(self, response_column):
        assert_is_type(response_column, None, str)
        self._parms["response_column"] = response_column

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

        Type: ``bool``  (default: ``True``).

        :examples:

        >>> splice = h2o.import_file("http://h2o-public-test-data.s3.amazonaws.com/smalldata/splice/splice.svm")
        >>> svm = H2OSupportVectorMachineEstimator(gamma=0.01,
        ...                                        rank_ratio=0.1,
        ...                                        ignore_const_cols=False,
        ...                                        disable_training_metrics=False)
        >>> svm.train(y="C1", training_frame=splice)
        >>> svm.mse()
        """
        return self._parms.get("ignore_const_cols")

    @ignore_const_cols.setter
    def ignore_const_cols(self, ignore_const_cols):
        assert_is_type(ignore_const_cols, None, bool)
        self._parms["ignore_const_cols"] = ignore_const_cols

    @property
    def hyper_param(self):
        """
        Penalty parameter C of the error term

        Type: ``float``  (default: ``1.0``).

        :examples:

        >>> splice = h2o.import_file("http://h2o-public-test-data.s3.amazonaws.com/smalldata/splice/splice.svm")
        >>> svm = H2OSupportVectorMachineEstimator(gamma=0.01,
        ...                                        rank_ratio=0.1,
        ...                                        hyper_param=0.01,
        ...                                        disable_training_metrics=False)
        >>> svm.train(y="C1", training_frame=splice)
        >>> svm.mse()
        """
        return self._parms.get("hyper_param")

    @hyper_param.setter
    def hyper_param(self, hyper_param):
        assert_is_type(hyper_param, None, numeric)
        self._parms["hyper_param"] = hyper_param

    @property
    def kernel_type(self):
        """
        Type of used kernel

        Type: ``Literal["gaussian"]``  (default: ``"gaussian"``).

        :examples:

        >>> splice = h2o.import_file("http://h2o-public-test-data.s3.amazonaws.com/smalldata/splice/splice.svm")
        >>> svm = H2OSupportVectorMachineEstimator(gamma=0.1,
        ...                                        rank_ratio=0.1,
        ...                                        hyper_param=0.01,
        ...                                        kernel_type="gaussian",
        ...                                        disable_training_metrics=False)
        >>> svm.train(y="C1", training_frame=splice) 
        >>> svm.mse()
        """
        return self._parms.get("kernel_type")

    @kernel_type.setter
    def kernel_type(self, kernel_type):
        assert_is_type(kernel_type, None, Enum("gaussian"))
        self._parms["kernel_type"] = kernel_type

    @property
    def gamma(self):
        """
        Coefficient of the kernel (currently RBF gamma for gaussian kernel, -1 means 1/#features)

        Type: ``float``  (default: ``-1.0``).

        :examples:

        >>> splice = h2o.import_file("http://h2o-public-test-data.s3.amazonaws.com/smalldata/splice/splice.svm")
        >>> svm = H2OSupportVectorMachineEstimator(gamma=0.01,
        ...                                        rank_ratio=0.1,
        ...                                        disable_training_metrics=False)
        >>> svm.train(y="C1", training_frame=splice)
        >>> svm.mse()
        """
        return self._parms.get("gamma")

    @gamma.setter
    def gamma(self, gamma):
        assert_is_type(gamma, None, numeric)
        self._parms["gamma"] = gamma

    @property
    def rank_ratio(self):
        """
        Desired rank of the ICF matrix expressed as an ration of number of input rows (-1 means use sqrt(#rows)).

        Type: ``float``  (default: ``-1.0``).

        :examples:

        >>> splice = h2o.import_file("http://h2o-public-test-data.s3.amazonaws.com/smalldata/splice/splice.svm")
        >>> svm = H2OSupportVectorMachineEstimator(gamma=0.01,
        ...                                        rank_ratio=0.1,
        ...                                        disable_training_metrics=False)
        >>> svm.train(y="C1", training_frame=splice)
        >>> svm.mse()
        """
        return self._parms.get("rank_ratio")

    @rank_ratio.setter
    def rank_ratio(self, rank_ratio):
        assert_is_type(rank_ratio, None, numeric)
        self._parms["rank_ratio"] = rank_ratio

    @property
    def positive_weight(self):
        """
        Weight of positive (+1) class of observations

        Type: ``float``  (default: ``1.0``).

        :examples:

        >>> splice = h2o.import_file("http://h2o-public-test-data.s3.amazonaws.com/smalldata/splice/splice.svm")
        >>> svm = H2OSupportVectorMachineEstimator(gamma=0.1,
        ...                                        rank_ratio=0.1,
        ...                                        positive_weight=0.1,
        ...                                        disable_training_metrics=False)
        >>> svm.train(y="C1", training_frame=splice)   
        >>> svm.mse()
        """
        return self._parms.get("positive_weight")

    @positive_weight.setter
    def positive_weight(self, positive_weight):
        assert_is_type(positive_weight, None, numeric)
        self._parms["positive_weight"] = positive_weight

    @property
    def negative_weight(self):
        """
        Weight of positive (-1) class of observations

        Type: ``float``  (default: ``1.0``).

        :examples:

        >>> splice = h2o.import_file("http://h2o-public-test-data.s3.amazonaws.com/smalldata/splice/splice.svm")
        >>> svm = H2OSupportVectorMachineEstimator(gamma=0.1,
        ...                                        rank_ratio=0.1,
        ...                                        negative_weight=10,
        ...                                        disable_training_metrics=False)
        >>> svm.train(y="C1", training_frame=splice)  
        >>> svm.mse()
        """
        return self._parms.get("negative_weight")

    @negative_weight.setter
    def negative_weight(self, negative_weight):
        assert_is_type(negative_weight, None, numeric)
        self._parms["negative_weight"] = negative_weight

    @property
    def disable_training_metrics(self):
        """
        Disable calculating training metrics (expensive on large datasets)

        Type: ``bool``  (default: ``True``).

        :examples:

        >>> from h2o.estimators import H2OSupportVectorMachineEstimator
        >>> splice = h2o.import_file("http://h2o-public-test-data.s3.amazonaws.com/smalldata/splice/splice.svm")
        >>> svm = H2OSupportVectorMachineEstimator(gamma=0.01,
        ...                                        rank_ratio=0.1,
        ...                                        disable_training_metrics=False)
        >>> svm.train(y="C1", training_frame=splice)
        >>> svm.mse()
        """
        return self._parms.get("disable_training_metrics")

    @disable_training_metrics.setter
    def disable_training_metrics(self, disable_training_metrics):
        assert_is_type(disable_training_metrics, None, bool)
        self._parms["disable_training_metrics"] = disable_training_metrics

    @property
    def sv_threshold(self):
        """
        Threshold for accepting a candidate observation into the set of support vectors

        Type: ``float``  (default: ``0.0001``).

        :examples:

        >>> splice = h2o.import_file("http://h2o-public-test-data.s3.amazonaws.com/smalldata/splice/splice.svm")
        >>> svm = H2OSupportVectorMachineEstimator(gamma=0.01,
        ...                                        rank_ratio=0.1,
        ...                                        sv_threshold=0.01,
        ...                                        disable_training_metrics=False)
        >>> svm.train(y="C1", training_frame=splice) 
        >>> svm.mse()
        """
        return self._parms.get("sv_threshold")

    @sv_threshold.setter
    def sv_threshold(self, sv_threshold):
        assert_is_type(sv_threshold, None, numeric)
        self._parms["sv_threshold"] = sv_threshold

    @property
    def fact_threshold(self):
        """
        Convergence threshold of the Incomplete Cholesky Factorization (ICF)

        Type: ``float``  (default: ``1e-05``).

        :examples:

        >>> splice = h2o.import_file("http://h2o-public-test-data.s3.amazonaws.com/smalldata/splice/splice.svm")
        >>> svm = H2OSupportVectorMachineEstimator(disable_training_metrics=False,
        ...                                        fact_threshold=1e-7)
        >>> svm.train(y="C1", training_frame=splice)
        >>> svm.mse()
        """
        return self._parms.get("fact_threshold")

    @fact_threshold.setter
    def fact_threshold(self, fact_threshold):
        assert_is_type(fact_threshold, None, numeric)
        self._parms["fact_threshold"] = fact_threshold

    @property
    def feasible_threshold(self):
        """
        Convergence threshold for primal-dual residuals in the IPM iteration

        Type: ``float``  (default: ``0.001``).

        :examples:

        >>> splice = h2o.import_file("http://h2o-public-test-data.s3.amazonaws.com/smalldata/splice/splice.svm")
        >>> svm = H2OSupportVectorMachineEstimator(disable_training_metrics=False,
        ...                                        fact_threshold=1e-7)
        >>> svm.train(y="C1", training_frame=splice)
        >>> svm.mse()
        """
        return self._parms.get("feasible_threshold")

    @feasible_threshold.setter
    def feasible_threshold(self, feasible_threshold):
        assert_is_type(feasible_threshold, None, numeric)
        self._parms["feasible_threshold"] = feasible_threshold

    @property
    def surrogate_gap_threshold(self):
        """
        Feasibility criterion of the surrogate duality gap (eta)

        Type: ``float``  (default: ``0.001``).

        :examples:

        >>> splice = h2o.import_file("http://h2o-public-test-data.s3.amazonaws.com/smalldata/splice/splice.svm")
        >>> svm = H2OSupportVectorMachineEstimator(gamma=0.01,
        ...                                        rank_ratio=0.1,
        ...                                        surrogate_gap_threshold=0.1,
        ...                                        disable_training_metrics=False)
        >>> svm.train(y="C1", training_frame=splice) 
        >>> svm.mse()
        """
        return self._parms.get("surrogate_gap_threshold")

    @surrogate_gap_threshold.setter
    def surrogate_gap_threshold(self, surrogate_gap_threshold):
        assert_is_type(surrogate_gap_threshold, None, numeric)
        self._parms["surrogate_gap_threshold"] = surrogate_gap_threshold

    @property
    def mu_factor(self):
        """
        Increasing factor mu

        Type: ``float``  (default: ``10.0``).

        :examples:

        >>> splice = h2o.import_file("http://h2o-public-test-data.s3.amazonaws.com/smalldata/splice/splice.svm")
        >>> svm = H2OSupportVectorMachineEstimator(gamma=0.1,
        ...                                        mu_factor=100.5,
        ...                                        disable_training_metrics=False)
        >>> svm.train(y="C1", training_frame=splice) 
        >>> svm.mse()
        """
        return self._parms.get("mu_factor")

    @mu_factor.setter
    def mu_factor(self, mu_factor):
        assert_is_type(mu_factor, None, numeric)
        self._parms["mu_factor"] = mu_factor

    @property
    def max_iterations(self):
        """
        Maximum number of iteration of the algorithm

        Type: ``int``  (default: ``200``).

        :examples:

        >>> splice = h2o.import_file("http://h2o-public-test-data.s3.amazonaws.com/smalldata/splice/splice.svm")
        >>> svm = H2OSupportVectorMachineEstimator(gamma=0.1,
        ...                                        rank_ratio=0.1,
        ...                                        hyper_param=0.01,
        ...                                        max_iterations=20,
        ...                                        disable_training_metrics=False)
        >>> svm.train(y="C1", training_frame=splice)  
        >>> svm.mse()
        """
        return self._parms.get("max_iterations")

    @max_iterations.setter
    def max_iterations(self, max_iterations):
        assert_is_type(max_iterations, None, int)
        self._parms["max_iterations"] = max_iterations

    @property
    def seed(self):
        """
        Seed for pseudo random number generator (if applicable)

        Type: ``int``  (default: ``-1``).

        :examples:

        >>> splice = h2o.import_file("http://h2o-public-test-data.s3.amazonaws.com/smalldata/splice/splice.svm")
        >>> svm = H2OSupportVectorMachineEstimator(gamma=0.1,
        ...                                        rank_ratio=0.1,
        ...                                        seed=1234,
        ...                                        disable_training_metrics=False)
        >>> svm.train(y="C1", training_frame=splice)
        >>> svm.model_performance
        """
        return self._parms.get("seed")

    @seed.setter
    def seed(self, seed):
        assert_is_type(seed, None, int)
        self._parms["seed"] = seed


