"""
Database tools for cards and decks.
"""
import sqlite3
from pathlib import Path
import random

from monster_brawl.card import Card


def save_monster_db(card_list : list[Card], name : str, pth : Path):
    conn = sqlite3.connect(pth / "Cards.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE monsters(name, desc, mtype, rank, hp int, atk int, pic)")
    for i, card in enumerate(card_list):
        param_tuple = (card.name, card.desc, card.mtype, card.rank, card.hp, card.atk, card.pic)
        cur.execute("INSERT INTO monsters VALUES(?, ?, ?, ?, ?, ?, ?)", param_tuple)
    conn.commit()
    conn.close()


def save_gear_db(card_list : list[Card], name : str, pth : Path):
    conn = sqlite3.connect(pth / "Cards.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE gear(name, desc, mtype, rank, cost int, pic)")
    for i, card in enumerate(card_list):
        param_tuple = (card.name, card.desc, card.gtype, card.rank, card.cost, card.pic)
        cur.execute("INSERT INTO gear VALUES(?, ?, ?, ?, ?, ?)", param_tuple)
    conn.commit()
    conn.close()

def save_spell_db(card_list : list[Card], name : str, pth : Path):
    conn = sqlite3.connect(pth / "Cards.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE spells(name, desc, cost int, pic)")
    for i, card in enumerate(card_list):
        param_tuple = (card.name, card.desc, card.cost, card.pic)
        cur.execute("INSERT INTO spells VALUES(?, ?, ?, ?)", param_tuple)
    conn.commit()
    conn.close()

def deckbuild_to_db(card_dict):
    rand_num = "".join([str(random.randint(0,10)) for _ in range(5)])
    conn = sqlite3.connect(f"new_deck_{rand_num}.db")
    cur = conn.cursor()
    cur.execute("CREATE TABLE monsters(name, desc, mtype, rank, hp int, atk int, pic)")
    for i, card in enumerate(card_dict["monsters"]):
        # param_tuple = (card.name, card.desc, card.mtype, card.rank, card.hp, card.atk, card.pic)
        cur.execute("INSERT INTO monsters VALUES(?, ?, ?, ?, ?, ?, ?)", card)
    cur.execute("CREATE TABLE gear(name, desc, mtype, rank, cost int, pic)")
    for i, card in enumerate(card_dict["gear"]):
        # param_tuple = (card.name, card.desc, card.gtype, card.rank, card.cost, card.pic)
        cur.execute("INSERT INTO gear VALUES(?, ?, ?, ?, ?, ?)", card)
    cur.execute("CREATE TABLE spells(name, desc, cost int, pic)")
    for i, card in enumerate(card_dict["spells"]):
        # param_tuple = (card.name, card.desc, card.cost, card.pic)
        cur.execute("INSERT INTO spells VALUES(?, ?, ?, ?)", card)
    conn.commit()
    conn.close()


def grab_cards_from_db(db_pth : Path, table_name : str) -> list:
    """
    Grab specific spectral densities from a given database.
    """
    # First, select the rows where simnum=simnum
    # Second, reconstruct objects from params BLOB, need to unpickle that stuff
    conn = sqlite3.connect(db_pth)
    cur = conn.cursor()
    res = cur.execute(f"SELECT * FROM {table_name}")
    columns = [column[0] for column in cur.description]
    query_result = list(res.fetchall())
    # Returns a list of tuples containing coupling and parameters.
    return query_result, columns
