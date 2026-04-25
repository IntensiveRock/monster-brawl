import pandas as pd
import click
from monster_brawl.card import *
from PIL import Image, ImageDraw, ImageFont, ImageText, ImageOps
import click


@click.command()
@click.argument('cardtype')
def main(cardtype : str):
    if cardtype == "m":
        card_type = "monsters"
        mon_name = "Sentient Suit of Barbarian Armor"
    elif cardtype == "g":
        card_type = "gear"
        mon_name = "short sword"
    elif cardtype == "s":
        card_type = "spells"
        mon_name = "fireball"
    card_file = pd.read_excel('/home/dewdrop/Projects/ccb/monster-brawl/data/Cards.xlsx', sheet_name=card_type, header=0, index_col=None)
    cards = {}
    buffs = {"ATK Buff" : 0,
             "HP Buff" : 0,
             "Shield Buff" : 0,
             "Armor Buff" : 0,
             "Reach Buff" : 0}
    if card_type == "monsters":
        for index, row in card_file.iterrows():
            tmp_monster = MonsterCard(
                name=row['Name'],
                desc=row['Description'],
                mtype=row['Monster Type'],
                rank=row['Monster Rank'],
                hp=row['HP'],
                atk=row['ATK'],
                speed=row['Speed'])
            cards[row['Name']] = tmp_monster
    elif card_type == "gear":
        for index, row in card_file.iterrows():
            tmp_monster = GearCard(
                name=row['Name'],
                desc=row['Description'],
                gtype=row['Gear Type'],
                rank=row['Gear Rank'],
                cost=row['Cost'],
                buffs=buffs)
            cards[row['Name']] = tmp_monster
    elif card_type == "spells":
        for index, row in card_file.iterrows():
            tmp_monster = SpellCard(
                name=row['Name'],
                desc=row['Description'],
                cost=row['Cost'])
            cards[row['Name']] = tmp_monster


    mon = cards[mon_name]
    template = mon.draw()
    template.show()

if __name__ == "__main__":
    main()
