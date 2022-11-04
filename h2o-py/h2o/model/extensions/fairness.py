import numpy as np
from collections import defaultdict
from itertools import product


class Fairness:

    def fairness_metrics(self, frame, protected_columns, reference, favorable_class):
        """
        Calculate intersectional fairness metrics.

        :param frame: Frame used to calculate the metrics.
        :param protected_columns: List of categorical columns that contain sensitive information
                                  such as race, gender, age etc.
        :param reference: List of values corresponding to a reference for each protected columns.
                          If set to None, it will use the biggest group as the reference.
        :param favorable_class: Positive/favorable outcome class of the response.

        :return: Dictionary of frames. One frame is the overview, other frames contain dependence
                 of performance on threshold for each protected group.
        """
        import h2o
        from h2o.utils.typechecks import assert_is_type
        from h2o.expr import ExprNode
        assert_is_type(frame, h2o.H2OFrame)
        assert_is_type(protected_columns, [str])
        assert_is_type(reference, [str], None)
        assert_is_type(favorable_class, str)

        expr = ExprNode(
            "fairnessMetrics",
            self,
            frame,
            protected_columns,
            reference,
            favorable_class)
        res = expr._eager_map_frame()

        def _get_tracked_frame(frame_id):
            expr = ExprNode()
            expr._cache._id = frame_id
            return h2o.H2OFrame._expr(expr)

        return {n: _get_tracked_frame(f["key"]["name"]) for n, f in zip(res.map_keys["string"], res.frames)}

    def pd_fair_plot(self, frame, column, protected_columns, figsize=(16, 9), autoscale=True):
        """
        Partial dependence plot per protected group.

        :param model: H2O Model Object
        :param frame: H2OFrame
        :param column: String containing column name.
        :param protected_columns: List of categorical columns that contain sensitive information
                                      such as race, gender, age etc.
        :param figsize: Tuple with figure size; passed directly to matplotlib.
        :param autoscale: If ``True``, try to guess when to use log transformation on X axis.
        :return: Matplotlib Figure object
        """
        import h2o
        from h2o.explanation._explain import no_progress_block
        from h2o.plot import get_matplotlib_pyplot
        from h2o.utils.typechecks import assert_is_type, is_type

        assert_is_type(frame, h2o.H2OFrame)
        assert_is_type(column, str)
        assert_is_type(protected_columns, [str])
        assert_is_type(figsize, tuple, list)
        assert_is_type(autoscale, bool)

        plt = get_matplotlib_pyplot(False, raise_if_not_available=True)
        pgs = product(*[frame[col].unique()["C1"].as_data_frame(False, False) for col in protected_columns])
        plt.figure(figsize=figsize)
        results = []
        maxes = []
        with no_progress_block():
            for pg in pgs:
                pg = [p[0] for p in pg]
                filtered_hdf = frame
                for i in range(len(protected_columns)):
                    filtered_hdf = filtered_hdf[filtered_hdf[protected_columns[i]] == pg[i], :]
                if filtered_hdf.nrow == 0: continue
                pd = self.partial_plot(filtered_hdf, cols=[column], plot=False, nbins=40)[0]
                results.append((pg, pd))
                if is_type(pd[column.lower()][0], str):
                    maxes.append(1)
                else:
                    maxes.append(np.nanmax(pd[column.lower()]))
        maxes = np.array(maxes) - np.min(maxes) + 1
        is_factor = frame[column].isfactor()[0]
        autoscale = autoscale and not is_factor and frame[column].min() > -1 and (
                np.nanmax(np.log(maxes)) - np.nanmin(np.log(maxes)) > 1).all()
        for pg, pd in results:
            x = pd[column.lower()]
            if autoscale:
                x = np.log1p(x)
            mean_response = pd["mean_response"]
            stdev_response = pd["std_error_mean_response"]
            if is_factor:
                plt.errorbar(x, mean_response, yerr=stdev_response, label=", ".join(pg), fmt='o', elinewidth=3,
                             capsize=0, markersize=10)
            else:
                plt.plot(x, mean_response, label=", ".join(pg))
                plt.fill_between(x, [m[0] - m[1] for m in zip(mean_response, stdev_response)],
                                 [m[0] + m[1] for m in zip(mean_response, stdev_response)], label="_noLabel", alpha=0.2)
        plt.title("PDP for {}".format(column))
        plt.xlabel("log({})".format(column) if autoscale else column)
        plt.ylabel("Response")
        plt.legend()
        plt.grid()
        return plt.gcf()

    def fair_roc_plot(self, frame, protected_columns, reference, favorable_class, figsize=(16, 9)):
        """
        Plot ROC curve per protected group.

        :param model: H2O Model Object
        :param frame: H2OFrame
        :param protected_columns: List of categorical columns that contain sensitive information
                                  such as race, gender, age etc.
        :param reference: List of values corresponding to a reference for each protected columns.
                          If set to ``None``, it will use the biggest group as the reference.
        :param favorable_class: Positive/favorable outcome class of the response.
        :param figsize: Figure size; passed directly to Matplotlib

        :return: Matplotlib Figure object
        """
        import h2o
        from h2o.explanation._explain import NumpyFrame
        from h2o.plot import get_matplotlib_pyplot
        from h2o.utils.typechecks import assert_is_type

        assert_is_type(frame, h2o.H2OFrame)
        assert_is_type(protected_columns, [str])
        assert_is_type(reference, [str])
        assert_is_type(favorable_class, str)
        assert_is_type(figsize, tuple, list)

        plt = get_matplotlib_pyplot(False, raise_if_not_available=True)
        fair = self.fairness_metrics(frame=frame, protected_columns=protected_columns, reference=reference,
                                     favorable_class=favorable_class)
        roc_prefix = "thresholds_and_metrics_"
        rocs = [k for k in fair.keys() if k.startswith(roc_prefix)]
        plt.figure(figsize=figsize)
        for roc in rocs:
            df = NumpyFrame(fair[roc])
            plt.plot(df["fpr"], df["tpr"], label=roc[len(roc_prefix):])
        plt.plot([0, 1], [0, 1], c="gray", linestyle="dashed")
        plt.grid()
        plt.legend()
        plt.xlabel("False Positive Rate")
        plt.ylabel("True Positive Rate")
        plt.title("Receiver Operating Characteristic Curve")
        return plt.gcf()

    def fair_pr_plot(self, frame, protected_columns, reference, favorable_class, figsize=(16, 9)):
        """
        Plot PR curve per protected group.
        :param frame: H2OFrame
        :param protected_columns: List of categorical columns that contain sensitive information
                                  such as race, gender, age etc.
        :param reference: List of values corresponding to a reference for each protected columns.
                          If set to ``None``, it will use the biggest group as the reference.
        :param favorable_class: Positive/favorable outcome class of the response.
        :param figsize: Figure size; passed directly to Matplotlib

        :return: Matplotlib Figure object
        """
        import h2o
        from h2o.utils.typechecks import assert_is_type

        from h2o.explanation._explain import NumpyFrame
        from h2o.plot import get_matplotlib_pyplot

        assert_is_type(frame, h2o.H2OFrame)
        assert_is_type(protected_columns, [str])
        assert_is_type(reference, [str])
        assert_is_type(favorable_class, str)
        assert_is_type(figsize, tuple, list)

        plt = get_matplotlib_pyplot(False, raise_if_not_available=True)
        fair = self.fairness_metrics(frame=frame, protected_columns=protected_columns, reference=reference,
                                     favorable_class=favorable_class)
        roc_prefix = "thresholds_and_metrics_"
        rocs = [k for k in fair.keys() if k.startswith(roc_prefix)]
        plt.figure(figsize=figsize)
        for roc in rocs:
            df = NumpyFrame(fair[roc])
            plt.plot(df["recall"], df["precision"], label=roc[len(roc_prefix):])
        mean = frame[self.actual_params["response_column"]].mean()
        if isinstance(mean, list):
            mean = mean[0]
        else:
            mean = float(mean.as_data_frame(False, False)[0][0])
        plt.axhline(y=mean, c="gray", linestyle="dashed")
        plt.grid()
        plt.legend()
        plt.xlabel("Recall")
        plt.ylabel("Precision")
        plt.title("Precision-Recall Curve")
        return plt.gcf()

    def shap_fair_plot(model, frame, column, protected_columns, autoscale=True, figsize=(16, 9), jitter=0.35, alpha=1):
        """
        SHAP summary plot for one feature with protected groups on y-axis.

        :param model: H2O Model Object
        :param frame: H2OFrame
        :param column: String containing column name.
        :param protected_columns: List of categorical columns that contain sensitive information
                                  such as race, gender, age etc.
        :param category: Used to specify what category to inspect when categorical feature is one hot encoded, typically in XGBoost.
        :param autoscale: If ``True``, try to guess when to use log transformation on X axis.
        :param figsize: Tuple with figure size; passed directly to matplotlib.
        :param jitter: Amount of jitter used to show the point density.
        :param alpha: Transparency of the points.
        :return: Matplotlib Figure object
        """
        import h2o
        from h2o.explanation._explain import no_progress_block
        from h2o.explanation import H2OExplanation
        from h2o.explanation._explain import NumpyFrame
        from h2o.explanation._explain import _density
        from h2o.model.model_base import ModelBase
        from h2o.utils.typechecks import assert_is_type

        assert_is_type(model, ModelBase)
        assert_is_type(frame, h2o.H2OFrame)
        assert_is_type(column, str)
        assert_is_type(protected_columns, [str])
        assert_is_type(figsize, tuple, list)
        assert_is_type(jitter, float)
        assert_is_type(alpha, float, int)
        assert_is_type(autoscale, bool)

        from h2o.plot import get_matplotlib_pyplot
        plt = get_matplotlib_pyplot(False, raise_if_not_available=True)
        pgs = product(*[frame[col].unique()["C1"].as_data_frame(False, False) for col in protected_columns])
        results = defaultdict(list)
        maxes = []
        contr_columns = [column]
        with no_progress_block():
            for pg in pgs:
                pg = [p[0] for p in pg]
                filtered_hdf = frame
                for i in range(len(protected_columns)):
                    filtered_hdf = filtered_hdf[filtered_hdf[protected_columns[i]] == pg[i], :]
                if filtered_hdf.nrow == 0: continue
                cont = NumpyFrame(model.predict_contributions(filtered_hdf))
                vals = NumpyFrame(filtered_hdf)[column]
                maxes.append(np.nanmax(vals))
                if len(contr_columns) == 1 and all((c not in cont.columns for c in contr_columns)):
                    contr_columns = [c for c in cont.columns if c.startswith("{}.".format(contr_columns[0]))]
                for cc in contr_columns:
                    results[cc].append((pg, cont[cc], vals))
        maxes = np.array(maxes) - np.min(maxes) + 1
        autoscale = autoscale and not frame[column].isfactor()[0] and frame[column].min() > -1 and (
                np.nanmax(np.log(maxes)) - np.nanmin(np.log(maxes)) > 1).all()
        plots = H2OExplanation()
        for contr_column, result in results.items():
            plt.figure(figsize=figsize)
            for i, (pg, contr, vals) in enumerate(result):
                dens = _density(contr)
                plt.scatter(x=contr, y=i + dens * np.random.uniform(-jitter, jitter, size=len(contr)),
                            label=", ".join(pg), alpha=alpha, c=np.log1p(vals) if autoscale else vals)
            plt.axvline(x=0, c="k")
            plt.title("SHAP Contributions for {}".format(contr_column))
            plt.xlabel("Contribution of {}".format(contr_column))
            plt.ylabel("Sensitive Features")
            plt.yticks(range(len(result)), [", ".join(pg) for pg, _, _ in result])
            plt.grid()
            plt.colorbar().set_label("log({})".format(contr_column) if autoscale else contr_column)
            plots[contr_column] = plt.gcf()
        return plots

    def inspect_model_fairness(self, frame, protected_columns, reference, favorable_class,
                               metrics=("auc", "aucpr", "f1", "p.value", "selectedRatio", "total"), figsize=(16, 9),
                               render=True):
        """
         Produce plots and dataframes related to a single model fairness.

        :param frame: H2OFrame
        :param protected_columns: List of categorical columns that contain sensitive information
                                  such as race, gender, age etc.
        :param reference: List of values corresponding to a reference for each protected columns.
                          If set to None, it will use the biggest group as the reference.
        :param favorable_class: Positive/favorable outcome class of the response.
        :param metrics: List of metrics to show.
        :param figsize: Figure size; passed directly to Matplotlib
        :param render: if ``True``, render the model explanations; otherwise model explanations are just returned.
        :return: H2OExplanation object
        """
        import h2o
        from h2o.explanation import H2OExplanation
        from h2o.explanation._explain import NumpyFrame
        from h2o.explanation._explain import _display, _dont_display, Header
        from h2o.model.extensions import has_extension
        from h2o.plot import get_matplotlib_pyplot
        from h2o.utils.typechecks import assert_is_type

        assert_is_type(frame, h2o.H2OFrame)
        assert_is_type(protected_columns, [str])
        assert_is_type(reference, [str])
        assert_is_type(favorable_class, str)
        assert_is_type(metrics, [str], tuple)
        assert_is_type(figsize, tuple, list)
        assert_is_type(render, bool)

        plt = get_matplotlib_pyplot(False, raise_if_not_available=True)
        fair = self.fairness_metrics(frame=frame, protected_columns=protected_columns, reference=reference,
                                      favorable_class=favorable_class)
        cols_to_show = sorted(
            list(set(metrics).union({"AIR_{}".format(m) for m in metrics}).intersection(fair["overview"].columns)))
        overview = fair["overview"]

        if render:
            display = _display
        else:
            display = _dont_display

        result = H2OExplanation()
        result["overview"] = H2OExplanation()
        result["overview"]["header"] = display(Header("Overview"))
        result["overview"]["data"] = display(overview[:, protected_columns + cols_to_show])

        groups = [", ".join(r) for r in overview[:, protected_columns].as_data_frame(False, False)]
        reference_name = ", ".join(reference)
        result["overview"]["plots"] = H2OExplanation()
        overview = NumpyFrame(overview)
        permutation = sorted(range(overview.nrow), key=lambda i: -overview[i, "auc"])

        def _permute(x):
            return [x[i] for i in permutation]

        groups = _permute(groups)
        for col in cols_to_show:
            plt.figure(figsize=figsize)
            plt.title(col)
            if "AIR_" in col:
                plt.bar(groups, _permute([a - 1 for a in overview[col]]), bottom=1)
                plt.axhline(1, c="k")
                plt.axhline(0.8, c="gray", linestyle="dashed")
                plt.axhline(1.25, c="gray", linestyle="dashed")
            elif "p-value" in col:
                plt.bar(groups, _permute(overview[col]))
                plt.axhline(0.05, c="r")
                plt.axhspan(0, 0.05, color="r", alpha=0.1)
            else:
                plt.bar(groups, _permute(overview[col]), color=["C1" if g == reference_name else "C0" for g in groups])
            plt.grid()
            plt.xticks(rotation=45)
            result["overview"]["plots"][col] = display(plt.gcf())

        # ROC
        result["ROC"] = display(
            self.fair_roc_plot(frame, protected_columns, reference, favorable_class, figsize=figsize))

        # PR
        result["PR"] = display(
            self.fair_pr_plot(frame, protected_columns, reference, favorable_class, figsize=figsize))

        # permutation varimp
        perm = self.permutation_importance(frame)
        result["permutation_importance"] = H2OExplanation()
        result["permutation_importance"]["header"] = display(Header("Permutation Variable Importance"))
        result["permutation_importance"]["data"] = display(perm)
        sorted_features = list(perm["Variable"])

        # PDP per group
        result["pdp"] = H2OExplanation()
        result["pdp"]["header"] = display(Header("Partial Dependence Plots"))
        result["pdp"]["plots"] = H2OExplanation()
        for col in sorted_features:
            result["pdp"]["plots"][col] = display(self.pd_fair_plot(frame, col, protected_columns, figsize=figsize))

        # SHAP per group
        if has_extension(self, "Contributions"):
            result["shap"] = H2OExplanation()
            result["shap"]["header"] = display(Header("SHAP per protected group"))
            result["shap"]["plots"] = H2OExplanation()
            for col in sorted_features:
                result["shap"]["plots"][col] = display(
                    self.shap_fair_plot(frame, col, protected_columns, figsize=figsize))

        return result
