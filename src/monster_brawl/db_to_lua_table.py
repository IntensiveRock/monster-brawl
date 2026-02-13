import sqlite3
from monster_brawl.db import grab_cards_from_db
from pathlib import Path
import click

tables = ["monsters", "gear", "spells"]

# @click.command()
# @click.argument("dbpth", type=click.Path(exists=True))
# def main(dbpth):
#     card_str_list = ["[\n"]
#     for tbl in tables:
#         card_str_list += make_lua_file(dbpth, tbl)
#     card_str_list += ["]\n"]
#     with open("cardlist.fnl", "w") as f:
#         for line in card_str_list:
#             f.write(line)


def make_lua_file(dbpth = None, tbl = None, cards = None, cols = None):
    if cards:
        cards = cards
        columns = cols
    else:
        cards, columns = grab_cards_from_db(dbpth, tbl)
    card_list = []
    for card in cards:
        card_str = "{:kind " + f'"{tbl}"'
        for i, column in enumerate(columns):
            if type(card[i]) == str:
                card_str += f' :{column} "{card[i]}"'
            elif card[i] == None:
                card_str += f' :{column} nil'
            else:
                card_str += f" :{column} {card[i]}"
        card_str += "}\n"
        card_list += card_str
    return card_list
    

# if __name__ == "__main__":
#     main()
