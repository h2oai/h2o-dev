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
import h2o


class H2OTargetencoderEstimator(H2OEstimator):
    """
    TargetEncoder

    """

    algo = "targetencoder"

    def __init__(self, **kwargs):
        super(H2OTargetencoderEstimator, self).__init__()
        self._parms = {}
        names_list = {"encoded_columns", "target_column", "k", "f", "data_leakage_handling", "model_id",
                      "training_frame", "fold_column"}
        if "Lambda" in kwargs: kwargs["lambda_"] = kwargs.pop("Lambda")
        for pname, pvalue in kwargs.items():
            if pname == 'model_id':
                self._id = pvalue
                self._parms["model_id"] = pvalue
            elif pname in names_list:
                # Using setattr(...) will invoke type-checking of the arguments
                setattr(self, pname, pvalue)
            else:
                raise H2OValueError("Unknown parameter %s = %r" % (pname, pvalue))

    @property
    def encoded_columns(self):
        """
        Columnds to encode.

        Type: ``List[str]``.
        """
        return self._parms.get("encoded_columns")

    @encoded_columns.setter
    def encoded_columns(self, encoded_columns):
        assert_is_type(encoded_columns, None, [str])
        self._parms["encoded_columns"] = encoded_columns


    @property
    def target_column(self):
        """
        Target column for the encoding

        Type: ``str``.
        """
        return self._parms.get("target_column")

    @target_column.setter
    def target_column(self, target_column):
        assert_is_type(target_column, None, str)
        self._parms["target_column"] = target_column


    @property
    def k(self):
        """
        Parameter 'k' used for blending (if enabled). Blending is to be enabled separately using the 'blending'
        parameter.

        Type: ``float``  (default: ``0``).
        """
        return self._parms.get("k")

    @k.setter
    def k(self, k):
        assert_is_type(k, None, numeric)
        self._parms["k"] = k


    @property
    def f(self):
        """
        Parameter 'f' used for blending (if enabled). Blending is to be enabled separately using the 'blending'
        parameter.

        Type: ``float``  (default: ``0``).
        """
        return self._parms.get("f")

    @f.setter
    def f(self, f):
        assert_is_type(f, None, numeric)
        self._parms["f"] = f


    @property
    def data_leakage_handling(self):
        """
        Data leakage handling strategy. Default to None.

        One of: ``"none"``, ``"k_fold"``, ``"leave_one_out"``.
        """
        return self._parms.get("data_leakage_handling")

    @data_leakage_handling.setter
    def data_leakage_handling(self, data_leakage_handling):
        assert_is_type(data_leakage_handling, None, Enum("none", "k_fold", "leave_one_out"))
        self._parms["data_leakage_handling"] = data_leakage_handling


    @property
    def training_frame(self):
        """
        Id of the training data frame.

        Type: ``H2OFrame``.
        """
        return self._parms.get("training_frame")

    @training_frame.setter
    def training_frame(self, training_frame):
        self._parms["training_frame"] = H2OFrame._validate(training_frame, 'training_frame')


    @property
    def fold_column(self):
        """
        Column with cross-validation fold index assignment per observation.

        Type: ``str``.
        """
        return self._parms.get("fold_column")

    @fold_column.setter
    def fold_column(self, fold_column):
        assert_is_type(fold_column, None, str)
        self._parms["fold_column"] = fold_column



    def transform(self, frame, data_leakage_handling="None", noise=-1, seed=-1):
        """
        Deprecated API. Please use H2OTargetencoderEstimator instead.

        Apply transformation to `te_columns` based on the encoding maps generated during `trains()` method call.

        :param frame frame: to which frame we are applying target encoding transformations.
        :param str data_leakage_handling: Supported options:

        1) "KFold" - encodings for a fold are generated based on out-of-fold data.
        2) "LeaveOneOut" - leave one out. Current row's response value is subtracted from the pre-calculated per-level frequencies.
        3) "None" - we do not holdout anything. Using whole frame for training

        :param float noise: the amount of random noise added to the target encoding.  This helps prevent overfitting. Defaults to 0.01 * range of y.
        :param int seed: a random seed used to generate draws from the uniform distribution for random noise. Defaults to -1.

        :example:
        >>> targetEncoder = TargetEncoder(x=te_columns, y=responseColumnName, blended_avg=True, inflection_point=10, smoothing=20)
                            >>> encodedTrain = targetEncoder.transform(frame=trainFrame, data_leakage_handling="kfold", seed=1234, is_train_or_valid=True)
        """
        output = h2o.api("GET /3/TargetEncoderTransform", data={'model': self.model_id, 'frame': frame.key,
                                                                'data_leakage_handling': data_leakage_handling,
                                                                'noise': noise,
                                                                'seed': seed})
        return h2o.get_frame(output["name"])
