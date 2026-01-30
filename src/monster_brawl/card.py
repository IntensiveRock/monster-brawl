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
        template_pth = Path(CARD_PATHS[f"template_pth"]) / Path(f"{self.mtype}-{self.rank}.png")
        template = Image.open(template_pth)
        if self.pic != None:
            ...
        numfont = ImageFont.truetype(CARD_PATHS["font_path"], size=70)
        namefont = ImageFont.truetype(CARD_PATHS["font_path"], size=30)
        descfont = ImageFont.truetype(CARD_PATHS["font_path"], size=25)
        draw = ImageDraw.Draw(template)
        draw.text((105, 290), massage_desc(self.name, 15), font=namefont, fill='black')
        # Desc
        draw.multiline_text((40, 40), massage_desc(self.desc, 23), font=descfont, fill='black')
        # HP
        draw.text((40, 290), str(int(self.hp)), font=numfont, fill='green')
        # ATK
        draw.text((40, 380), str(int(self.atk)), font=numfont, fill='red')
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
        template_pth = Path(CARD_PATHS[f"template_pth"]) / Path(f"gear.png")
        template = Image.open(template_pth)
        if self.pic != None:
            ...
        numfont = ImageFont.truetype(CARD_PATHS["font_path"], size=70)
        namefont = ImageFont.truetype(CARD_PATHS["font_path"], size=30)
        descfont = ImageFont.truetype(CARD_PATHS["font_path"], size=25)
        draw = ImageDraw.Draw(template)
        #Name
        draw.text((130, 290), massage_desc(self.name, 15), font=namefont, fill='black')
        #draw_underlined_text(draw, (50, 150), mon.name, font=namefont, fill='black')
        # Desc
        draw.multiline_text((40, 40), massage_desc(self.desc, 20), font=descfont, fill='black')
        draw.text((50,310), str(int(self.cost)), font=numfont, fill='black')
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
        template_pth = Path(CARD_PATHS[f"template_pth"]) / Path(f"spell.png")
        template = Image.open(template_pth)
        if self.pic != None:
            ...
        numfont = ImageFont.truetype(CARD_PATHS["font_path"], size=70)
        namefont = ImageFont.truetype(CARD_PATHS["font_path"], size=30)
        descfont = ImageFont.truetype(CARD_PATHS["font_path"], size=25)
        draw = ImageDraw.Draw(template)
        #Name
        draw.text((130, 290), massage_desc(self.name, 15), font=namefont, fill='black')
        #draw_underlined_text(draw, (50, 150), mon.name, font=namefont, fill='black')
        # Desc
        draw.multiline_text((40, 40), massage_desc(self.desc, 20), font=descfont, fill='black')
        draw.text((50,310), str(int(self.cost)), font=numfont, fill='black')
        return template
        

def massage_desc(desc, char_len):
    new_text = ""
    i = 0
    recent_white_space = 0
    for j, char in enumerate(desc):
        if i >= char_len:
            if char == " ":
                new_text += " \n"
                i = 0
            else:
                before = new_text[:recent_white_space]
                after = new_text[recent_white_space+1:]
                new_text = before + "\n" + after + char
                i = len(after) + 1
        else:
            if char == " ":
                recent_white_space = j
            new_text += char
            i += 1
    return new_text

# def massage_desc(desc, char_len):
#     if len(desc) == 0:
#         return ""
#     else:
#         new_text = ""
#         i = 0
#         for char in desc:
#             if i >= char_len:
#                 new_text += "\n"+char
#                 i = 0
#             else:
#                 new_text += char
#                 i += 1
#         return new_text
