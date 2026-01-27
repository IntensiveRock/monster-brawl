"""
After running the deckbuilder, construct the card images.
"""
import click
from pathlib import Path
from PIL import Image

from monster_brawl.db import grab_cards_from_db
from monster_brawl.card import MonsterCard, GearCard, SpellCard


@click.command()
@click.option('-n', '--name', help="Name for the new deck")
@click.argument('DECKPATH', type=click.Path(exists=True))
def db_to_images(name, deckpath):
    monsters, mcols = grab_cards_from_db(Path(deckpath), "monsters")
    gear, gcols = grab_cards_from_db(Path(deckpath), "gear")
    spells, scols = grab_cards_from_db(Path(deckpath), "spells")
    card_list = []
    for index, row in enumerate(monsters):
        try:
            tmp_monster = MonsterCard(
                name=row[0],
                desc=row[1],
                mtype=row[2],
                rank=row[3],
                hp=row[4],
                atk=row[5],)
            img = tmp_monster.draw()
            card_list.append(img)
        except:
            pass
    for index, row in enumerate(gear):
        try:
            tmp_monster = GearCard(
                name=row[0],
                desc=row[1],
                gtype=row[2],
                rank=row[3],
                cost=row[4])
            img = tmp_monster.draw()
            card_list.append(img)
        except:
            pass
    for index, row in enumerate(spells):
        try:
            tmp_monster = SpellCard(
                name=row[0],
                desc=row[1],
                cost=row[2])
            img = tmp_monster.draw()
            card_list.append(img)
        except:
            pass
    deck_grid = image_grid(card_list, 7, 10)
    deck_grid.save(f"{name}.png")

def image_grid(imgs, rows, cols):
    w, h = imgs[0].size
    grid = Image.new('RGB', size=(cols*w, rows*h))
    grid_w, grid_h = grid.size
    for i, img in enumerate(imgs):
        grid.paste(img, box=(i%cols*w, i//cols*h))
    return grid


if __name__ == "__main__":
    db_to_images()
