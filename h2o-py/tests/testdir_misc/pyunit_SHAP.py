import sys

sys.path.insert(1, "../../")
from tests import pyunit_utils

import random
import h2o
import numpy as np
import pandas as pd

from itertools import chain, combinations
from collections import defaultdict

try:
    from tqdm.auto import tqdm
except ImportError:

    def tqdm(x, *args, **kwargs):
        return x


from h2o.estimators import *
from h2o.explanation._explain import no_progress_block


seed = 6
K = 5
LARGE_K = 1 * K


def prob_to_logit(p):
    return np.log(p / (1 - p))


def logit_to_prob(l):
    return np.exp(l) / (1 + np.exp(l))


def sample(x, k=K):
    x = list(x)
    if len(x) < k:
        return x
    return random.sample(x, k)


def remove_all_but(*args):
    keep = {x.key if hasattr(x, "key") else x.frame_id for x in args}
    h2o.remove([key for key in h2o.ls().iloc[:, 0].values if key not in keep])


def test_local_accuracy(
    mod, train, test, link=False, eps=1e-5, output_format="original"
):
    with no_progress_block():
        cf = mod.predict_contributions(
            test, background_frame=train, output_format=output_format
        )
        pf = mod.predict(test)
        col = "Yes" if "Yes" in pf.names else "predict"
        p = pf[col].as_data_frame()[col]
        h2o.remove(pf)
        fr = cf.drop("BackgroundRowIdx").group_by("RowIdx").mean().get_frame()
        tmp = fr.drop("RowIdx").sum(axis=1, return_frame=True)
        mu = tmp.as_data_frame().iloc[:, 0]
        h2o.remove(cf)
        h2o.remove(fr)
        h2o.remove(tmp)
        if link:
            mu = logit_to_prob(mu)

    assert (
        np.abs(p - mu) < eps
    ).any(), f"Failed local accuracy test: {mod.key} on {test.frame_id}. max diff = {np.max(np.abs(p-mu))}, mean diff = {np.mean(np.abs(p-mu))}"


def test_dummy_property(mod, train, test, output_format):
    contr_h2o = (
        mod.predict_contributions(
            test, background_frame=train, output_format=output_format
        )
        .sort(["RowIdx", "BackgroundRowIdx"])
        .drop(["BiasTerm", "RowIdx", "BackgroundRowIdx"])
    )

    contr_df = contr_h2o.as_data_frame()
    h2o.remove(contr_h2o)

    train_df = train.as_data_frame()
    test_df = test.as_data_frame()
    for ts in tqdm(sample(range(test_df.shape[0]), LARGE_K), desc="Test"):
        for tr in sample(range(train_df.shape[0]), LARGE_K):
            for col in contr_df.columns:
                row_in_contr = ts * train.shape[0] + tr
                if col not in train_df.columns:
                    fragments = col.split(".")
                    col_name, cat = [
                        (".".join(fragments[:i]), ".".join(fragments[i:]))
                        for i in range(1, len(fragments))
                        if ".".join(fragments[:i]) in train.columns
                    ][0]

                    if contr_df.loc[row_in_contr, col] != 0:
                        if test_df.loc[ts, col_name] == train_df.loc[tr, col_name] or (
                            pd.isna(test_df.loc[ts, col_name])
                            and pd.isna(train_df.loc[tr, col_name])
                        ):
                            print(
                                f"test={test_df.loc[ts, col_name]} != train={train_df.loc[tr, col_name]}: contr={contr_df.loc[row_in_contr, col]}| ts={ts}, tr={tr}"
                            )
                            assert False
                        # not train_df.loc[tr, col_name] != cat and \
                        if test_df.loc[ts, col_name] != cat and not (
                            cat == "missing(NA)"
                            and (
                                pd.isna(
                                    test_df.loc[ts, col_name]
                                    or pd.isna(train_df.loc[tr, col_name])
                                )
                            )
                        ):
                            print(
                                f"Category not used but contributes! col={col_name}; test={test_df.loc[ts, col_name]} != cat={cat}; train={train_df.loc[tr, col_name]}: contr={contr_df.loc[row_in_contr, col]}| ts={ts}, tr={tr} | {cat == 'missing(NA)'} and {pd.isna(test_df.loc[ts, col_name])}"
                            )
                            assert False
                else:
                    if contr_df.loc[row_in_contr, col] != 0:
                        if test_df.loc[ts, col] == train_df.loc[tr, col]:
                            print(
                                f"test={test_df.loc[ts, col]} != train={train_df.loc[tr, col]}: contr={contr_df.loc[row_in_contr, col]}| ts={ts}, tr={tr}"
                            )
                            assert False


def test_symmetry(mod, train, test, output_format, eps=1e-10):
    """This test does not test the symmetry axiom from shap. It tests whether contributions are same magnitude
    but opposite sign if we switch the background with the foreground."""
    contr = (
        mod.predict_contributions(
            test, background_frame=train, output_format=output_format
        )
        .sort(["RowIdx", "BackgroundRowIdx"])
        .drop(["BiasTerm", "RowIdx", "BackgroundRowIdx"])
        .as_data_frame()
    )
    contr2 = (
        mod.predict_contributions(
            train, background_frame=test, output_format=output_format
        )
        .sort(["RowIdx", "BackgroundRowIdx"][::-1])
        .drop(["BiasTerm", "RowIdx", "BackgroundRowIdx"])
        .as_data_frame()
    )

    test = test.as_data_frame()
    train = train.as_data_frame()

    for row in tqdm(sample(range(contr.shape[0]), LARGE_K), desc="Row"):
        for col in sample(contr.columns, LARGE_K):
            if col not in train.columns:
                fragments = col.split(".")
                col_name, cat = [
                    (".".join(fragments[:i]), ".".join(fragments[i:]))
                    for i in range(1, len(fragments))
                    if ".".join(fragments[:i]) in train.columns
                ][0]

                val = test.loc[row // train.shape[0], col_name]
                if val == "NA" or pd.isna(val):
                    val = "missing(NA)"
                if abs(contr.loc[row, col]) > 0:
                    assert val == cat
                val_bg = train.loc[row % train.shape[0], col_name]
                if val_bg == "NA" or pd.isna(val_bg):
                    val_bg = "missing(NA)"
                if (
                    abs(
                        contr.loc[row, f"{col_name}.{val}"]
                        + contr2.loc[row, f"{col_name}.{val_bg}"]
                    )
                    > eps
                ):
                    print(
                        f"row: {row}, col: {col}, col2: {col_name}.{val_bg}, {contr.loc[row, col]} != - {contr2.loc[row, col]}"
                    )
                    assert False
            else:
                if abs(contr.loc[row, col] + contr2.loc[row, col]) > eps:
                    print(
                        f"row: {row}, col: {col}, {contr.loc[row, col]} != - {contr2.loc[row, col]}"
                    )
                    assert False


def powerset(iterable):
    s = list(iterable)
    return list(chain.from_iterable(combinations(s, r) for r in range(len(s) + 1)))


def fact(n):
    if n < 1:
        return 1
    return n * fact(n - 1)


def naiveBSHAP(mod, train, test, xrow, brow):
    x = test[xrow, :].as_data_frame()
    b = train[brow, :].as_data_frame()

    cols = [
        col
        for col in x.columns.values[(x != b).values[0]]
        if col in mod._model_json["output"]["names"]
        and not (pd.isna(x.loc[0, col]) and pd.isna(b.loc[0, col]))
        and col != y
    ]
    # print(cols, len(cols))
    # display(x.loc[:, cols])
    # display(b.loc[:, cols])
    pset = powerset(cols)

    df = pd.concat([b for _ in range(len(pset))], ignore_index=True)
    for row in tqdm(range(df.shape[0]), desc="Creating data frame", leave=False):
        for col in pset[row]:
            df.loc[row, col] = x[col].values

    df = h2o.H2OFrame(df, column_types=train.types)

    # for row in tqdm(range(pdf.shape[0]), desc="Setting NAs to h2oframe", leave=False):
    #     for col in pdf.columns[pdf.iloc[row].isna()]:
    #         if pd.isna(pdf.loc[row, col]) and train.types[col] == "enum":
    #             df[row, col] = None

    for i, cat in enumerate(train.isfactor()):
        if cat:
            df[df.columns[i]] = df[df.columns[i]].asfactor()

    results = defaultdict(lambda: 0)
    preds = mod.predict(df)
    resp = "Yes" if "Yes" in preds.names else "predict"
    evals = list(zip(pset, preds[resp].as_data_frame()[resp]))
    for c in tqdm(cols, desc="Calculating B-SHAP", leave=False):
        F = len(cols)
        for ec, ev in evals:
            if c in ec:
                S = len(ec) - 1
                coef = fact(S) * fact(F - S - 1) / fact(F)
                results[c] += ev * coef
            if c not in ec:
                S = len(ec)
                coef = fact(S) * fact(F - S - 1) / fact(F)
                results[c] -= ev * coef
    return results


def test_contributions_against_naive(mod, train, test, link=False, eps=1e-6):
    # In this test, I'm generating the data in python and then at once converting to h2o frame. This speeds it by several magnitudes
    # but it also creates nasty bugs when NAs are involved, e.g., category level "3" gets converted to float and hence is a new level "3.0"
    # that's why I remove NAs here
    train = train.na_omit()
    test = test.na_omit()
    for xrow in tqdm(sample(range(test.nrow), k=LARGE_K), desc="X row"):
        if any([test[xrow, k] == "NA" for k, v in train.types.items() if v == "enum"]):
            continue  # Converting NA from pandas to h2oFrame gets very messy
        for brow in tqdm(sample(range(train.nrow), k=K), leave=False, desc="B row"):
            if any(
                [train[brow, k] == "NA" for k, v in train.types.items() if v == "enum"]
            ):
                continue
            with no_progress_block():
                naive_contr = naiveBSHAP(mod, train, test, xrow, brow)
                contr = mod.predict_contributions(
                    test[xrow, :],
                    background_frame=train[brow, :],
                    output_format="compact",
                ).as_data_frame()
                contr = contr.loc[:, (contr != 0).values[0]]
                cols = set(contr.columns)
                cols = cols.union(set(naive_contr.keys()))
                if "BiasTerm" in cols:
                    cols.remove("BiasTerm")
                if link:
                    naive_contr_df = pd.DataFrame(
                        {k: v for k, v in naive_contr.items() if abs(v) > 1e-15},
                        index=[0],
                    ).rank(axis=1)
                    contr_df = contr.drop("BiasTerm", axis=1).rank(axis=1)
                    for col in cols:
                        if col not in contr.columns:
                            assert (
                                abs(naive_contr[col]) < eps
                            ), f"{col} present in naive contr but not in contr with value {naive_contr[col]}, xrow={xrow}, brow={brow}"
                        else:
                            assert (
                                abs(naive_contr_df[col] - contr_df.loc[0, col]) < eps
                            ).all(), f"{col} contribution ranks differ: contr={contr_df.loc[0, col]}, naive_contr={naive_contr_df[col]}, diff={naive_contr_df[col] - contr_df.loc[0,col]}, xrow={xrow}, brow={brow}"

                else:
                    for col in cols:
                        if col not in contr.columns:
                            assert (
                                abs(naive_contr[col]) < eps
                            ), f"{col} present in naive contr but not in contr with value {naive_contr[col]}, xrow={xrow}, brow={brow}"
                        else:
                            assert (
                                abs(naive_contr[col] - contr.loc[0, col]) < eps
                            ), f"{col} contributions differ: contr={contr.loc[0, col]}, naive_contr={naive_contr[col]}, diff={naive_contr[col] - contr.loc[0,col]}, xrow={xrow}, brow={brow}"


def import_data(seed=seed):
    df = h2o.import_file(
        pyunit_utils.locate("smalldata/titanic/titanic_expanded.csv"),
        na_strings=["", " ", "NA"],
    )
    df["survived"] = df["survived"].asfactor()
    return df.split_frame([0.75], seed=seed)


def helper_test_all(Estimator, y, train, test, output_format, link=False, **kwargs):
    mod = Estimator(**kwargs)
    mod.train(y=y, training_frame=train)

    test_local_accuracy(mod, train, test, link=link, output_format=output_format)

    test_dummy_property(mod, train, test, output_format=output_format)

    test_symmetry(mod, train, test, output_format=output_format)

    if output_format.lower() == "compact":
        test_contributions_against_naive(mod, train, test, link=link)


########################################################################################################################
def test_drf_one_tree_binomial_original():
    train, test = import_data()
    helper_test_all(
        H2ORandomForestEstimator, "survived", train, test, "original", ntrees=1
    )


def test_drf_one_tree_binomial_compact():
    train, test = import_data()
    helper_test_all(
        H2ORandomForestEstimator, "survived", train, test, "compact", ntrees=1
    )


def test_drf_one_tree_regression_original():
    train, test = import_data()
    helper_test_all(H2ORandomForestEstimator, "fare", train, test, "original", ntrees=1)


def test_drf_one_tree_regression_compact():
    train, test = import_data()
    helper_test_all(H2ORandomForestEstimator, "fare", train, test, "compact", ntrees=1)


def test_drf_binomial_original():
    train, test = import_data()
    helper_test_all(H2ORandomForestEstimator, "survived", train, test, "original")


def test_drf_binomial_compact():
    train, test = import_data()
    helper_test_all(H2ORandomForestEstimator, "survived", train, test, "compact")


def test_drf_regression_original():
    train, test = import_data()
    helper_test_all(H2ORandomForestEstimator, "fare", train, test, "original")


def test_drf_regression_compact():
    train, test = import_data()
    helper_test_all(H2ORandomForestEstimator, "fare", train, test, "compact")


def test_xrt_one_tree_binomial_original():
    train, test = import_data()
    helper_test_all(
        H2ORandomForestEstimator,
        "survived",
        train,
        test,
        "original",
        ntrees=1,
        histogram_type="random",
    )


def test_xrt_one_tree_binomial_compact():
    train, test = import_data()
    helper_test_all(
        H2ORandomForestEstimator,
        "survived",
        train,
        test,
        "compact",
        ntrees=1,
        histogram_type="random",
    )


def test_xrt_one_tree_regression_original():
    train, test = import_data()
    helper_test_all(
        H2ORandomForestEstimator,
        "fare",
        train,
        test,
        "original",
        ntrees=1,
        histogram_type="random",
    )


def test_xrt_one_tree_regression_compact():
    train, test = import_data()
    helper_test_all(
        H2ORandomForestEstimator,
        "fare",
        train,
        test,
        "compact",
        ntrees=1,
        histogram_type="random",
    )


def test_xrt_binomial_original():
    train, test = import_data()
    helper_test_all(
        H2ORandomForestEstimator,
        "survived",
        train,
        test,
        "original",
        histogram_type="random",
    )


def test_xrt_binomial_compact():
    train, test = import_data()
    helper_test_all(
        H2ORandomForestEstimator,
        "survived",
        train,
        test,
        "compact",
        histogram_type="random",
    )


def test_xrt_regression_original():
    train, test = import_data()
    helper_test_all(
        H2ORandomForestEstimator,
        "fare",
        train,
        test,
        "original",
        histogram_type="random",
    )


def test_xrt_regression_compact():
    train, test = import_data()
    helper_test_all(
        H2ORandomForestEstimator,
        "fare",
        train,
        test,
        "compact",
        histogram_type="random",
    )


def test_gbm_one_tree_binomial_original():
    train, test = import_data()
    helper_test_all(
        H2OGradientBoostingEstimator,
        "survived",
        train,
        test,
        "original",
        link=True,
        ntrees=1,
    )


def test_gbm_one_tree_binomial_compact():
    train, test = import_data()
    helper_test_all(
        H2OGradientBoostingEstimator,
        "survived",
        train,
        test,
        "compact",
        link=True,
        ntrees=1,
    )


def test_gbm_one_tree_regression_original():
    train, test = import_data()
    helper_test_all(
        H2OGradientBoostingEstimator, "fare", train, test, "original", ntrees=1
    )


def test_gbm_one_tree_regression_compact():
    train, test = import_data()
    helper_test_all(
        H2OGradientBoostingEstimator, "fare", train, test, "compact", ntrees=1
    )


def test_gbm_binomial_original():
    train, test = import_data()
    helper_test_all(
        H2OGradientBoostingEstimator, "survived", train, test, "original", link=True
    )


def test_gbm_binomial_compact():
    train, test = import_data()
    helper_test_all(
        H2OGradientBoostingEstimator, "survived", train, test, "compact", link=True
    )


def test_gbm_regression_original():
    train, test = import_data()
    helper_test_all(H2OGradientBoostingEstimator, "fare", train, test, "original")


def test_gbm_regression_compact():
    train, test = import_data()
    helper_test_all(H2OGradientBoostingEstimator, "fare", train, test, "compact")


def test_xgboost_one_tree_binomial_original():
    train, test = import_data()
    helper_test_all(
        H2OXGBoostEstimator, "survived", train, test, "original", link=True, ntrees=1
    )


def test_xgboost_one_tree_binomial_compact():
    train, test = import_data()
    helper_test_all(
        H2OXGBoostEstimator, "survived", train, test, "compact", link=True, ntrees=1
    )


def test_xgboost_one_tree_regression_original():
    train, test = import_data()
    helper_test_all(H2OXGBoostEstimator, "fare", train, test, "original", ntrees=1)


def test_xgboost_one_tree_regression_compact():
    train, test = import_data()
    helper_test_all(H2OXGBoostEstimator, "fare", train, test, "compact", ntrees=1)


def test_xgboost_binomial_original():
    train, test = import_data()
    helper_test_all(H2OXGBoostEstimator, "survived", train, test, "original", link=True)


def test_xgboost_binomial_compact():
    train, test = import_data()
    helper_test_all(H2OXGBoostEstimator, "survived", train, test, "compact", link=True)


def test_xgboost_regression_original():
    train, test = import_data()
    helper_test_all(H2OXGBoostEstimator, "fare", train, test, "original")


def test_xgboost_regression_compact():
    train, test = import_data()
    helper_test_all(H2OXGBoostEstimator, "fare", train, test, "compact")


TESTS = [
    test_drf_one_tree_binomial_original,
    test_drf_one_tree_binomial_compact,
    test_drf_one_tree_regression_original,
    test_drf_one_tree_regression_compact,
    test_drf_binomial_original,
    test_drf_binomial_compact,
    test_drf_regression_original,
    test_drf_regression_compact,
    test_xrt_one_tree_binomial_original,
    test_xrt_one_tree_binomial_compact,
    test_xrt_one_tree_regression_original,
    test_xrt_one_tree_regression_compact,
    test_xrt_binomial_original,
    test_xrt_binomial_compact,
    test_xrt_regression_original,
    test_xrt_regression_compact,
    test_gbm_one_tree_binomial_original,
    test_gbm_one_tree_binomial_compact,
    test_gbm_one_tree_regression_original,
    test_gbm_one_tree_regression_compact,
    test_gbm_binomial_original,
    test_gbm_binomial_compact,
    test_gbm_regression_original,
    test_gbm_regression_compact,
    test_xgboost_one_tree_binomial_original,
    test_xgboost_one_tree_binomial_compact,
    test_xgboost_one_tree_regression_original,
    test_xgboost_one_tree_regression_compact,
    test_xgboost_binomial_original,
    test_xgboost_binomial_compact,
    test_xgboost_regression_original,
    test_xgboost_regression_compact,
]


if __name__ == "__main__":
    pyunit_utils.run_tests(TESTS)
else:
    for t in TESTS:
        t()
