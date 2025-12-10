from anonypy import mondrian
import pandas as pd


class Preserver:

    def __init__(self, df, feature_columns, sensitive_column, ignored_columns=None):
        self.modrian = mondrian.Mondrian(df, feature_columns, sensitive_column)
        self.ignored_columns = ignored_columns if ignored_columns is not None else []

    def __anonymize(self, k, l=0, p=0.0):
        partitions = self.modrian.partition(k, l, p)
        return anonymize(
            self.modrian.df,
            partitions,
            self.modrian.feature_columns,
            self.modrian.sensitive_column,
            ignored_columns=self.ignored_columns,
        )

    def anonymize_k_anonymity(self, k):
        return self.__anonymize(k)

    def anonymize_l_diversity(self, k, l):
        return self.__anonymize(k, l=l)

    def anonymize_t_closeness(self, k, p):
        return self.__anonymize(k, p=p)

    def __count_anonymity(self, k, l=0, p=0.0):
        partitions = self.modrian.partition(k, l, p)
        return count_anonymity(
            self.modrian.df,
            partitions,
            self.modrian.feature_columns,
            self.modrian.sensitive_column,
            ignored_columns=self.ignored_columns,
        )

    def count_k_anonymity(self, k):
        return self.__count_anonymity(k)

    def count_l_diversity(self, k, l):
        return self.__count_anonymity(k, l=l)

    def count_t_closeness(self, k, p):
        return self.__count_anonymity(k, p=p)


def agg_categorical_column(series):
    series.astype("category")
    converted = [str(n) for n in set(series)]
    return [",".join(converted)]


def agg_numerical_column(series):
    minimum = series.min()
    maximum = series.max()
    if maximum == minimum:
        string = str(maximum)
    else:
        string = f"{minimum}-{maximum}"
    return [string]


def anonymize(df, partitions, feature_columns, sensitive_column, ignored_columns=None, max_partitions=None):
    ignored_columns = ignored_columns if ignored_columns is not None else []

    aggregations = {}
    for column in feature_columns:
        if column in ignored_columns:
            continue  # ignored columns are not aggregated
        if df[column].dtype.name == "category":
            aggregations[column] = agg_categorical_column
        else:
            aggregations[column] = agg_numerical_column

    rows = []
    for i, partition in enumerate(partitions):
        if max_partitions is not None and i > max_partitions:
            break

        grouped_columns = {
            column: aggregations[column](df.loc[partition, column])
            for column in aggregations
        }

        sensitive_counts = (
            df.loc[partition]
            .groupby(sensitive_column, observed=False)[sensitive_column]
            .count()
            .to_dict()
        )

        for sensitive_value, count in sensitive_counts.items():
            if count == 0:
                continue

            # Collect ignored columns as lists, aligned with sensitive_value
            ignored_data = {
                col: df.loc[partition][df.loc[partition, sensitive_column] == sensitive_value][col].tolist()
                for col in ignored_columns
            }

            # Build the output row
            values = grouped_columns.copy()
            values.update(ignored_data)
            values.update({
                sensitive_column: sensitive_value,
                "count": count,
            })
            rows.append(values)
    return rows


def count_anonymity(df, partitions, feature_columns, sensitive_column, ignored_columns=None, max_partitions=None):
    ignored_columns = ignored_columns if ignored_columns is not None else []

    aggregations = {}
    for column in feature_columns:
        if column in ignored_columns:
            continue
        if df[column].dtype.name == "category":
            aggregations[column] = agg_categorical_column
        else:
            aggregations[column] = agg_numerical_column
    aggregations[sensitive_column] = "count"

    rows = []
    for i, partition in enumerate(partitions):
        if max_partitions is not None and i > max_partitions:
            break
        grouped_columns = df.loc[partition].agg(aggregations, squeeze=False)

        # Include ignored columns as-is
        for column in ignored_columns:
            grouped_columns[column] = [df.loc[partition, column].iloc[0]]

        values = grouped_columns.apply(
            lambda x: x[0] if isinstance(x, list) else x
        ).to_dict()
        rows.append(values.copy())
    return rows
