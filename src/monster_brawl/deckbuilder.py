from rich.text import Text


from textual import events
from textual.app import App, ComposeResult
from textual.containers import Container, Horizontal, VerticalScroll, Vertical
from textual.widgets import Header, Static, DataTable, Label, SelectionList, Footer, Input
from textual.message import Message

from monster_brawl.tui_resources import SourceTable, DeckTable, DeckLoad
from monster_brawl.config import CARD_PATHS
from monster_brawl.db import deckbuild_to_db





class DeckbuilderApp(App):
    # Make a widget that keeps track of card counts for total and each table.
    
    CSS_PATH = "deckbuilder.tcss"

    TITLE = "Monster Brawl Deckbuilder"

    BINDINGS = [
        ("e", "export_deck()", "Export Deck"),
        ("l", "push_screen('load')", "Load Deck")
    ]

    def compose(self) -> ComposeResult:
        self.monster_table = SourceTable("Monsters", CARD_PATHS["db_pth"], "monsters")
        self.gear_table = SourceTable("Gear", CARD_PATHS["db_pth"], "gear")
        self.spell_table = SourceTable("Spells", CARD_PATHS["db_pth"], "spells")
        self.mdeck_table = DeckTable("Monster Deck", CARD_PATHS["db_pth"], "monsters")
        self.gdeck_table = DeckTable("Gear Deck", CARD_PATHS["db_pth"], "gear")
        self.sdeck_table = DeckTable("Spells Deck", CARD_PATHS["db_pth"], "spells")
        self.install_screen(DeckLoad(), name='load')
        yield Header()
        yield Footer()
        with Container(id="app-grid"):
            with Vertical(id="left-pane"):
                yield self.mdeck_table
                yield self.gdeck_table
                yield self.sdeck_table
            with Vertical(id="top-right"):
                yield self.monster_table
                yield self.gear_table
                yield self.spell_table

    def action_load_deck(self,):
        """Load a deck from provided path."""
        ...
        

    def action_export_deck(self,):
        """
        Take all of the rows from monster, gear and spell gear decks and make a directory with images.
        """
        mrows = self.mdeck_table.dt.rows
        deck_dict = {}
        deck_dict["monsters"] = []
        for key in mrows.keys():
                row = mrows[key]
                rowkey = row.key
                row_list = self.mdeck_table.dt.get_row(rowkey)
                deck_dict["monsters"].append(row_list)
        grows = self.gdeck_table.dt.rows
        deck_dict["gear"] = []
        for key in grows.keys():
                row = grows[key]
                rowkey = row.key
                row_list = self.gdeck_table.dt.get_row(rowkey)
                deck_dict["gear"].append(row_list)
        srows = self.sdeck_table.dt.rows
        deck_dict["spells"] = []
        for key in srows.keys():
                row = srows[key]
                rowkey = row.key
                row_list = self.sdeck_table.dt.get_row(rowkey)
                deck_dict["spells"].append(row_list)
        deckbuild_to_db(deck_dict)
        
        

    def on_source_table_row_selected(self, event : SourceTable.RowSelected):
        row = event.row
        row_tup = row.data_table.get_row(row.row_key)
        if len(row_tup) == 7:
            self.mdeck_table.add_row(row)
        elif len(row_tup) == 6:
            self.gdeck_table.add_row(row)
        elif len(row_tup) == 4:
            self.sdeck_table.add_row(row)
        else:
            print("Cannot find table")

    def on_deck_table_row_selected(self, event : DeckTable.RowSelected):
        row = event.row
        row_tup = row.data_table.get_row(row.row_key)
        if len(row_tup) == 7:
            self.mdeck_table.remove_row(row)
        elif len(row_tup) == 6:
            self.gdeck_table.remove_row(row)
        elif len(row_tup) == 4:
            self.sdeck_table.remove_row(row)
        else:
            print("Cannot find table")

    def on_deck_load_path_submitted(self, event : DeckLoad.PathSubmitted):
        self.mdeck_table.load(event.path_str, "monsters")
        self.gdeck_table.load(event.path_str, "gear")
        self.sdeck_table.load(event.path_str, "spells")
        self.pop_screen()


def main():
    app = DeckbuilderApp()
    app.run()
    
if __name__ == "__main__":
    main()
