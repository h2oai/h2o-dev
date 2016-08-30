#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# This file is auto-generated by h2o-3/h2o-bindings/bin/gen_python.py
# Copyright 2016 H2O.ai;  Apache License Version 2.0 (see LICENSE for details)
#
from .estimator_base import H2OEstimator


class H2ONaiveBayesEstimator(H2OEstimator):
    """
    Naive Bayes

    The naive Bayes classifier assumes independence between predictor variables
    conditional on the response, and a Gaussian distribution of numeric predictors with
    mean and standard deviation computed from the training dataset. When building a naive
    Bayes classifier, every row in the training dataset that contains at least one NA will
    be skipped completely. If the test dataset has missing values, then those predictors
    are omitted in the probability calculation during prediction.

    Parameters
    ----------
      model_id : str
        Destination id for this model; auto-generated if not specified.

      nfolds : int
        Number of folds for N-fold cross-validation (0 to disable or >= 2).
        Default: 0

      seed : int
        Seed for pseudo random number generator (only used for cross-validation and fold_assignment="Random" or "AUTO")
        Default: -1

      fold_assignment : "AUTO" | "Random" | "Modulo" | "Stratified"
        Cross-validation fold assignment scheme, if fold_column is not specified. The 'Stratified' option will stratify
        the folds based on the response variable, for classification problems.
        Default: "AUTO"

      fold_column : VecSpecifier
        Column with cross-validation fold index assignment per observation.

      keep_cross_validation_predictions : bool
        Whether to keep the predictions of the cross-validation models.
        Default: False

      keep_cross_validation_fold_assignment : bool
        Whether to keep the cross-validation fold assignment.
        Default: False

      training_frame : str
        Id of the training data frame (Not required, to allow initial validation of model parameters).

      validation_frame : str
        Id of the validation data frame.

      response_column : VecSpecifier
        Response variable column.

      ignored_columns : list(str)
        Names of columns to ignore for training.

      ignore_const_cols : bool
        Ignore constant columns.
        Default: True

      score_each_iteration : bool
        Whether to score during each iteration of model training.
        Default: False

      balance_classes : bool
        Balance training data class counts via over/under-sampling (for imbalanced data).
        Default: False

      class_sampling_factors : list(float)
        Desired over/under-sampling ratios per class (in lexicographic order). If not specified, sampling factors will
        be automatically computed to obtain class balance during training. Requires balance_classes.

      max_after_balance_size : float
        Maximum relative size of the training data after balancing class counts (can be less than 1.0). Requires
        balance_classes.
        Default: 5.0

      max_confusion_matrix_size : int
        Maximum size (# classes) for confusion matrices to be printed in the Logs
        Default: 20

      max_hit_ratio_k : int
        Max. number (top K) of predictions to use for hit ratio computation (for multi-class only, 0 to disable)
        Default: 0

      laplace : float
        Laplace smoothing parameter
        Default: 0.0

      min_sdev : float
        Min. standard deviation to use for observations with not enough data
        Default: 0.001

      eps_sdev : float
        Cutoff below which standard deviation is replaced with min_sdev
        Default: 0.0

      min_prob : float
        Min. probability to use for observations with not enough data
        Default: 0.001

      eps_prob : float
        Cutoff below which probability is replaced with min_prob
        Default: 0.0

      compute_metrics : bool
        Compute metrics on training data
        Default: True

      max_runtime_secs : float
        Maximum allowed runtime in seconds for model training. Use 0 to disable.
        Default: 0.0

    """
    def __init__(self, **kwargs):
        super(H2ONaiveBayesEstimator, self).__init__()
        self._parms = {}
        for name in ["model_id", "nfolds", "seed", "fold_assignment", "fold_column",
                     "keep_cross_validation_predictions", "keep_cross_validation_fold_assignment", "training_frame",
                     "validation_frame", "response_column", "ignored_columns", "ignore_const_cols",
                     "score_each_iteration", "balance_classes", "class_sampling_factors", "max_after_balance_size",
                     "max_confusion_matrix_size", "max_hit_ratio_k", "laplace", "min_sdev", "eps_sdev", "min_prob",
                     "eps_prob", "compute_metrics", "max_runtime_secs"]:
            pname = name[:-1] if name[-1] == '_' else name
            self._parms[pname] = kwargs[name] if name in kwargs else None

    @property
    def nfolds(self):
        return self._parms["nfolds"]

    @nfolds.setter
    def nfolds(self, value):
        self._parms["nfolds"] = value

    @property
    def seed(self):
        return self._parms["seed"]

    @seed.setter
    def seed(self, value):
        self._parms["seed"] = value

    @property
    def fold_assignment(self):
        return self._parms["fold_assignment"]

    @fold_assignment.setter
    def fold_assignment(self, value):
        self._parms["fold_assignment"] = value

    @property
    def fold_column(self):
        return self._parms["fold_column"]

    @fold_column.setter
    def fold_column(self, value):
        self._parms["fold_column"] = value

    @property
    def keep_cross_validation_predictions(self):
        return self._parms["keep_cross_validation_predictions"]

    @keep_cross_validation_predictions.setter
    def keep_cross_validation_predictions(self, value):
        self._parms["keep_cross_validation_predictions"] = value

    @property
    def keep_cross_validation_fold_assignment(self):
        return self._parms["keep_cross_validation_fold_assignment"]

    @keep_cross_validation_fold_assignment.setter
    def keep_cross_validation_fold_assignment(self, value):
        self._parms["keep_cross_validation_fold_assignment"] = value

    @property
    def training_frame(self):
        return self._parms["training_frame"]

    @training_frame.setter
    def training_frame(self, value):
        self._parms["training_frame"] = value

    @property
    def validation_frame(self):
        return self._parms["validation_frame"]

    @validation_frame.setter
    def validation_frame(self, value):
        self._parms["validation_frame"] = value

    @property
    def response_column(self):
        return self._parms["response_column"]

    @response_column.setter
    def response_column(self, value):
        self._parms["response_column"] = value

    @property
    def ignored_columns(self):
        return self._parms["ignored_columns"]

    @ignored_columns.setter
    def ignored_columns(self, value):
        self._parms["ignored_columns"] = value

    @property
    def ignore_const_cols(self):
        return self._parms["ignore_const_cols"]

    @ignore_const_cols.setter
    def ignore_const_cols(self, value):
        self._parms["ignore_const_cols"] = value

    @property
    def score_each_iteration(self):
        return self._parms["score_each_iteration"]

    @score_each_iteration.setter
    def score_each_iteration(self, value):
        self._parms["score_each_iteration"] = value

    @property
    def balance_classes(self):
        return self._parms["balance_classes"]

    @balance_classes.setter
    def balance_classes(self, value):
        self._parms["balance_classes"] = value

    @property
    def class_sampling_factors(self):
        return self._parms["class_sampling_factors"]

    @class_sampling_factors.setter
    def class_sampling_factors(self, value):
        self._parms["class_sampling_factors"] = value

    @property
    def max_after_balance_size(self):
        return self._parms["max_after_balance_size"]

    @max_after_balance_size.setter
    def max_after_balance_size(self, value):
        self._parms["max_after_balance_size"] = value

    @property
    def max_confusion_matrix_size(self):
        return self._parms["max_confusion_matrix_size"]

    @max_confusion_matrix_size.setter
    def max_confusion_matrix_size(self, value):
        self._parms["max_confusion_matrix_size"] = value

    @property
    def max_hit_ratio_k(self):
        return self._parms["max_hit_ratio_k"]

    @max_hit_ratio_k.setter
    def max_hit_ratio_k(self, value):
        self._parms["max_hit_ratio_k"] = value

    @property
    def laplace(self):
        return self._parms["laplace"]

    @laplace.setter
    def laplace(self, value):
        self._parms["laplace"] = value

    @property
    def min_sdev(self):
        return self._parms["min_sdev"]

    @min_sdev.setter
    def min_sdev(self, value):
        self._parms["min_sdev"] = value

    @property
    def eps_sdev(self):
        return self._parms["eps_sdev"]

    @eps_sdev.setter
    def eps_sdev(self, value):
        self._parms["eps_sdev"] = value

    @property
    def min_prob(self):
        return self._parms["min_prob"]

    @min_prob.setter
    def min_prob(self, value):
        self._parms["min_prob"] = value

    @property
    def eps_prob(self):
        return self._parms["eps_prob"]

    @eps_prob.setter
    def eps_prob(self, value):
        self._parms["eps_prob"] = value

    @property
    def compute_metrics(self):
        return self._parms["compute_metrics"]

    @compute_metrics.setter
    def compute_metrics(self, value):
        self._parms["compute_metrics"] = value

    @property
    def max_runtime_secs(self):
        return self._parms["max_runtime_secs"]

    @max_runtime_secs.setter
    def max_runtime_secs(self, value):
        self._parms["max_runtime_secs"] = value

    # overrides superclass
    def _compute_algo(self):
        return "naivebayes"

