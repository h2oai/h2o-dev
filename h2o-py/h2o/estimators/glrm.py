#!/usr/bin/env python
# -*- encoding: utf-8 -*-
#
# This file is auto-generated by h2o-3/h2o-bindings/bin/gen_python.py
# Copyright 2016 H2O.ai;  Apache License Version 2.0 (see LICENSE for details)
#
from __future__ import absolute_import, division, print_function, unicode_literals

import re
from h2o.estimators.estimator_base import H2OEstimator
from h2o.exceptions import H2OValueError
from h2o.utils.typechecks import assert_is_type, numeric


class H2OGeneralizedLowRankEstimator(H2OEstimator):
    """
    Generalized Low Rank Modeling

    Builds a generalized low rank model of a H2O dataset.
    """

    algo = "glrm"

    def __init__(self, **kwargs):
        super(H2OGeneralizedLowRankEstimator, self).__init__()
        self._parms = {}
        names_list = {"model_id", "training_frame", "validation_frame", "ignored_columns", "ignore_const_cols",
                      "score_each_iteration", "loading_name", "transform", "k", "loss", "loss_by_col",
                      "loss_by_col_idx", "multi_loss", "period", "regularization_x", "regularization_y", "gamma_x",
                      "gamma_y", "max_iterations", "max_updates", "init_step_size", "min_step_size", "seed", "init",
                      "svd_method", "user_y", "user_x", "expand_user_y", "impute_original", "recover_svd",
                      "max_runtime_secs"}
        if "Lambda" in kwargs: kwargs["lambda_"] = kwargs.pop("Lambda")
        for pname in kwargs:
            sname = pname[:-1] if pname[-1] == '_' else pname
            if pname in names_list:
                self._parms[sname] = kwargs[pname]
            else:
                raise H2OValueError("Unknown parameter %s" % pname)
        self._parms["_rest_version"] = 3

    @property
    def training_frame(self):
        """str: Id of the training data frame (Not required, to allow initial validation of model parameters)."""
        return self._parms.get("training_frame")

    @training_frame.setter
    def training_frame(self, value):
        assert_is_type(value, str)
        self._parms["training_frame"] = value


    @property
    def validation_frame(self):
        """str: Id of the validation data frame."""
        return self._parms.get("validation_frame")

    @validation_frame.setter
    def validation_frame(self, value):
        assert_is_type(value, str)
        self._parms["validation_frame"] = value


    @property
    def ignored_columns(self):
        """List[str]: Names of columns to ignore for training."""
        return self._parms.get("ignored_columns")

    @ignored_columns.setter
    def ignored_columns(self, value):
        assert_is_type(value, [str])
        self._parms["ignored_columns"] = value


    @property
    def ignore_const_cols(self):
        """bool: Ignore constant columns. (Default: True)"""
        return self._parms.get("ignore_const_cols")

    @ignore_const_cols.setter
    def ignore_const_cols(self, value):
        assert_is_type(value, bool)
        self._parms["ignore_const_cols"] = value


    @property
    def score_each_iteration(self):
        """bool: Whether to score during each iteration of model training. (Default: False)"""
        return self._parms.get("score_each_iteration")

    @score_each_iteration.setter
    def score_each_iteration(self, value):
        assert_is_type(value, bool)
        self._parms["score_each_iteration"] = value


    @property
    def loading_name(self):
        """str: Frame key to save resulting X"""
        return self._parms.get("loading_name")

    @loading_name.setter
    def loading_name(self, value):
        assert_is_type(value, str)
        self._parms["loading_name"] = value


    @property
    def transform(self):
        """
        Enum["none", "standardize", "normalize", "demean", "descale"]: Transformation of training data (Default: "none")
        """
        return self._parms.get("transform")

    @transform.setter
    def transform(self, value):
        simple_val = re.sub(r"[^a-z]+", "", value.lower())
        assert_is_type(simple_val, "none", "standardize", "normalize", "demean", "descale")
        self._parms["transform"] = value


    @property
    def k(self):
        """int: Rank of matrix approximation (Default: 1)"""
        return self._parms.get("k")

    @k.setter
    def k(self, value):
        assert_is_type(value, int)
        self._parms["k"] = value


    @property
    def loss(self):
        """
        Enum["quadratic", "absolute", "huber", "poisson", "hinge", "logistic", "periodic"]: Numeric loss function
        (Default: "quadratic")
        """
        return self._parms.get("loss")

    @loss.setter
    def loss(self, value):
        simple_val = re.sub(r"[^a-z]+", "", value.lower())
        assert_is_type(simple_val, "quadratic", "absolute", "huber", "poisson", "hinge", "logistic", "periodic")
        self._parms["loss"] = value


    @property
    def loss_by_col(self):
        """
        List[Enum["quadratic", "absolute", "huber", "poisson", "hinge", "logistic", "periodic", "categorical",
        "ordinal"]]: Loss function by column (override)
        """
        return self._parms.get("loss_by_col")

    @loss_by_col.setter
    def loss_by_col(self, value):
        simple_val = re.sub(r"[^a-z]+", "", value.lower())
        assert_is_type(simple_val, ["quadratic", "absolute", "huber", "poisson", "hinge", "logistic", "periodic", "categorical", "ordinal"])
        self._parms["loss_by_col"] = value


    @property
    def loss_by_col_idx(self):
        """List[int]: Loss function by column index (override)"""
        return self._parms.get("loss_by_col_idx")

    @loss_by_col_idx.setter
    def loss_by_col_idx(self, value):
        assert_is_type(value, [int])
        self._parms["loss_by_col_idx"] = value


    @property
    def multi_loss(self):
        """Enum["categorical", "ordinal"]: Categorical loss function (Default: "categorical")"""
        return self._parms.get("multi_loss")

    @multi_loss.setter
    def multi_loss(self, value):
        simple_val = re.sub(r"[^a-z]+", "", value.lower())
        assert_is_type(simple_val, "categorical", "ordinal")
        self._parms["multi_loss"] = value


    @property
    def period(self):
        """int: Length of period (only used with periodic loss function) (Default: 1)"""
        return self._parms.get("period")

    @period.setter
    def period(self, value):
        assert_is_type(value, int)
        self._parms["period"] = value


    @property
    def regularization_x(self):
        """
        Enum["none", "quadratic", "l2", "l1", "non_negative", "one_sparse", "unit_one_sparse", "simplex"]:
        Regularization function for X matrix (Default: "none")
        """
        return self._parms.get("regularization_x")

    @regularization_x.setter
    def regularization_x(self, value):
        simple_val = re.sub(r"[^a-z]+", "", value.lower())
        assert_is_type(simple_val, "none", "quadratic", "l", "l", "nonnegative", "onesparse", "unitonesparse", "simplex")
        self._parms["regularization_x"] = value


    @property
    def regularization_y(self):
        """
        Enum["none", "quadratic", "l2", "l1", "non_negative", "one_sparse", "unit_one_sparse", "simplex"]:
        Regularization function for Y matrix (Default: "none")
        """
        return self._parms.get("regularization_y")

    @regularization_y.setter
    def regularization_y(self, value):
        simple_val = re.sub(r"[^a-z]+", "", value.lower())
        assert_is_type(simple_val, "none", "quadratic", "l", "l", "nonnegative", "onesparse", "unitonesparse", "simplex")
        self._parms["regularization_y"] = value


    @property
    def gamma_x(self):
        """float: Regularization weight on X matrix (Default: 0.0)"""
        return self._parms.get("gamma_x")

    @gamma_x.setter
    def gamma_x(self, value):
        assert_is_type(value, numeric)
        self._parms["gamma_x"] = value


    @property
    def gamma_y(self):
        """float: Regularization weight on Y matrix (Default: 0.0)"""
        return self._parms.get("gamma_y")

    @gamma_y.setter
    def gamma_y(self, value):
        assert_is_type(value, numeric)
        self._parms["gamma_y"] = value


    @property
    def max_iterations(self):
        """int: Maximum number of iterations (Default: 1000)"""
        return self._parms.get("max_iterations")

    @max_iterations.setter
    def max_iterations(self, value):
        assert_is_type(value, int)
        self._parms["max_iterations"] = value


    @property
    def max_updates(self):
        """int: Maximum number of updates (Default: 2000)"""
        return self._parms.get("max_updates")

    @max_updates.setter
    def max_updates(self, value):
        assert_is_type(value, int)
        self._parms["max_updates"] = value


    @property
    def init_step_size(self):
        """float: Initial step size (Default: 1.0)"""
        return self._parms.get("init_step_size")

    @init_step_size.setter
    def init_step_size(self, value):
        assert_is_type(value, numeric)
        self._parms["init_step_size"] = value


    @property
    def min_step_size(self):
        """float: Minimum step size (Default: 0.0001)"""
        return self._parms.get("min_step_size")

    @min_step_size.setter
    def min_step_size(self, value):
        assert_is_type(value, numeric)
        self._parms["min_step_size"] = value


    @property
    def seed(self):
        """int: RNG seed for initialization (Default: -1)"""
        return self._parms.get("seed")

    @seed.setter
    def seed(self, value):
        assert_is_type(value, int)
        self._parms["seed"] = value


    @property
    def init(self):
        """Enum["random", "svd", "plus_plus", "user"]: Initialization mode (Default: "plus_plus")"""
        return self._parms.get("init")

    @init.setter
    def init(self, value):
        simple_val = re.sub(r"[^a-z]+", "", value.lower())
        assert_is_type(simple_val, "random", "svd", "plusplus", "user")
        self._parms["init"] = value


    @property
    def svd_method(self):
        """
        Enum["gram_s_v_d", "power", "randomized"]: Method for computing SVD during initialization (Caution: Power and
        Randomized are currently experimental and unstable) (Default: "randomized")
        """
        return self._parms.get("svd_method")

    @svd_method.setter
    def svd_method(self, value):
        simple_val = re.sub(r"[^a-z]+", "", value.lower())
        assert_is_type(simple_val, "gramsvd", "power", "randomized")
        self._parms["svd_method"] = value


    @property
    def user_y(self):
        """str: User-specified initial Y"""
        return self._parms.get("user_y")

    @user_y.setter
    def user_y(self, value):
        assert_is_type(value, str)
        self._parms["user_y"] = value


    @property
    def user_x(self):
        """str: User-specified initial X"""
        return self._parms.get("user_x")

    @user_x.setter
    def user_x(self, value):
        assert_is_type(value, str)
        self._parms["user_x"] = value


    @property
    def expand_user_y(self):
        """bool: Expand categorical columns in user-specified initial Y (Default: True)"""
        return self._parms.get("expand_user_y")

    @expand_user_y.setter
    def expand_user_y(self, value):
        assert_is_type(value, bool)
        self._parms["expand_user_y"] = value


    @property
    def impute_original(self):
        """bool: Reconstruct original training data by reversing transform (Default: False)"""
        return self._parms.get("impute_original")

    @impute_original.setter
    def impute_original(self, value):
        assert_is_type(value, bool)
        self._parms["impute_original"] = value


    @property
    def recover_svd(self):
        """bool: Recover singular values and eigenvectors of XY (Default: False)"""
        return self._parms.get("recover_svd")

    @recover_svd.setter
    def recover_svd(self, value):
        assert_is_type(value, bool)
        self._parms["recover_svd"] = value


    @property
    def max_runtime_secs(self):
        """float: Maximum allowed runtime in seconds for model training. Use 0 to disable. (Default: 0.0)"""
        return self._parms.get("max_runtime_secs")

    @max_runtime_secs.setter
    def max_runtime_secs(self, value):
        assert_is_type(value, numeric)
        self._parms["max_runtime_secs"] = value


