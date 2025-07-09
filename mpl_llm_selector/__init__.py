from .mpl_plot_properties import MplAxesProperties, SelectedArtists
from . import mpl_llm_query
import asyncio
from matplotlib.axes import Axes
from typing import List


async def async_query_artists(ax: Axes, q: str) -> SelectedArtists:
    ax_prop = MplAxesProperties(ax)

    ax_prop_context = ax_prop.get_context()
    response = await mpl_llm_query.async_query(ax_prop_context, q)
    selected = ax_prop.select_artists(response.items)

    return selected


def query_artists(ax: Axes, q: str) -> SelectedArtists:
    return asyncio.run(async_query_artists(ax, q))


def from_selectors(ax: Axes, selectors: List[str]) -> SelectedArtists:
    selected = SelectedArtists.from_selectors(ax, selectors)
    return selected
