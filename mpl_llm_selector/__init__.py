from .mpl_plot_properties import MplAxesProperties, SelectedArtists
from . import mpl_llm_query



def query_artists(ax, q: str) -> SelectedArtists:
    ax_prop = MplAxesProperties(ax)

    ax_prop_context = ax_prop.get_context()
    response = mpl_llm_query.query(ax_prop_context, q)
    selected = ax_prop.select_artists(response.items)

    return selected

def from_selectors(ax, selectors: list[str]) -> SelectedArtists:
    selected = SelectedArtists.from_selectors(ax, selectors)
    return selected


