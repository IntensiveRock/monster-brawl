"""
After running the deckbuilder, construct the card images.
"""
import click
from pathlib import Path
from PIL import Image

from monster_brawl.db import grab_cards_from_db
from monster_brawl.card import MonsterCard, GearCard, SpellCard
from monster_brawl.db_to_lua_table import make_lua_file


@click.command()
@click.option('-n', '--name', help="Name for the new deck")
@click.option('-r', '--rows', help="Number of rows in sheet", default=7)
@click.option('-c', '--cols', help="Number of rows in sheet", default=10)
@click.argument('DECKPATH', type=click.Path(exists=True))
def db_to_images(name, rows, cols, deckpath):
    monsters, mcols = grab_cards_from_db(Path(deckpath), "monsters")
    # lua_list += make_lua_file(tbl="monsters", cards=monsters, cols=mcols)
    gear, gcols = grab_cards_from_db(Path(deckpath), "gear")
    # lua_list += make_lua_file(tbl="gear", cards=gear, cols=gcols)
    spells, scols = grab_cards_from_db(Path(deckpath), "spells")
    # lua_list += make_lua_file(tbl="spells", cards=spells, cols=scols) + ["]\n"]
    # with open("cardlist.fnl", "w") as f:
    #     for line in lua_list:
    #         f.write(line)
    monster_list = []
    gear_list = []
    spells_list = []
    card_list = []
    for index, row in enumerate(monsters):
        try:
            tmp_monster = MonsterCard(
                name=row[0],
                desc=row[5],
                mtype=row[1],
                rank=int(row[2]),
                hp=row[3],
                atk=row[4],)
            img = tmp_monster.draw()
            monster_list.append(row)
            card_list.append(img)
        except:
            pass
    for index, row in enumerate(gear):
        try:
            tmp_monster = GearCard(
                name=row[0],
                desc=row[4],
                gtype=row[1],
                rank=row[2],
                cost=row[3])
            img = tmp_monster.draw()
            gear_list.append(row)
            card_list.append(img)
        except:
            pass
    for index, row in enumerate(spells):
        try:
            tmp_monster = SpellCard(
                name=row[0],
                desc=row[2],
                cost=row[1])
            img = tmp_monster.draw()
            spells_list.append(row)
            card_list.append(img)
        except:
            pass
    lua_list = ["[\n"]
    lua_list += make_lua_file(tbl="monsters", cards=monster_list, cols=mcols)
    lua_list += make_lua_file(tbl="gear", cards=gear_list, cols=gcols)
    lua_list += make_lua_file(tbl="spells", cards=spells_list, cols=scols) + ["]\n"]
    with open("cardlist.fnl", "w") as f:
        for line in lua_list:
            f.write(line)
    deck_grid = image_grid(card_list, rows, cols)
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
