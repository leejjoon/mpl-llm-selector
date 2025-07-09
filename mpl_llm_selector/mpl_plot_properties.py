import pandas as pd
from matplotlib.colors import to_hex
from typing import List, Iterator, Any, Dict
from matplotlib.axes import Axes
from pandas import DataFrame, Series, Index


class MplAxesProperties:
    def __init__(self, ax: Axes):
        self._ax: Axes = ax

        xx: List[Dict[str, Any]] = self.get_artist_attrs_all(get_id=True)
        self._df_artists: DataFrame = pd.DataFrame(xx)

        labs: List[Dict[str, Any]] = self.get_label_properties()
        self._df_legend: DataFrame = pd.DataFrame(labs)

    def get_artist_attrs(self, l: Any, get_bbox: bool = True, get_id: bool = True) -> Dict[str, Any]:
        ax = self._ax

        if get_bbox:
            bbox = l.get_window_extent().transformed(ax.transData.inverted())
            x = dict(zip(["xmin", "ymin", "xmax", "ymax"], bbox.extents))
        else:
            x = dict()

        # x["kind"] = kind

        for k in ["color", "facecolor", "edgecolor", "linewidth", "label"]:
            if hasattr(l, f"get_{k}"):
                v = getattr(l, f"get_{k}")()
                if "color" in k:
                    v = v and to_hex(v)
                x[k] = v
            else:
                x[k] = None

        if get_id:
            x["id"] = id(l)

        return x


    def get_artist_attrs_all(self, get_id: bool = True) -> List[Dict[str, Any]]:
        ax = self._ax
        xx = []
        for kind, artists in [("lines", ax.lines),
                              ("patches", ax.patches),
                              ("collections", ax.collections)]:
            for i, l in enumerate(artists):

                x = self.get_artist_attrs(l, get_id=get_id)
                x["selector"] = f"{kind}[{i}]"
                xx.append(x)

        return xx

    def get_label_properties(self) -> List[Dict[str, Any]]:

        ax = self._ax

        labs = []
        for h, t in zip(ax.legend_.legend_handles, ax.legend_.get_texts()):
            lab = dict(label=t.get_text())
            lab.update(self.get_artist_attrs(h, get_bbox=False, get_id=False))
            labs.append(lab)

        return labs

    def get_axes_properties(self) -> Dict[str, Any]:

        ax = self._ax
        df_legend = self._df_legend
        df_artists = self._df_artists

        xticklabels = pd.DataFrame([dict(x=t._x, value=t.get_text())
                                    for t in ax.get_xticklabels()])
        yticklabels = pd.DataFrame([dict(x=t._y, value=t.get_text())
                                    for t in ax.get_yticklabels()])

        xlim = ax.get_xlim()
        ylim = ax.get_ylim()

        return dict(xlim=xlim,
                    ylim=ylim,
                    xticklabels_dataframe=xticklabels,
                    yticklabels_dataframe=yticklabels,
                    artist_dataframe=df_artists,
                    legend_dataframe=df_legend
                    )

    def get_context(self) -> str:

        prop = self.get_axes_properties()
        context = f"""

## Data limits of the axes

x = {prop["xlim"]}
y = {prop["ylim"]}

## Properties of Artists

{prop["artist_dataframe"].to_markdown(index=False)}

## X-axis tick labeles and their location

{prop["xticklabels_dataframe"].to_markdown(index=False)}


## y-axis tick labeles and their location

{prop["yticklabels_dataframe"].to_markdown(index=False)}

## legend

{prop["legend_dataframe"].to_markdown(index=False)}

"""

        return context

    def select_artists(self, id_list: List[int]) -> "SelectedArtists":
        selectors = self._df_artists.set_index("id").loc[id_list]["selector"]
        selected = SelectedArtists(self._ax, self._df_artists.set_index("selector"),
                                   selectors)
        return selected

import re
p_selector = re.compile(r"(\w+)\[(\d+)\]")

class SelectedArtists:
    # @classmethod
    # def from_axes(cls, ax):
    #     pass

    @classmethod
    def from_selectors(cls, ax: Axes, selectors: List[str]) -> "SelectedArtists":
        ax_prop = MplAxesProperties(ax)
        return cls(ax, ax_prop._df_artists.set_index("selector"), selectors)

    def __init__(self, ax: Axes, df_artists: DataFrame, selectors: List[str] | Series | Index):
        self._ax: Axes = ax
        self._df_artists_parent: DataFrame = df_artists
        self._selected_df: DataFrame = df_artists.loc[selectors]
        self._selectors: List[str] | Series | Index = selectors

    def __repr__(self) -> str:
        if isinstance(self._selectors, pd.Series):
            selectors = list(self._selectors.values)
        else:
            selectors = self._selectors
        return f"SelectedArtists: {selectors}"

    def inverted(self) -> "SelectedArtists":
        inverted_idx = self._df_artists_parent.index.difference(self._selectors)

        return type(self)(self._ax, self._df_artists_parent, inverted_idx)

    def iter_artists(self) -> Iterator[Any]:
        for selector in self._selectors:
            m = p_selector.match(selector)
            kind, ind = m.groups()
            a = getattr(self._ax, kind)[int(ind)]
            yield a

    def show_selectors(self) -> List[str]:
        return list(self._selectors)

    def set(self, *kl: Any, **kwargs: Any) -> None:
        for a in self.iter_artists():
            a.set(*kl, **kwargs)

