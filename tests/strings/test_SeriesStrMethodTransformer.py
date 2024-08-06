import re

import numpy as np
import pytest

from tests.base_tests import ColumnStrListInitTests, NewColumnNameInitMixintests
from tubular.strings import SeriesStrMethodTransformer


class TestInit(ColumnStrListInitTests, NewColumnNameInitMixintests):
    """Generic tests for transformer.init()."""

    @classmethod
    def setup_class(cls):
        cls.transformer_name = "SeriesStrMethodTransformer"

    @pytest.mark.parametrize(
        "non_string",
        [1, True, {"a": 1}, [1, 2], None, np.inf, np.nan],
    )
    def test_columns_list_element_error(
        self,
        non_string,
        minimal_attribute_dict,
        uninitialized_transformers,
    ):
        """Test an error is raised if columns list contains non-string elements."""

        args = minimal_attribute_dict[self.transformer_name].copy()
        args["columns"] = [non_string]

        with pytest.raises(
            TypeError,
            match=re.escape(
                f"{self.transformer_name}: each element of columns should be a single (string) column name",
            ),
        ):
            uninitialized_transformers[self.transformer_name](**args)

    def test_list_length(self):
        """Test that an error is raised if columns list contains more than a single element"""

        with pytest.raises(
            ValueError,
            match="SeriesStrMethodTransformer: columns arg should contain only 1 column name but got 2",
        ):
            SeriesStrMethodTransformer(
                new_column_name="a",
                pd_method_name=1,
                columns=["b", "c"],
            )

    def test_exception_raised_non_pandas_method_passed(self):
        """Test and exception is raised if a non pd.Series.str method is passed for pd_method_name."""
        with pytest.raises(
            AttributeError,
            match="""SeriesStrMethodTransformer: error accessing "str.b" method on pd.Series object - pd_method_name should be a pd.Series.str method""",
        ):
            SeriesStrMethodTransformer(
                new_column_name="a",
                pd_method_name="b",
                columns=["b"],
            )

    @pytest.mark.parametrize(
        "non_dict",
        [1, "a", True, [1, 2], np.inf, np.nan],
    )
    def test_invalid_pd_kwargs_type_errors(
        self,
        non_dict,
        minimal_attribute_dict,
        uninitialized_transformers,
    ):
        """Test that an exceptions are raised for invalid pd_kwargs types."""

        args = minimal_attribute_dict[self.transformer_name].copy()
        args["pd_method_kwargs"] = non_dict

        with pytest.raises(
            TypeError,
            match=re.escape(
                f"{self.transformer_name}: pd_method_kwargs should be provided as a dict or defaulted to None",
            ),
        ):
            uninitialized_transformers[self.transformer_name](**args)

    @pytest.mark.parametrize(
        "na_dict_key",
        [{"a": 1, 2: "b"}, {"a": 1, (1, 2): "b"}],
    )
    def test_invalid_pd_kwargs_key_errors(
        self,
        na_dict_key,
        minimal_attribute_dict,
        uninitialized_transformers,
    ):
        """Test that an exceptions are raised for invalid pd_kwargs key types."""

        args = minimal_attribute_dict[self.transformer_name].copy()
        args["pd_method_kwargs"] = na_dict_key

        with pytest.raises(
            TypeError,
            match=re.escape(
                f"{self.transformer_name}: all keys in pd_method_kwargs must be a string value",
            ),
        ):
            uninitialized_transformers[self.transformer_name](**args)


# class TestTransform:
#     """Tests for SeriesStrMethodTransformer.transform()."""

#     def expected_df_1():
#         """Expected output of test_expected_output_no_overwrite."""
#         df = d.create_df_7()

#         df["b_new"] = df["b"].str.find(sub="a")

#         return df

#     def expected_df_2():
#         """Expected output of test_expected_output_overwrite."""
#         df = d.create_df_7()

#         df["b"] = df["b"].str.pad(width=10)

#         return df

#     def test_super_transform_called(self, mocker):
#         """Test that BaseTransformer.transform called."""
#         df = d.create_df_7()

#         x = SeriesStrMethodTransformer(
#             new_column_name="cc",
#             pd_method_name="find",
#             columns=["c"],
#         )

#         expected_call_args = {0: {"args": (d.create_df_7(),), "kwargs": {}}}

#         with ta.functions.assert_function_call(
#             mocker,
#             tubular.base.BaseTransformer,
#             "transform",
#             expected_call_args,
#         ):
#             x.transform(df)

#     @pytest.mark.parametrize(
#         ("df", "expected"),
#         ta.pandas.adjusted_dataframe_params(d.create_df_7(), expected_df_1()),
#     )
#     def test_expected_output_no_overwrite(self, df, expected):
#         """Test a single column output from transform gives expected results, when not overwriting the original column."""
#         x = SeriesStrMethodTransformer(
#             new_column_name="b_new",
#             pd_method_name="find",
#             columns=["b"],
#             pd_method_kwargs={"sub": "a"},
#         )

#         df_transformed = x.transform(df)

#         ta.equality.assert_frame_equal_msg(
#             actual=df_transformed,
#             expected=expected,
#             msg_tag="Unexpected values in SeriesStrMethodTransformer.transform with find, not overwriting original column",
#         )

#     @pytest.mark.parametrize(
#         ("df", "expected"),
#         ta.pandas.adjusted_dataframe_params(d.create_df_7(), expected_df_2()),
#     )
#     def test_expected_output_overwrite(self, df, expected):
#         """Test a single column output from transform gives expected results, when overwriting the original column."""
#         x = SeriesStrMethodTransformer(
#             new_column_name="b",
#             pd_method_name="pad",
#             columns=["b"],
#             pd_method_kwargs={"width": 10},
#         )

#         df_transformed = x.transform(df)

#         ta.equality.assert_frame_equal_msg(
#             actual=df_transformed,
#             expected=expected,
#             msg_tag="Unexpected values in SeriesStrMethodTransformer.transform with pad, overwriting original column",
#         )

#     @pytest.mark.parametrize(
#         ("df", "new_column_name", "pd_method_name", "columns", "pd_method_kwargs"),
#         [
#             (d.create_df_7(), "b_new", "find", ["b"], {"sub": "a"}),
#             (
#                 d.create_df_7(),
#                 "c_slice",
#                 "slice",
#                 ["c"],
#                 {"start": 0, "stop": 1, "step": 1},
#             ),
#             (d.create_df_7(), "b_upper", "upper", ["b"], {}),
#         ],
#     )
#     def test_pandas_method_called(
#         self,
#         mocker,
#         df,
#         new_column_name,
#         pd_method_name,
#         columns,
#         pd_method_kwargs,
#     ):
#         """Test that the pandas.Series.str method is called as expected (with kwargs passed) during transform."""
#         spy = mocker.spy(pd.Series.str, pd_method_name)

#         x = SeriesStrMethodTransformer(
#             new_column_name=new_column_name,
#             pd_method_name=pd_method_name,
#             columns=columns,
#             pd_method_kwargs=pd_method_kwargs,
#         )

#         x.transform(df)

#         # pull out positional and keyword args to target the call
#         call_args = spy.call_args_list[0]
#         call_kwargs = call_args[1]

#         # test keyword are as expected
#         ta.equality.assert_dict_equal_msg(
#             actual=call_kwargs,
#             expected=pd_method_kwargs,
#             msg_tag=f"""Keyword arg assert for {pd_method_name}""",
#         )

#     def test_attributes_unchanged_by_transform(self):
#         """Test that attributes set in init are unchanged by the transform method."""
#         df = d.create_df_7()

#         x = SeriesStrMethodTransformer(
#             new_column_name="b",
#             pd_method_name="pad",
#             columns=["b"],
#             pd_method_kwargs={"width": 10},
#         )

#         x2 = SeriesStrMethodTransformer(
#             new_column_name="b",
#             pd_method_name="pad",
#             columns=["b"],
#             pd_method_kwargs={"width": 10},
#         )

#         x.transform(df)

#         assert (
#             x.new_column_name == x2.new_column_name
#         ), "new_column_name changed by SeriesDtMethodTransformer.transform"
#         assert (
#             x.pd_method_name == x2.pd_method_name
#         ), "pd_method_name changed by SeriesDtMethodTransformer.transform"
#         assert (
#             x.columns == x2.columns
#         ), "columns changed by SeriesDtMethodTransformer.transform"
#         assert (
#             x.pd_method_kwargs == x2.pd_method_kwargs
#         ), "pd_method_kwargs changed by SeriesDtMethodTransformer.transform"
