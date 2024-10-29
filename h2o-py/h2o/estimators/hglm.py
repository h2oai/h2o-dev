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


class H2OHGLMEstimator(H2OEstimator):
    """
    Hierarchical Generalized Linear Model

    Fits a HGLM model with both the residual noise and random effect being modeled by Gaussian distribution.  The fixed
    effect coefficients are specified in parameter x, the random effect coefficients are specified in parameter 
    random_columns.  The column specified in group_column will contain the level 2 index value and must be an enum column.
    """

    algo = "hglm"
    supervised_learning = True

    def __init__(self,
                 model_id=None,  # type: Optional[Union[None, str, H2OEstimator]]
                 training_frame=None,  # type: Optional[Union[None, str, H2OFrame]]
                 validation_frame=None,  # type: Optional[Union[None, str, H2OFrame]]
                 response_column=None,  # type: Optional[str]
                 ignored_columns=None,  # type: Optional[List[str]]
                 ignore_const_cols=True,  # type: bool
                 offset_column=None,  # type: Optional[str]
                 weights_column=None,  # type: Optional[str]
                 max_runtime_secs=0.0,  # type: float
                 custom_metric_func=None,  # type: Optional[str]
                 score_each_iteration=False,  # type: bool
                 score_iteration_interval=5,  # type: int
                 seed=-1,  # type: int
                 missing_values_handling="mean_imputation",  # type: Literal["mean_imputation", "skip", "plug_values"]
                 plug_values=None,  # type: Optional[Union[None, str, H2OFrame]]
                 family="gaussian",  # type: Literal["gaussian"]
                 rand_family=None,  # type: Optional[Literal["gaussian"]]
                 max_iterations=-1,  # type: int
                 initial_fixed_effects=None,  # type: Optional[List[float]]
                 initial_random_effects=None,  # type: Optional[Union[None, str, H2OFrame]]
                 initial_t_matrix=None,  # type: Optional[Union[None, str, H2OFrame]]
                 tau_u_var_init=0.0,  # type: float
                 tau_e_var_init=0.0,  # type: float
                 random_columns=None,  # type: Optional[List[str]]
                 method="em",  # type: Literal["em"]
                 em_epsilon=0.001,  # type: float
                 random_intercept=True,  # type: bool
                 group_column=None,  # type: Optional[str]
                 gen_syn_data=False,  # type: bool
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
        :param response_column: Response variable column.
               Defaults to ``None``.
        :type response_column: str, optional
        :param ignored_columns: Names of columns to ignore for training.
               Defaults to ``None``.
        :type ignored_columns: List[str], optional
        :param ignore_const_cols: Ignore constant columns.
               Defaults to ``True``.
        :type ignore_const_cols: bool
        :param offset_column: Offset column. This will be added to the combination of columns before applying the link
               function.
               Defaults to ``None``.
        :type offset_column: str, optional
        :param weights_column: Column with observation weights. Giving some observation a weight of zero is equivalent
               to excluding it from the dataset; giving an observation a relative weight of 2 is equivalent to repeating
               that row twice. Negative weights are not allowed. Note: Weights are per-row observation weights and do
               not increase the size of the data frame. This is typically the number of times a row is repeated, but
               non-integer values are supported as well. During training, rows with higher weights matter more, due to
               the larger loss function pre-factor. If you set weight = 0 for a row, the returned prediction frame at
               that row is zero and this is incorrect. To get an accurate prediction, remove all rows with weight == 0.
               Defaults to ``None``.
        :type weights_column: str, optional
        :param max_runtime_secs: Maximum allowed runtime in seconds for model training. Use 0 to disable.
               Defaults to ``0.0``.
        :type max_runtime_secs: float
        :param custom_metric_func: Reference to custom evaluation function, format: `language:keyName=funcName`
               Defaults to ``None``.
        :type custom_metric_func: str, optional
        :param score_each_iteration: Whether to score during each iteration of model training.
               Defaults to ``False``.
        :type score_each_iteration: bool
        :param score_iteration_interval: Perform scoring for every score_iteration_interval iterations.
               Defaults to ``5``.
        :type score_iteration_interval: int
        :param seed: Seed for pseudo random number generator (if applicable).
               Defaults to ``-1``.
        :type seed: int
        :param missing_values_handling: Handling of missing values. Either MeanImputation, Skip or PlugValues.
               Defaults to ``"mean_imputation"``.
        :type missing_values_handling: Literal["mean_imputation", "skip", "plug_values"]
        :param plug_values: Plug Values (a single row frame containing values that will be used to impute missing values
               of the training/validation frame, use with conjunction missing_values_handling = PlugValues).
               Defaults to ``None``.
        :type plug_values: Union[None, str, H2OFrame], optional
        :param family: Family. Only gaussian is supported now.
               Defaults to ``"gaussian"``.
        :type family: Literal["gaussian"]
        :param rand_family: Set distribution of random effects.  Only Gaussian is implemented now.
               Defaults to ``None``.
        :type rand_family: Literal["gaussian"], optional
        :param max_iterations: Maximum number of iterations.  Value should >=1.  A value of 0 is only set when only the
               model coefficient names and model coefficient dimensions are needed.
               Defaults to ``-1``.
        :type max_iterations: int
        :param initial_fixed_effects: An array that contains initial values of the fixed effects coefficient.
               Defaults to ``None``.
        :type initial_fixed_effects: List[float], optional
        :param initial_random_effects: A H2OFrame id that contains initial values of the random effects coefficient.
               The row names shouldbe the random coefficient names.  If you are not sure what the random coefficient
               names are, build HGLM model with max_iterations = 0 and checkout the model output field
               random_coefficient_names.  The number of rows of this frame should be the number of level 2 units.
               Again, to figure this out, build HGLM model with max_iterations=0 and check out the model output field
               group_column_names.  The number of rows should equal the length of thegroup_column_names.
               Defaults to ``None``.
        :type initial_random_effects: Union[None, str, H2OFrame], optional
        :param initial_t_matrix: A H2OFrame id that contains initial values of the T matrix.  It should be a positive
               symmetric matrix.
               Defaults to ``None``.
        :type initial_t_matrix: Union[None, str, H2OFrame], optional
        :param tau_u_var_init: Initial variance of random coefficient effects.  If set, should provide a value > 0.0.
               If not set, will be randomly set in the model building process.
               Defaults to ``0.0``.
        :type tau_u_var_init: float
        :param tau_e_var_init: Initial variance of random noise.  If set, should provide a value > 0.0.  If not set,
               will be randomly set in the model building process.
               Defaults to ``0.0``.
        :type tau_e_var_init: float
        :param random_columns: Random columns indices for HGLM.
               Defaults to ``None``.
        :type random_columns: List[str], optional
        :param method: We only implemented EM as a method to obtain the fixed, random coefficients and the various
               variances.
               Defaults to ``"em"``.
        :type method: Literal["em"]
        :param em_epsilon: Converge if beta/ubeta/tmat/tauEVar changes less (using L-infinity norm) than em esilon. ONLY
               applies to EM method.
               Defaults to ``0.001``.
        :type em_epsilon: float
        :param random_intercept: If true, will allow random component to the GLM coefficients.
               Defaults to ``True``.
        :type random_intercept: bool
        :param group_column: Group column is the column that is categorical and used to generate the groups in HGLM
               Defaults to ``None``.
        :type group_column: str, optional
        :param gen_syn_data: If true, add gaussian noise with variance specified in parms._tau_e_var_init.
               Defaults to ``False``.
        :type gen_syn_data: bool
        """
        super(H2OHGLMEstimator, self).__init__()
        self._parms = {}
        self._id = self._parms['model_id'] = model_id
        self.training_frame = training_frame
        self.validation_frame = validation_frame
        self.response_column = response_column
        self.ignored_columns = ignored_columns
        self.ignore_const_cols = ignore_const_cols
        self.offset_column = offset_column
        self.weights_column = weights_column
        self.max_runtime_secs = max_runtime_secs
        self.custom_metric_func = custom_metric_func
        self.score_each_iteration = score_each_iteration
        self.score_iteration_interval = score_iteration_interval
        self.seed = seed
        self.missing_values_handling = missing_values_handling
        self.plug_values = plug_values
        self.family = family
        self.rand_family = rand_family
        self.max_iterations = max_iterations
        self.initial_fixed_effects = initial_fixed_effects
        self.initial_random_effects = initial_random_effects
        self.initial_t_matrix = initial_t_matrix
        self.tau_u_var_init = tau_u_var_init
        self.tau_e_var_init = tau_e_var_init
        self.random_columns = random_columns
        self.method = method
        self.em_epsilon = em_epsilon
        self.random_intercept = random_intercept
        self.group_column = group_column
        self.gen_syn_data = gen_syn_data

    @property
    def training_frame(self):
        """
        Id of the training data frame.

        Type: ``Union[None, str, H2OFrame]``.
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

        Type: ``bool``, defaults to ``True``.
        """
        return self._parms.get("ignore_const_cols")

    @ignore_const_cols.setter
    def ignore_const_cols(self, ignore_const_cols):
        assert_is_type(ignore_const_cols, None, bool)
        self._parms["ignore_const_cols"] = ignore_const_cols

    @property
    def offset_column(self):
        """
        Offset column. This will be added to the combination of columns before applying the link function.

        Type: ``str``.
        """
        return self._parms.get("offset_column")

    @offset_column.setter
    def offset_column(self, offset_column):
        assert_is_type(offset_column, None, str)
        self._parms["offset_column"] = offset_column

    @property
    def weights_column(self):
        """
        Column with observation weights. Giving some observation a weight of zero is equivalent to excluding it from the
        dataset; giving an observation a relative weight of 2 is equivalent to repeating that row twice. Negative
        weights are not allowed. Note: Weights are per-row observation weights and do not increase the size of the data
        frame. This is typically the number of times a row is repeated, but non-integer values are supported as well.
        During training, rows with higher weights matter more, due to the larger loss function pre-factor. If you set
        weight = 0 for a row, the returned prediction frame at that row is zero and this is incorrect. To get an
        accurate prediction, remove all rows with weight == 0.

        Type: ``str``.
        """
        return self._parms.get("weights_column")

    @weights_column.setter
    def weights_column(self, weights_column):
        assert_is_type(weights_column, None, str)
        self._parms["weights_column"] = weights_column

    @property
    def max_runtime_secs(self):
        """
        Maximum allowed runtime in seconds for model training. Use 0 to disable.

        Type: ``float``, defaults to ``0.0``.
        """
        return self._parms.get("max_runtime_secs")

    @max_runtime_secs.setter
    def max_runtime_secs(self, max_runtime_secs):
        assert_is_type(max_runtime_secs, None, numeric)
        self._parms["max_runtime_secs"] = max_runtime_secs

    @property
    def custom_metric_func(self):
        """
        Reference to custom evaluation function, format: `language:keyName=funcName`

        Type: ``str``.
        """
        return self._parms.get("custom_metric_func")

    @custom_metric_func.setter
    def custom_metric_func(self, custom_metric_func):
        assert_is_type(custom_metric_func, None, str)
        self._parms["custom_metric_func"] = custom_metric_func

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
    def score_iteration_interval(self):
        """
        Perform scoring for every score_iteration_interval iterations.

        Type: ``int``, defaults to ``5``.
        """
        return self._parms.get("score_iteration_interval")

    @score_iteration_interval.setter
    def score_iteration_interval(self, score_iteration_interval):
        assert_is_type(score_iteration_interval, None, int)
        self._parms["score_iteration_interval"] = score_iteration_interval

    @property
    def seed(self):
        """
        Seed for pseudo random number generator (if applicable).

        Type: ``int``, defaults to ``-1``.
        """
        return self._parms.get("seed")

    @seed.setter
    def seed(self, seed):
        assert_is_type(seed, None, int)
        self._parms["seed"] = seed

    @property
    def missing_values_handling(self):
        """
        Handling of missing values. Either MeanImputation, Skip or PlugValues.

        Type: ``Literal["mean_imputation", "skip", "plug_values"]``, defaults to ``"mean_imputation"``.
        """
        return self._parms.get("missing_values_handling")

    @missing_values_handling.setter
    def missing_values_handling(self, missing_values_handling):
        assert_is_type(missing_values_handling, None, Enum("mean_imputation", "skip", "plug_values"))
        self._parms["missing_values_handling"] = missing_values_handling

    @property
    def plug_values(self):
        """
        Plug Values (a single row frame containing values that will be used to impute missing values of the
        training/validation frame, use with conjunction missing_values_handling = PlugValues).

        Type: ``Union[None, str, H2OFrame]``.
        """
        return self._parms.get("plug_values")

    @plug_values.setter
    def plug_values(self, plug_values):
        self._parms["plug_values"] = H2OFrame._validate(plug_values, 'plug_values')

    @property
    def family(self):
        """
        Family. Only gaussian is supported now.

        Type: ``Literal["gaussian"]``, defaults to ``"gaussian"``.
        """
        return self._parms.get("family")

    @family.setter
    def family(self, family):
        assert_is_type(family, None, Enum("gaussian"))
        self._parms["family"] = family

    @property
    def rand_family(self):
        """
        Set distribution of random effects.  Only Gaussian is implemented now.

        Type: ``Literal["gaussian"]``.
        """
        return self._parms.get("rand_family")

    @rand_family.setter
    def rand_family(self, rand_family):
        assert_is_type(rand_family, None, Enum("gaussian"))
        self._parms["rand_family"] = rand_family

    @property
    def max_iterations(self):
        """
        Maximum number of iterations.  Value should >=1.  A value of 0 is only set when only the model coefficient names
        and model coefficient dimensions are needed.

        Type: ``int``, defaults to ``-1``.
        """
        return self._parms.get("max_iterations")

    @max_iterations.setter
    def max_iterations(self, max_iterations):
        assert_is_type(max_iterations, None, int)
        self._parms["max_iterations"] = max_iterations

    @property
    def initial_fixed_effects(self):
        """
        An array that contains initial values of the fixed effects coefficient.

        Type: ``List[float]``.
        """
        return self._parms.get("initial_fixed_effects")

    @initial_fixed_effects.setter
    def initial_fixed_effects(self, initial_fixed_effects):
        assert_is_type(initial_fixed_effects, None, [numeric])
        self._parms["initial_fixed_effects"] = initial_fixed_effects

    @property
    def initial_random_effects(self):
        """
        A H2OFrame id that contains initial values of the random effects coefficient.  The row names shouldbe the random
        coefficient names.  If you are not sure what the random coefficient names are, build HGLM model with
        max_iterations = 0 and checkout the model output field random_coefficient_names.  The number of rows of this
        frame should be the number of level 2 units.  Again, to figure this out, build HGLM model with max_iterations=0
        and check out the model output field group_column_names.  The number of rows should equal the length of
        thegroup_column_names.

        Type: ``Union[None, str, H2OFrame]``.
        """
        return self._parms.get("initial_random_effects")

    @initial_random_effects.setter
    def initial_random_effects(self, initial_random_effects):
        self._parms["initial_random_effects"] = H2OFrame._validate(initial_random_effects, 'initial_random_effects')

    @property
    def initial_t_matrix(self):
        """
        A H2OFrame id that contains initial values of the T matrix.  It should be a positive symmetric matrix.

        Type: ``Union[None, str, H2OFrame]``.
        """
        return self._parms.get("initial_t_matrix")

    @initial_t_matrix.setter
    def initial_t_matrix(self, initial_t_matrix):
        self._parms["initial_t_matrix"] = H2OFrame._validate(initial_t_matrix, 'initial_t_matrix')

    @property
    def tau_u_var_init(self):
        """
        Initial variance of random coefficient effects.  If set, should provide a value > 0.0.  If not set, will be
        randomly set in the model building process.

        Type: ``float``, defaults to ``0.0``.
        """
        return self._parms.get("tau_u_var_init")

    @tau_u_var_init.setter
    def tau_u_var_init(self, tau_u_var_init):
        assert_is_type(tau_u_var_init, None, numeric)
        self._parms["tau_u_var_init"] = tau_u_var_init

    @property
    def tau_e_var_init(self):
        """
        Initial variance of random noise.  If set, should provide a value > 0.0.  If not set, will be randomly set in
        the model building process.

        Type: ``float``, defaults to ``0.0``.
        """
        return self._parms.get("tau_e_var_init")

    @tau_e_var_init.setter
    def tau_e_var_init(self, tau_e_var_init):
        assert_is_type(tau_e_var_init, None, numeric)
        self._parms["tau_e_var_init"] = tau_e_var_init

    @property
    def random_columns(self):
        """
        Random columns indices for HGLM.

        Type: ``List[str]``.

        :examples:

        >>> import h2o
        >>> from h2o.estimators import H2OHGLMEstimator
        >>> h2o.init()
        >>> prostate_path <- system.file("extdata", "prostate.csv", package = "h2o")
        >>> prostate <- h2o.uploadFile(path = prostate_path)
        >>> prostate$CAPSULE <- as.factor(prostate$CAPSULE)
        >>> hglm_model =H2OHGLMEstimator(random_columns = ["AGE"], group_column = "RACE")
        >>> hglm_model.train(x=c("AGE","RACE","DPROS"), y="CAPSULE", training_frame=prostate)
        """
        return self._parms.get("random_columns")

    @random_columns.setter
    def random_columns(self, random_columns):
        assert_is_type(random_columns, None, [str])
        self._parms["random_columns"] = random_columns

    @property
    def method(self):
        """
        We only implemented EM as a method to obtain the fixed, random coefficients and the various variances.

        Type: ``Literal["em"]``, defaults to ``"em"``.
        """
        return self._parms.get("method")

    @method.setter
    def method(self, method):
        assert_is_type(method, None, Enum("em"))
        self._parms["method"] = method

    @property
    def em_epsilon(self):
        """
        Converge if beta/ubeta/tmat/tauEVar changes less (using L-infinity norm) than em esilon. ONLY applies to EM
        method.

        Type: ``float``, defaults to ``0.001``.
        """
        return self._parms.get("em_epsilon")

    @em_epsilon.setter
    def em_epsilon(self, em_epsilon):
        assert_is_type(em_epsilon, None, numeric)
        self._parms["em_epsilon"] = em_epsilon

    @property
    def random_intercept(self):
        """
        If true, will allow random component to the GLM coefficients.

        Type: ``bool``, defaults to ``True``.
        """
        return self._parms.get("random_intercept")

    @random_intercept.setter
    def random_intercept(self, random_intercept):
        assert_is_type(random_intercept, None, bool)
        self._parms["random_intercept"] = random_intercept

    @property
    def group_column(self):
        """
        Group column is the column that is categorical and used to generate the groups in HGLM

        Type: ``str``.
        """
        return self._parms.get("group_column")

    @group_column.setter
    def group_column(self, group_column):
        assert_is_type(group_column, None, str)
        self._parms["group_column"] = group_column

    @property
    def gen_syn_data(self):
        """
        If true, add gaussian noise with variance specified in parms._tau_e_var_init.

        Type: ``bool``, defaults to ``False``.
        """
        return self._parms.get("gen_syn_data")

    @gen_syn_data.setter
    def gen_syn_data(self, gen_syn_data):
        assert_is_type(gen_syn_data, None, bool)
        self._parms["gen_syn_data"] = gen_syn_data


    def level_2_names(self):
        """
        Get the level 2 column values.
        """
        return self._model_json["output"]["group_column_names"]

    def coefs_random_names(self):
        """
        Get the random effect coefficient names including the intercept if applicable.
        """
        return self._model_json["output"]["random_coefficient_names"]

    def coefs_random(self):
        """
        Get the random coefficients of the model.
        """
        level_2_names = self.level_2_names()
        random_coefs = self._model_json["output"]["ubeta"]
        return dict(zip(level_2_names, random_coefs))

    def scoring_history_valid(self, as_data_frame=True):
        """
        Retrieve Model Score History for validation data frame if present

        :returns: The validation score history as an H2OTwoDimTable or a Pandas DataFrame.
        """
        model = self._model_json["output"]
        if "scoring_history_valid" in model and model["scoring_history_valid"] is not None:
            if as_data_frame:
                return model["scoring_history_valid"].as_data_frame()
            else:
                return model["scoring_history_valid"]
        print("No validation scoring history for this model")

    def matrix_T(self):
        """
        retrieve the T matrix estimated for the random effects. The T matrix is the Tj matrix described in 
        section II.I of the doc.

        :return: The T matrix as a tuple of tuples.
        """
        model = self._model_json["output"]
        return model["tmat"]

    def residual_variance(self):
        """
        retrieve the residual variance estimate from the model building process.

        :return: residual variance estiamte as a double
        """
        model = self._model_json["output"]
        return model["residual_variance"]

    def icc(self):
        """
        retrieve the icc from the model building process.

        :return: icc as an array
        """
        model = self._model_json["output"]
        return model["icc"]

    def mean_residual_fixed(self, train = True):
        """
        retrieve the mean residual error using the fixed effect coefficients only.

        :param train: boolean, if true return result from training frame, else return result from validation frame.
        :return: mean residual error as a double.
        """
        model = self._model_json["output"]
        if train:
            return model["mean_residual_fixed"]
        else:
            return model["mean_residual_fixed_valid"]
