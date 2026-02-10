import pandas as pd
import click
from pathlib import Path
import logging
import math

from monster_brawl.card import MonsterCard, GearCard, SpellCard
from monster_brawl.db import save_monster_db, save_gear_db, save_spell_db

_logger = logging.getLogger(__name__)

# platform.system() >>> windows


@click.command()
@click.argument('FILEPTH', type=click.Path(exists=True))
def main(filepth):
    monster_file = pd.read_excel(filepth, sheet_name="monsters", header=0, index_col=None)
    gear_file = pd.read_excel(filepth, sheet_name="gear", header=0, index_col=None)
    spell_file = pd.read_excel(filepth, sheet_name="spells", header=0, index_col=None)
    _logger.info("Loading monsters...")
    monster_list = []
    for index, row in monster_file.iterrows():        
        try:
            if not math.isnan(row['Monster Rank']):
                tmp_monster = MonsterCard(
                    name=row['Name'],
                    desc=row['Description'],
                    mtype=row['Monster Type'],
                    rank=row['Monster Rank'],
                    hp=row['HP'],
                    atk=row['ATK'],
                    speed=row['speed']
                )
                monster_list.append(tmp_monster)
        except:
            pass
    save_monster_db(monster_list, Path("monsters"), Path("."))
    _logger.info("Loading gear...")
    gear_list = []
    for index, row in gear_file.iterrows():
        if type(row['Name']) == float :
            break
        try:
            tmp_monster = GearCard(
                name=row['Name'],
                desc=row['Description'],
                gtype=row['Gear Type'],
                rank=row['Gear Rank'],
                cost=row['Cost'])
            gear_list.append(tmp_monster)
        except:
            pass
    save_gear_db(gear_list, Path("gear"), Path("."))
    _logger.info("Starting spells...")
    spell_list = []
    for index, row in spell_file.iterrows():
        try:
            tmp_monster = SpellCard(
                name=row['Name'],
                desc=row['Description'],
                cost=row['Cost'])
            spell_list.append(tmp_monster)
        except:
            pass
    save_spell_db(spell_list, Path("spells"), Path("."))
    

if __name__ == "__main__":
    main()
