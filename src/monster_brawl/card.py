"""
The Card Class.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont

from monster_brawl.config import CARD_PATHS


class Card():
    """
    Generic Card Class
    """
    def __init(self, name : str, desc : str):
        self.name = name
        self.desc = desc


class MonsterCard(Card):
    """
    Monster Card.
    """
    def __init__(
            self,
            name : str,
            desc : str,
            mtype : str,
            rank : str,
            hp : int,
            atk : int,
            pic : Path = None,
    ):
        self.name = name
        self.desc = desc
        self.mtype = mtype
        self.rank = rank
        self.hp = hp
        self.atk = atk
        self.pic = pic

    def draw(self,):
        """
        Draw the monster card.
        """
        template = Image.open(CARD_PATHS["monster_template_path"])
        if self.pic != None:
            ...
        font = ImageFont.truetype(CARD_PATHS["font_path"], size=25)
        draw = ImageDraw.Draw(template)
        #Name
        draw.text((80, 550), self.name, font=font, fill='black')
        # Desc
        draw.multiline_text((80, 650), massage_desc(self.desc, 45), font=font, fill='black')
        # Rank
        draw.text((80, 470), self.rank[0], font=font, fill='black')
        # HP
        draw.text((250, 960), str(int(self.hp)), font=font, fill='black')
        # ATK
        draw.text((650, 960), str(int(self.atk)), font=font, fill='black')
        # Type
        draw.circle((660, 90), 30, fill=self.mtype)
        return template

        
        


class GearCard(Card):
    """
    Gear Card
    """
    def __init__(
            self,
            name : str,
            desc : str,
            gtype : str,
            rank : str,
            cost : str,
            pic : Path = None,
    ):
        self.name = name
        self.desc = desc
        self.gtype = gtype
        self.rank = rank
        self.cost = cost
        self.pic = pic

    def draw(self,):
        template = Image.open(CARD_PATHS["gear_template_path"])
        if self.pic != None:
            ...
        font = ImageFont.truetype(CARD_PATHS["font_path"], size=25)
        draw = ImageDraw.Draw(template)
        #Name
        draw.text((80, 550), self.name, font=font, fill='black')
        # Desc
        draw.multiline_text((80, 650), massage_desc(self.desc, 45), font=font, fill='black')
        # Rank
        draw.text((80, 470), self.rank[0], font=font, fill='black')
        # HP
        #draw.text((250, 960), str(int(mon.hp)), font=font, fill='black')
        # ATK
        draw.text((650, 960), str(int(self.cost)), font=font, fill='black')
        return template


class SpellCard(Card):
    """
    Gear Card
    """
    def __init__(
            self,
            name : str,
            desc : str,
            cost : int,
            pic : Path = None
    ):
        self.name = name
        self.desc = desc
        self.cost = cost
        self.pic = pic

    def draw(self,):
        template = Image.open(CARD_PATHS["spell_template_path"])
        if self.pic != None:
            ...
        font = ImageFont.truetype(CARD_PATHS["font_path"], size=25)
        draw = ImageDraw.Draw(template)
        draw.text((80, 550), self.name, font=font, fill='black')
        draw.multiline_text((80, 650), massage_desc(self.desc, 45), font=font, fill='black')
        draw.text((650, 960), str(int(self.cost)), font=font, fill='black')
        return template
        


def massage_desc(desc, char_len):
    if len(desc) == 0:
        return ""
    else:
        new_text = ""
        i = 0
        for char in desc:
            if i >= char_len:
                new_text += "\n"+char
                i = 0
            else:
                new_text += char
                i += 1
        return new_text
