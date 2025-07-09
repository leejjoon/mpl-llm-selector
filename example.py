import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns

# %%

sns.set_theme(style="ticks", palette="pastel")

# Load the example tips dataset
tips = sns.load_dataset("tips")

fig, ax = plt.subplots(1, 1, num=1, clear=True)

# Draw a nested boxplot to show bills by day and time
sns.boxplot(x="day", y="total_bill",
            hue="smoker", palette=["m", "g"],
            data=tips, ax=ax)

sns.despine(offset=10, trim=True)


# %%

from mpl_llm_selector import query_artists

q = "artists for Friday"
selected = query_artists(ax, q)
print(selected)

# %%

# from mpl_llm_selector import from_selectors
# selectors = ['patches[1]', 'patches[5]',
#              'lines[6]', 'lines[7]', 'lines[8]', 'lines[9]', 'lines[10]', 'lines[11]',
#              'lines[30]', 'lines[31]', 'lines[32]', 'lines[33]', 'lines[34]']
# selected = from_selectors(ax, selectors)

# %%

selected.inverted().set(alpha=0.2)

plt.show()

# # %%

# from mpl_plot_properties import MplAxesProperties, SelectedArtists
# import mpl_llm_query

# ax_prop = MplAxesProperties(ax)

# ax_prop_context = ax_prop.get_context()

# # %%

# q = "artists for Friday"  # this should return 12 artists. sometimes it returns
#                           # 8 or less which is incorrect. The context need to be improved.

# response = mpl_llm_query.query(ax_prop_context, q)

# # %%

# selected = ax_prop.select_artists(response.items)

# selected.inverted().set(alpha=0.2)

# # %%

# import json
# json.dumps(selected.show_selectors())

# # %%

# selectors = json.loads('["lines[6]", "lines[7]", "lines[8]", "lines[9]", "lines[10]", "lines[11]", "lines[30]", "lines[31]", "lines[32]", "lines[33]", "lines[34]", "patches[1]", "patches[5]"]')

# selected = SelectedArtists.from_selectors(ax, selectors)

# # %%

# q = "patches for Friday"

# response = mpl_llm_query.query(ax_prop_context, q)
# selected = ax_prop.select_artists(response.items)
# selected.show_selectors()
