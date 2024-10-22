# standard library imports
import logging

# third-party imports
import openai
import numpy as np
import pandas as pd
from dotenv import load_dotenv
import matplotlib.pyplot as plt

# local imports
from prompt_texts import PROMPTS
from utils import extract_python_code, clean_python_code, clean_analysis_output

load_dotenv()
client = openai.OpenAI()


class DataAnalyzr:
    def __init__(self):
        """Create a new instance of the DataAnalyzr class."""
        self.logger = logging.getLogger(__name__)
        logging.basicConfig(level=logging.INFO)

        (
            self.df,
            self.analysis_code,
            self.analysis_output,
            self.plot,
            self.plot_code,
            self.plot_path,
            self.insights_output,
        ) = (None,) * 7

    def get_data(self, filepath: str, **kwargs):
        """Read data from the given file."""

        self.df = pd.read_csv(filepath, **kwargs)

    def analysis(self, user_input: str):
        """Generate analysis output for the given user input."""
        completion = client.chat.completions.create(
            model="",  # your model here
            messages=[
                {
                    "role": "system",
                    "content": PROMPTS["name_of_prompt"],
                },  # system message
                {
                    "role": "user",
                    "content": PROMPTS["name_of_prompt"].format(user_input=user_input),
                },  # user message
            ],
            # set openai chat parameters here
        )
        llm_response = completion.choices[0].message.content

        # extract code from llm_response
        analysis_code = clean_python_code(extract_python_code(llm_response))

        # execute code and get output
        locals_ = {
            "pd": pd,
            "np": np,
            "df": self.df,
        }  # add any other libs required for the analysis here
        pd.options.mode.chained_assignment = None
        globals_ = locals_
        exec(analysis_code, globals_, locals_)
        analysis_output = clean_analysis_output(locals_["result"])

        return analysis_output, analysis_code

    def plotting(self, user_input: str):
        """Generate plot output for the given user input."""
        plot_path = "path/to/your/plot.png"

        # get plotting code
        completion = client.chat.completions.create(
            model="",  # your model here
            messages=[
                {
                    "role": "system",
                    "content": PROMPTS["name_of_prompt"],
                },  # system message
                {
                    "role": "user",
                    "content": PROMPTS["name_of_prompt"].format(user_input=user_input),
                },  # user message
            ],
            # set openai chat parameters here
        )
        llm_response = completion.choices[0].message.content

        # extract code from llm_response
        plot_code = clean_python_code(extract_python_code(llm_response))

        # execute code and get output
        locals_ = {
            "pd": pd,
            "np": np,
            "plt": plt,
            "df": self.df,
            "analysis_output": self.analysis_output,
        }  # add any other libs and data required for the plotting here
        pd.options.mode.chained_assignment = None
        globals_ = locals_
        exec(plot_code, globals_, locals_)
        self.plot = locals_["fig"]

        # save plot image to file
        plt.savefig(plot_path)
        plt.close("all")
        return plot_path, plot_code

    def insights(self, user_input: str):
        """Generate insights output for the given user input."""
        completion = client.chat.completions.create(
            model="",  # your model here
            messages=[
                {
                    "role": "system",
                    "content": PROMPTS["name_of_prompt"],
                },  # system message
                {
                    "role": "user",
                    "content": PROMPTS["name_of_prompt"].format(user_input=user_input),
                },  # user message
            ],
            # set openai chat parameters here
        )
        insights_output = completion.choices[0].message.content
        return insights_output

    def ask(self, user_input: str) -> dict[str, str]:
        """Ask a question and generate analysis, plot and insights outputs."""
        user_input = user_input.strip()
        assert (
            user_input is not None
            and isinstance(user_input, str)
            and user_input.strip() != ""
        ), "user_input is a required string parameter to generate outputs."

        self.analysis_output, self.analysis_code = self.analysis(user_input=user_input)
        self.plot_path, self.plot_code = self.plotting(user_input=user_input)
        self.insights_output = self.insights(user_input=user_input)
        return {
            "analysis_output": self.analysis_output,
            "plot_path": self.plot_path,
            "insights": self.insights_output,
        }
