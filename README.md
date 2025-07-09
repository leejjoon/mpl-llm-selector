# mpl-llm-selector

`mpl-llm-selector` is a Python package that allows you to select `matplotlib` artists using natural language queries, powered by large language models.

## Installation

This project uses [Poetry](https://python-poetry.org/) for dependency management.

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-repo/mpl-llm-selector.git
    cd mpl-llm-selector
    ```

2.  **Install dependencies:**
    ```bash
    poetry install
    ```

3.  **Activate the virtual environment:**
    ```bash
    poetry shell
    ```

## Google API Key

This package utilizes Google's Gemini API for natural language processing. You need to set up a `GOOGLE_API_KEY` environment variable.

**How to get a `GOOGLE_API_KEY`:**

*   **Google AI Studio:** [https://aistudio.google.com/](https://aistudio.google.com/)
*   **Google Cloud Console:** [https://console.cloud.google.com/](https://console.cloud.google.com/) (Look for "APIs & Services" -> "Credentials")

**Setting the API Key:**

It is recommended to create a `.env` file in the root directory of the project and add your API key there:

```
GOOGLE_API_KEY="your_google_api_key_here"
```

The package will automatically load this key.

## Usage

Here's an example demonstrating how to use `mpl-llm-selector` to select artists from a `matplotlib` plot:

```python
import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

sns.set_theme(style="ticks", palette="pastel")

# Load the example tips dataset
tips = sns.load_dataset("tips")

fig, ax = plt.subplots(1, 1, num=1, clear=True)

# Draw a nested boxplot to show bills by day and time
sns.boxplot(x="day", y="total_bill",
            hue="smoker", palette=["m", "g"],
            data=tips, ax=ax)

sns.despine(offset=10, trim=True)

from mpl_llm_selector import query_artists

q = "artists for Friday"
selected = query_artists(ax, q)
print(selected)

selected.inverted().set(alpha=0.2)

plt.show()
```

To run this example:

1.  Save the code above as `example.py`.
2.  Ensure your `GOOGLE_API_KEY` is set (as described above).
3.  Run from your terminal:
    ```bash
    poetry run python example.py
    ```

This will display a plot where artists not matching "artists for Friday" are dimmed.
