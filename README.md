# mpl-llm-selector

`mpl-llm-selector` is a Python package that allows you to select `matplotlib` artists using natural language queries, powered by large language models.

## Usage

Here's an example demonstrating how to use `mpl-llm-selector` to select artists from a `matplotlib` plot:

```python
from mpl_llm_selector import query_artists

q = "artists for Friday"
selected = query_artists(ax, q)
print(selected)

selected.inverted().set(alpha=0.2)

plt.show()
```

This will display a plot where artists not matching "artists for Friday" are dimmed.

<img width="422" height="327" alt="Image" src="https://github.com/user-attachments/assets/0b55fb37-bccc-48ab-a8a3-0cad2625cefc" />

For the full example, take a look at [`usage_demonstration.ipynb`](notebooks/usage_demonstration.ipynb).

## Installation

This project uses [Poetry](https://python-poetry.org/) for dependency management.

### For Development (using Poetry)

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

### For Local Installation (using pip)

If you prefer to install the project directly using `pip` from the local source:

1.  **Clone the repository:**
    ```bash
    git clone https://github.com/your-repo/mpl-llm-selector.git
    cd mpl-llm-selector
    ```

2.  **Install in editable mode (recommended for development):**
    ```bash
    pip install -e .
    ```
    This allows changes in the source code to be reflected without re-installation.

3.  **Or, install normally:**
    ```bash
    pip install .
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

