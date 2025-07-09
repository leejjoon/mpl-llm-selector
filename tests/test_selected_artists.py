from mpl_llm_selector.mpl_plot_properties import SelectedArtists

def test_selected_artists_repr():
    selectors = ["lines[0]", "lines[1]"]
    # Create a dummy df_artists for the SelectedArtists constructor
    class DummyDfArtists:
        def __init__(self, selectors):
            self.index = selectors
        @property
        def loc(self):
            class LocIndexer:
                def __init__(self, parent):
                    self.parent = parent
                def __getitem__(self, key):
                    return self.parent
            return LocIndexer(self)

    dummy_df_artists = DummyDfArtists(selectors)
    # Pass None for ax as it's not used in __repr__
    selected_artists_instance = SelectedArtists(None, dummy_df_artists, selectors)
    expected_repr = f"SelectedArtists: {selectors}"
    assert repr(selected_artists_instance) == expected_repr
