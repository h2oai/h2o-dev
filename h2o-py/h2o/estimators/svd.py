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


class H2OSingularValueDecompositionEstimator(H2OEstimator):
    """
    Singular Value Decomposition

    """

    algo = "svd"
    supervised_learning = False

    def __init__(self,
                 model_id=None,  # type: Optional[Union[None, str, H2OEstimator]]
                 training_frame=None,  # type: Optional[Union[None, str, H2OFrame]]
                 validation_frame=None,  # type: Optional[Union[None, str, H2OFrame]]
                 ignored_columns=None,  # type: Optional[List[str]]
                 ignore_const_cols=True,  # type: bool
                 score_each_iteration=False,  # type: bool
                 transform="none",  # type: Literal["none", "standardize", "normalize", "demean", "descale"]
                 svd_method="gram_s_v_d",  # type: Literal["gram_s_v_d", "power", "randomized"]
                 nv=1,  # type: int
                 max_iterations=1000,  # type: int
                 seed=-1,  # type: int
                 keep_u=True,  # type: bool
                 u_name=None,  # type: Optional[str]
                 use_all_factor_levels=True,  # type: bool
                 max_runtime_secs=0.0,  # type: float
                 export_checkpoints_dir=None,  # type: Optional[str]
                 ):
        """
        :param model_id: Destination id for this model; auto-generated if not specified.
               Defaults to ``None``.
        :type model_id: Union[None, str, H2OEstimator], optional
        :param training_frame: Id of the training data frame.
               Defaults to ``None``.
        :type training_frame: Union[None, str, H2OFrame], optional
        :param validation_frame: Id of the validation data frame.
               Defaults to ``None``.
        :type validation_frame: Union[None, str, H2OFrame], optional
        :param ignored_columns: Names of columns to ignore for training.
               Defaults to ``None``.
        :type ignored_columns: List[str], optional
        :param ignore_const_cols: Ignore constant columns.
               Defaults to ``True``.
        :type ignore_const_cols: bool
        :param score_each_iteration: Whether to score during each iteration of model training.
               Defaults to ``False``.
        :type score_each_iteration: bool
        :param transform: Transformation of training data
               Defaults to ``"none"``.
        :type transform: Literal["none", "standardize", "normalize", "demean", "descale"]
        :param svd_method: Method for computing SVD (Caution: Randomized is currently experimental and unstable)
               Defaults to ``"gram_s_v_d"``.
        :type svd_method: Literal["gram_s_v_d", "power", "randomized"]
        :param nv: Number of right singular vectors
               Defaults to ``1``.
        :type nv: int
        :param max_iterations: Maximum iterations
               Defaults to ``1000``.
        :type max_iterations: int
        :param seed: RNG seed for k-means++ initialization
               Defaults to ``-1``.
        :type seed: int
        :param keep_u: Save left singular vectors?
               Defaults to ``True``.
        :type keep_u: bool
        :param u_name: Frame key to save left singular vectors
               Defaults to ``None``.
        :type u_name: str, optional
        :param use_all_factor_levels: Whether first factor level is included in each categorical expansion
               Defaults to ``True``.
        :type use_all_factor_levels: bool
        :param max_runtime_secs: Maximum allowed runtime in seconds for model training. Use 0 to disable.
               Defaults to ``0.0``.
        :type max_runtime_secs: float
        :param export_checkpoints_dir: Automatically export generated models to this directory.
               Defaults to ``None``.
        :type export_checkpoints_dir: str, optional
        """
        super(H2OSingularValueDecompositionEstimator, self).__init__()
        self._parms = {}
        self._id = self._parms['model_id'] = model_id
        self.training_frame = training_frame
        self.validation_frame = validation_frame
        self.ignored_columns = ignored_columns
        self.ignore_const_cols = ignore_const_cols
        self.score_each_iteration = score_each_iteration
        self.transform = transform
        self.svd_method = svd_method
        self.nv = nv
        self.max_iterations = max_iterations
        self.seed = seed
        self.keep_u = keep_u
        self.u_name = u_name
        self.use_all_factor_levels = use_all_factor_levels
        self.max_runtime_secs = max_runtime_secs
        self.export_checkpoints_dir = export_checkpoints_dir
        self._parms["_rest_version"] = 99

    @property
    def training_frame(self):
        """
        Id of the training data frame.

        Type: ``Union[None, str, H2OFrame]``.

        :examples:

        >>> arrests = h2o.import_file("https://s3.amazonaws.com/h2o-public-test-data/smalldata/pca_test/USArrests.csv")
        >>> fit_h2o = H2OSingularValueDecompositionEstimator()
        >>> fit_h2o.train(x=list(range(4)), training_frame=arrests)
        >>> fit_h2o
        """
        return self._parms.get("training_frame")

    @training_frame.setter
    def training_frame(self, training_frame):
        self._parms["training_frame"] = H2OFrame._validate(training_frame, 'training_frame')

    @property
    def validation_frame(self):
        """
        Id of the validation data frame.

        Type: ``Union[None, str, H2OFrame]``.

        :examples:

        >>> arrests = h2o.import_file("https://s3.amazonaws.com/h2o-public-test-data/smalldata/pca_test/USArrests.csv")
        >>> train, valid = arrests.split_frame(ratios=[.8])
        >>> fit_h2o = H2OSingularValueDecompositionEstimator()
        >>> fit_h2o.train(x=list(range(4)),
        ...               training_frame=train,
        ...               validation_frame=valid)
        >>> fit_h2o
        """
        return self._parms.get("validation_frame")

    @validation_frame.setter
    def validation_frame(self, validation_frame):
        self._parms["validation_frame"] = H2OFrame._validate(validation_frame, 'validation_frame')

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

        >>> arrests = h2o.import_file("https://s3.amazonaws.com/h2o-public-test-data/smalldata/pca_test/USArrests.csv")
        >>> fit_h2o = H2OSingularValueDecompositionEstimator(ignore_const_cols=False,
        ...                                                  nv=4)
        >>> fit_h2o.train(x=list(range(4)), training_frame=arrests)
        >>> fit_h2o
        """
        return self._parms.get("ignore_const_cols")

    @ignore_const_cols.setter
    def ignore_const_cols(self, ignore_const_cols):
        assert_is_type(ignore_const_cols, None, bool)
        self._parms["ignore_const_cols"] = ignore_const_cols

    @property
    def score_each_iteration(self):
        """
        Whether to score during each iteration of model training.

        Type: ``bool``, defaults to ``False``.

        :examples:

        >>> arrests = h2o.import_file("https://s3.amazonaws.com/h2o-public-test-data/smalldata/pca_test/USArrests.csv")
        >>> fit_h2o = H2OSingularValueDecompositionEstimator(nv=4,
        ...                                                  score_each_iteration=True)
        >>> fit_h2o.train(x=list(range(4)), training_frame=arrests)
        >>> fit_h2o
        """
        return self._parms.get("score_each_iteration")

    @score_each_iteration.setter
    def score_each_iteration(self, score_each_iteration):
        assert_is_type(score_each_iteration, None, bool)
        self._parms["score_each_iteration"] = score_each_iteration

    @property
    def transform(self):
        """
        Transformation of training data

        Type: ``Literal["none", "standardize", "normalize", "demean", "descale"]``, defaults to ``"none"``.

        :examples:

        >>> arrests = h2o.import_file("https://s3.amazonaws.com/h2o-public-test-data/smalldata/pca_test/USArrests.csv")
        >>> fit_h2o = H2OSingularValueDecompositionEstimator(nv=4,
        ...                                                  transform="standardize",
        ...                                                  max_iterations=2000)
        >>> fit_h2o.train(x=list(range(4)), training_frame=arrests)
        >>> fit_h2o
        """
        return self._parms.get("transform")

    @transform.setter
    def transform(self, transform):
        assert_is_type(transform, None, Enum("none", "standardize", "normalize", "demean", "descale"))
        self._parms["transform"] = transform

    @property
    def svd_method(self):
        """
        Method for computing SVD (Caution: Randomized is currently experimental and unstable)

        Type: ``Literal["gram_s_v_d", "power", "randomized"]``, defaults to ``"gram_s_v_d"``.

        :examples:

        >>> arrests = h2o.import_file("https://s3.amazonaws.com/h2o-public-test-data/smalldata/pca_test/USArrests.csv")
        >>> fit_h2o = H2OSingularValueDecompositionEstimator(svd_method="power")
        >>> fit_h2o.train(x=list(range(4)), training_frame=arrests)
        >>> fit_h2o
        """
        return self._parms.get("svd_method")

    @svd_method.setter
    def svd_method(self, svd_method):
        assert_is_type(svd_method, None, Enum("gram_s_v_d", "power", "randomized"))
        self._parms["svd_method"] = svd_method

    @property
    def nv(self):
        """
        Number of right singular vectors

        Type: ``int``, defaults to ``1``.

        :examples:

        >>> arrests = h2o.import_file("https://s3.amazonaws.com/h2o-public-test-data/smalldata/pca_test/USArrests.csv")
        >>> fit_h2o = H2OSingularValueDecompositionEstimator(nv=4,
        ...                                                  transform="standardize",
        ...                                                  max_iterations=2000)
        >>> fit_h2o.train(x=list(range(4)), training_frame=arrests)
        >>> fit_h2o
        """
        return self._parms.get("nv")

    @nv.setter
    def nv(self, nv):
        assert_is_type(nv, None, int)
        self._parms["nv"] = nv

    @property
    def max_iterations(self):
        """
        Maximum iterations

        Type: ``int``, defaults to ``1000``.

        :examples:

        >>> arrests = h2o.import_file("https://s3.amazonaws.com/h2o-public-test-data/smalldata/pca_test/USArrests.csv")
        >>> fit_h2o = H2OSingularValueDecompositionEstimator(nv=4,
        ...                                                  transform="standardize",
        ...                                                  max_iterations=2000)
        >>> fit_h2o.train(x=list(range(4)), training_frame=arrests)
        >>> fit_h2o
        """
        return self._parms.get("max_iterations")

    @max_iterations.setter
    def max_iterations(self, max_iterations):
        assert_is_type(max_iterations, None, int)
        self._parms["max_iterations"] = max_iterations

    @property
    def seed(self):
        """
        RNG seed for k-means++ initialization

        Type: ``int``, defaults to ``-1``.

        :examples:

        >>> arrests = h2o.import_file("https://s3.amazonaws.com/h2o-public-test-data/smalldata/pca_test/USArrests.csv")
        >>> fit_h2o = H2OSingularValueDecompositionEstimator(nv=4, seed=-3)
        >>> fit_h2o.train(x=list(range(4)), training_frame=arrests)
        >>> fit_h2o
        """
        return self._parms.get("seed")

    @seed.setter
    def seed(self, seed):
        assert_is_type(seed, None, int)
        self._parms["seed"] = seed

    @property
    def keep_u(self):
        """
        Save left singular vectors?

        Type: ``bool``, defaults to ``True``.

        :examples:

        >>> arrests = h2o.import_file("https://s3.amazonaws.com/h2o-public-test-data/smalldata/pca_test/USArrests.csv")
        >>> fit_h2o = H2OSingularValueDecompositionEstimator(keep_u=False)
        >>> fit_h2o.train(x=list(range(4)), training_frame=arrests)
        >>> fit_h2o
        """
        return self._parms.get("keep_u")

    @keep_u.setter
    def keep_u(self, keep_u):
        assert_is_type(keep_u, None, bool)
        self._parms["keep_u"] = keep_u

    @property
    def u_name(self):
        """
        Frame key to save left singular vectors

        Type: ``str``.

        :examples:

        >>> arrests = h2o.import_file("https://s3.amazonaws.com/h2o-public-test-data/smalldata/pca_test/USArrests.csv")
        >>> fit_h2o = H2OSingularValueDecompositionEstimator(u_name="fit_h2o")
        >>> fit_h2o.train(x=list(range(4)), training_frame=arrests)
        >>> fit_h2o.u_name
        >>> fit_h2o
        """
        return self._parms.get("u_name")

    @u_name.setter
    def u_name(self, u_name):
        assert_is_type(u_name, None, str)
        self._parms["u_name"] = u_name

    @property
    def use_all_factor_levels(self):
        """
        Whether first factor level is included in each categorical expansion

        Type: ``bool``, defaults to ``True``.

        :examples:

        >>> arrests = h2o.import_file("https://s3.amazonaws.com/h2o-public-test-data/smalldata/pca_test/USArrests.csv")
        >>> fit_h2o = H2OSingularValueDecompositionEstimator(use_all_factor_levels=False)
        >>> fit_h2o.train(x=list(range(4)), training_frame=arrests)
        >>> fit_h2o
        """
        return self._parms.get("use_all_factor_levels")

    @use_all_factor_levels.setter
    def use_all_factor_levels(self, use_all_factor_levels):
        assert_is_type(use_all_factor_levels, None, bool)
        self._parms["use_all_factor_levels"] = use_all_factor_levels

    @property
    def max_runtime_secs(self):
        """
        Maximum allowed runtime in seconds for model training. Use 0 to disable.

        Type: ``float``, defaults to ``0.0``.

        :examples:

        >>> arrests = h2o.import_file("https://s3.amazonaws.com/h2o-public-test-data/smalldata/pca_test/USArrests.csv")
        >>> fit_h2o = H2OSingularValueDecompositionEstimator(nv=4,
        ...                                                  transform="standardize",
        ...                                                  max_runtime_secs=25)
        >>> fit_h2o.train(x=list(range(4)), training_frame=arrests)
        >>> fit_h2o
        """
        return self._parms.get("max_runtime_secs")

    @max_runtime_secs.setter
    def max_runtime_secs(self, max_runtime_secs):
        assert_is_type(max_runtime_secs, None, numeric)
        self._parms["max_runtime_secs"] = max_runtime_secs

    @property
    def export_checkpoints_dir(self):
        """
        Automatically export generated models to this directory.

        Type: ``str``.

        :examples:

        >>> import tempfile
        >>> from os import listdir
        >>> arrests = h2o.import_file("https://s3.amazonaws.com/h2o-public-test-data/smalldata/pca_test/USArrests.csv")
        >>> checkpoints_dir = tempfile.mkdtemp()
        >>> fit_h2o = H2OSingularValueDecompositionEstimator(export_checkpoints_dir=checkpoints_dir,
        ...                                                  seed=-5)
        >>> fit_h2o.train(x=list(range(4)), training_frame=arrests)
        >>> len(listdir(checkpoints_dir))
        """
        return self._parms.get("export_checkpoints_dir")

    @export_checkpoints_dir.setter
    def export_checkpoints_dir(self, export_checkpoints_dir):
        assert_is_type(export_checkpoints_dir, None, str)
        self._parms["export_checkpoints_dir"] = export_checkpoints_dir

    def init_for_pipeline(self):
        """
        Returns H2OSVD object which implements fit and transform method to be used in sklearn.Pipeline properly.
        All parameters defined in self.__params, should be input parameters in H2OSVD.__init__ method.

        :returns: H2OSVD object

        :examples:

        >>> from h2o.transforms.preprocessing import H2OScaler
        >>> from h2o.estimators import H2ORandomForestEstimator
        >>> from h2o.estimators import H2OSingularValueDecompositionEstimator
        >>> from sklearn.pipeline import Pipeline
        >>> arrests = h2o.import_file("https://s3.amazonaws.com/h2o-public-test-data/smalldata/pca_test/USArrests.csv")
        >>> pipe = Pipeline([("standardize", H2OScaler()),
        ...                  ("svd", H2OSingularValueDecompositionEstimator(nv=3).init_for_pipeline()),
        ...                  ("rf", H2ORandomForestEstimator(seed=42,ntrees=50))])
        >>> pipe.fit(arrests[1:], arrests[0])
        """
        import inspect
        from h2o.transforms.decomposition import H2OSVD
        # check which parameters can be passed to H2OSVD init
        var_names = list(dict(inspect.getmembers(H2OSVD.__init__.__code__))['co_varnames'])
        parameters = {k: v for k, v in self._parms.items() if k in var_names}
        return H2OSVD(**parameters)

