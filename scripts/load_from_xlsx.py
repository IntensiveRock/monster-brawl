import pandas as pd
import click
from monster_brawl.card import MonsterCard, GearCard, SpellCard
import os
from pathlib import Path, PureWindowsPath, PurePosixPath
import platform
import logging

_logger = logging.getLogger(__name__)

# platform.system() >>> windows


@click.command()
@click.argument('FILEPTH', type=click.Path(exists=True))
def load_from_xslx(filepth):
    monster_file = pd.read_excel(filepth, sheet_name="monsters", header=0, index_col=None)
    gear_file = pd.read_excel(filepth, sheet_name="gear", header=0, index_col=None)
    spell_file = pd.read_excel(filepth, sheet_name="spells", header=0, index_col=None)
    os.mkdir("tmp")
    card_dir = "tmp"
    _logger.info("Starting monsters...")
    for index, row in monster_file.iterrows():
        try:
            tmp_monster = MonsterCard(
                name=row['Name'],
                desc=row['Description'],
                mtype=row['Monster Type'],
                rank=row['Monster Rank'],
                hp=row['HP'],
                atk=row['ATK'],)
            img = tmp_monster.draw()
            cpath = Path(card_dir, f"{tmp_monster.name}.png")
            if platform.system() == "Windows":
                cpath = PureWindowsPath(*cpath.parts)
            img.save(cpath)
        except:
            pass
    _logger.info("Starting gear...")
    for index, row in gear_file.iterrows():
        try:
            tmp_monster = GearCard(
                name=row['Name'],
                desc=row['Description'],
                gtype=row['Gear Type'],
                rank=row['Gear Rank'],
                cost=row['Cost'])
            img = tmp_monster.draw()
            cpath = Path(card_dir, f"{tmp_monster.name}.png")
            if platform.system() == "Windows":
                cpath = PureWindowsPath(*cpath.parts)
            img.save(cpath)
        except:
            pass
    _logger.info("Starting spells...")
    for index, row in spell_file.iterrows():
        try:
            tmp_monster = SpellCard(
                name=row['Name'],
                desc=row['Description'],
                cost=row['Cost'])
            img = tmp_monster.draw()
            cpath = Path(card_dir, f"{tmp_monster.name}.png")
            if platform.system() == "Windows":
                cpath = PureWindowsPath(*cpath.parts)
            img.save(cpath)
        except:
            pass
    

if __name__ == "__main__":
    load_from_xslx()
