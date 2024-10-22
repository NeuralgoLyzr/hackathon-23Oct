# standart-library imports
import re
import io
import time
import string
import hashlib
from typing import Union, Sequence, Any

# third-party imports
import numpy as np
import pandas as pd


def extract_python_code(llm_response: str) -> str:
    # Extract python code from LLM response
    py_code = re.search(r"```python\n(.*?)```", llm_response, re.DOTALL)
    if py_code:
        return py_code.group(1)
    py_code = re.search(r"```(.*?)```", llm_response, re.DOTALL)
    if py_code:
        return py_code.group(1)
    return llm_response


def clean_python_code(code: str) -> str:
    # Remove print statements and plot showing or saving commands from the code
    codelines = code.split("\n")
    return "\n".join(
        [
            line
            for line in codelines
            if not (
                (line.strip().startswith("print("))
                or (line.strip().startswith("plt.show()"))
                or (line.strip().startswith("plt.savefig("))
                or (line.strip().startswith("fig.savefig("))
            )
        ]
    ).strip()


def clean_analysis_output(
    analysis_output: Any,
) -> Union[str, pd.DataFrame, dict[str, pd.DataFrame], None]:
    # Handle the analysis output to return a string or a DataFrame
    if analysis_output is None:
        return None
    if isinstance(analysis_output, pd.DataFrame):
        return analysis_output
    if isinstance(analysis_output, pd.Series):
        return analysis_output.to_frame()
    if isinstance(analysis_output, (np.number, int, float, str, bool, complex)):
        return str(analysis_output)
    if isinstance(analysis_output, (Sequence, set)):
        return ", ".join([str(i) for i in analysis_output])
    if isinstance(analysis_output, np.ndarray):
        if analysis_output.ndim == 1:
            return ", ".join([str(i) for i in analysis_output])
        return pd.DataFrame(analysis_output)
    if isinstance(analysis_output, dict):
        try:
            return pd.DataFrame(analysis_output)
        except ValueError:
            return handle_dict_output(analysis_output)[0]
    return str(analysis_output)


def handle_dict_output(
    analysis_output: dict,
) -> tuple[dict[str, Union[str, pd.DataFrame]], bool]:
    only_string_values = True
    output = {}
    for key, value in analysis_output.items():
        output_value = clean_analysis_output(value)
        if isinstance(output_value, pd.DataFrame):
            only_string_values = False
        elif isinstance(output_value, dict):
            output_value, output_string_values = handle_dict_output(output_value)
            only_string_values = output_string_values and only_string_values
        else:
            output_value = str(output_value)
        output[str(key)] = output_value
    if only_string_values:
        return (
            ", ".join([f"{k}: {v}" for k, v in analysis_output.items()]),
            only_string_values,
        )
    return output, only_string_values


# ------------------------------Optional Utility Functions------------------------------


def deterministic_uuid(content: Union[str, bytes, list] = None):
    # Generate a deterministic UUID from the given content or current time
    if content is None:
        content = str(time.time())
    if isinstance(content, list):
        content = "/".join([str(x) for x in content if x is not None])
    if isinstance(content, str):
        content = content.encode("utf-8")
    hash_object = hashlib.md5(content)
    return hash_object.hexdigest()


def translate_string_name(name: str) -> str:
    # Translate a string to a valid Python variable name
    punc = string.punctuation + " "
    new_name = (
        name.lower().strip().translate(str.maketrans(punc, "_" * len(punc))).strip("_")
    )
    return re.sub(r"_+", "_", new_name)


def format_analysis_output(output_df, name: str = None) -> str:
    # Format the analysis output to a string
    if isinstance(output_df, pd.Series):
        output_df = output_df.to_frame()
    if isinstance(output_df, list):
        return "\n".join([format_analysis_output(df) for df in output_df])
    if isinstance(output_df, dict):
        return "\n".join(
            [format_analysis_output(df, name) for name, df in output_df.items()]
        )
    if not isinstance(output_df, pd.DataFrame):
        return str(output_df)
    else:
        return format_dataframe(output_df, name)


def format_dataframe(output_df: Union[None, pd.DataFrame], name: str = None) -> str:
    name = name or "Dataframe"
    if output_df.size > 100:
        buffer = io.StringIO()
        output_df.info(buf=buffer)
        df_display = pd.concat([output_df.head(50), output_df.tail(50)], axis=0)
        df_string = f"DataFrame name: {name}\n"
        df_string += f"DataFrame snapshot:\n{_df_to_string(df_display)}\n\n"
        df_string += f"DataFrame column details:\n{buffer.getvalue()}"
    else:
        df_string = f"{name}:\n{_df_to_string(output_df)}"
    return df_string


def _df_to_string(output_df: pd.DataFrame) -> str:
    output_df.columns = [str(col) for col in output_df.columns.tolist()]
    datetimecols = [
        col
        for col in output_df.columns.tolist()
        if ("date" in col.lower() or "time" in col.lower())
        and isinstance(output_df[col].dtype, np.number)
    ]
    if "timestamp" in output_df.columns and "timestamp" not in datetimecols:
        datetimecols.append("timestamp")
    for col in datetimecols:
        output_df[col] = output_df[col].astype(dtype="datetime64[ns]", errors="ignore")
        output_df.loc[:, col] = pd.to_datetime(output_df[col], errors="ignore")

    datetimecols = output_df.select_dtypes(include=["datetime64"]).columns.tolist()
    formatters = {col: _format_date for col in datetimecols}
    return output_df.to_string(
        float_format="{:,.2f}".format,
        formatters=formatters,
        na_rep="None",
    )


def _format_date(date: pd.Timestamp):
    return date.strftime("%d %b %Y %H:%M")


def extract_df_names(code: str, df_names: list[str]) -> list[str]:
    # extract dataframe names from given code
    extracted_names = []
    for name in df_names:
        if name in code:
            extracted_names.append(name)
    return extracted_names


def extract_column_names(code: str, df_columns: list[str]) -> list[str]:
    # extract column names from given code
    cols_dict = {remove_punctuation_from_string(col): col for col in df_columns}
    regex = [r"\"(.*?)\"", r"'(.*?)'"]
    cols = []
    for reg in regex:
        for x in re.finditer(reg, code):
            for a in x.groups():
                if remove_punctuation_from_string(a).strip() != "":
                    cols.append(remove_punctuation_from_string(a))
    return list(set(cols_dict[c] for c in cols if c in cols_dict))


def remove_punctuation_from_string(value: str) -> str:
    value = str(value).strip()
    value = value.translate(str.maketrans("", "", string.punctuation))
    value = value.replace(" ", "").lower()
    return value


def make_locals_string(locals_: dict) -> str:
    # Create a string representation of the locals dictionary
    locals_str = "{\n"
    for name, value in locals_.items():
        if isinstance(value, pd.DataFrame):
            locals_str += f"{name} (DataFrame):\n{value.head(5).to_markdown()},\n"
        elif isinstance(value, dict):
            locals_str += f"{name} (dict): " + "{\n"
            for df_name, df in value.items():
                if isinstance(df, pd.DataFrame):
                    locals_str += (
                        f"{df_name} (DataFrame):\n{df.head(5).to_markdown()},\n"
                    )
                else:
                    locals_str += f"{df_name} ({type(df).__name__}): {df},\n"
            locals_str += "},\n"
        else:
            locals_str += f"{name} ({type(value).__name__}): {value},\n"
    return locals_str + "}"
