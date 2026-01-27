from rich.text import Text

from textual.screen import Screen
from textual import events
from textual.app import App, ComposeResult
from textual.containers import Vertical
from textual.widgets import DataTable, Label, Static, Input, DirectoryTree
from textual.message import Message

from monster_brawl.db import grab_cards_from_db


class SourceTable( Vertical ):

    class RowSelected(Message):
        """Sent when the table is selected"""
        def __init__(self, row):
            super().__init__()
            self.row = row
    
    def __init__( self, title: str , db_pth : str = None, table_name : str = None) -> None:
        super().__init__()
        self._title = title
        if db_pth is not None:
            self.cards, self.cols = grab_cards_from_db(db_pth, table_name)
            self.popd = True
        else:
            self.popd = False
        self.dt = self._test_dt(table_name)

    def _test_dt( self, table_name ) -> DataTable:
        dt = DataTable()
        dt.zebra_stripes = True
        dt.cursor_type   = "row"
        # dt.name = table_name
        # dt.fixed_columns = 1
        if self.popd:
            for i, col in enumerate(self.cols):
                if i == 0:
                    dt.add_column(col, width=20)
                elif i ==1:
                    dt.add_column(col, width=100)
                else:
                    dt.add_column(col, width=10)
            dt.add_rows(self.cards)
        return dt

    def on_data_table_row_selected(self, row):
        row.stop()
        self.post_message(self.RowSelected(row))

    def compose( self ) -> ComposeResult:
        yield Label( self._title )
        # yield self._test_dt()
        yield self.dt


class DeckTable( Vertical ):

    class RowSelected(Message):
        """Sent when the table is selected"""
        def __init__(self, row):
            super().__init__()
            self.row = row

    def __init__( self, title: str , db_pth : str = None, table_name : str = None) -> None:
        super().__init__()
        self._title = title
        if db_pth is not None:
            self.cards, self.cols = grab_cards_from_db(db_pth, table_name)
            self.popd = True
        else:
            self.popd = False
        self.dt = self._test_dt()

    def _test_dt( self ) -> DataTable:
        dt = DataTable()
        dt.zebra_stripes = True
        dt.cursor_type   = "row"
        # dt.fixed_columns = 1
        if self.popd:
            for i, col in enumerate(self.cols):
                if i == 0:
                    dt.add_column(col, width=20)
                elif i == 1:
                    dt.add_column(col, width=100)
                else:
                    dt.add_column(col, width=10)
        return dt

    def on_data_table_row_selected(self, row):
        row.stop()
        self.post_message(self.RowSelected(row))

    def add_row(self, row) -> DataTable:
        row_tup = row.data_table.get_row(row.row_key)
        self.dt.add_row(*row_tup)

    def load(self, db_pth, table_name):
        self.cards, _ = grab_cards_from_db(db_pth, table_name)
        self.dt.add_rows(self.cards)

    def remove_row(self, row) -> DataTable:
        self.dt.remove_row(row.row_key)

    def compose( self ) -> ComposeResult:
        yield Label( self._title )
        # yield self._test_dt()
        yield self.dt


class DeckLoad(Screen):
    BINDINGS = [("escape", "app.pop_screen", "Pop screen")]

    class PathSubmitted(Message):
        """Sent when the table is selected"""
        def __init__(self, path_str):
            super().__init__()
            self.path_str = path_str

    def compose(self) -> ComposeResult:
        yield Static(" Select deck database file ", id="title")
        yield DirectoryTree("./")

    def on_directory_tree_file_selected(self, fs :DirectoryTree.FileSelected):
        fs.stop()
        self.post_message(self.PathSubmitted(fs.path))
