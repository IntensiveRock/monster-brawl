"""
The Card Class.
"""
from pathlib import Path
from PIL import Image, ImageDraw, ImageFont, ImageText, ImageOps

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
            speed : int = None,
    ):
        self.name = name
        self.desc = desc
        self.mtype = mtype
        self.rank = rank
        self.hp = hp
        self.atk = atk
        self.pic = pic
        self.speed = speed

    def draw(self,):
        """
        Draw the monster card.
        """
        rank_dict = {1 : "d2", 2 : "d6", 3 : "d10"}
        round_pth = CARD_PATHS['template_pth']
        temp_outline_pth = round_pth / Path(f"{self.mtype}.png")
        temp_level_pth = round_pth / Path(f"{rank_dict[int(self.rank)]}.png")

        template = Image.open(temp_outline_pth)
        level = Image.open(temp_level_pth)

        template.paste(level, (0,0), level)

        numfont = ImageFont.truetype(CARD_PATHS["font_path"], size=80)
        namefont = ImageFont.truetype(CARD_PATHS["font_path"], size=40)
        descfont = ImageFont.truetype(CARD_PATHS["font_path"], size=40)

        draw = ImageDraw.Draw(template)
        
        # Name        
        name_font_size = 40
        max_name_length = 450
        name_text = ImageText.Text(self.name, namefont)
        name_length = name_text.get_length()
        name_text.stroke(1.2)
        while name_length > max_name_length:
            name_font_size -= 1
            namefont = ImageFont.truetype(CARD_PATHS["font_path"], size=name_font_size)
            name_text = ImageText.Text(self.name, namefont)
            name_text.stroke(1.2)
            name_length = name_text.get_length()                    
        name_loc = (60, 550)
        if self.mtype == 'black':
            draw.text(name_loc, name_text, fill=self.mtype)
        else:
            draw.text(name_loc, name_text, fill=self.mtype)
            
        # Desc
        base_max_text = 18
        desc_font_size = 40
        max_desc_height = 250
        max_desc_width = 375
        desc_text = ImageText.Text(massage_desc(self.desc, 18), descfont)
        left, top, right, bottom = desc_text.get_bbox()
        width = right - left
        height = bottom - top
        while height > max_desc_height or width < max_desc_width:
            if width < max_desc_width:
                base_max_text += 1
                desc_text = ImageText.Text(massage_desc(self.desc, base_max_text), descfont)
            else:
                desc_font_size -= 1
                descfont = ImageFont.truetype(CARD_PATHS["font_path"], size=desc_font_size)
                desc_text = ImageText.Text(massage_desc(self.desc, 18), descfont)
            left, top, right, bottom = desc_text.get_bbox()
            width = right - left
            height = bottom - top
            
        draw.text((80,650), desc_text, fill='white')
        # HP
        draw.text((600, 760), str(int(self.hp)), font=numfont, fill='green')
        # ATK
        draw.text((600, 610), str(int(self.atk)), font=numfont, fill='red')
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
            buffs : dict,
            pic : Path = None,
    ):
        self.name = name
        self.desc = desc
        self.gtype = gtype
        self.rank = rank
        self.cost = cost
        self.pic = pic
        self._set_buffs(buffs)

    def _set_buffs(self, buffs):
        self.atk_buff = buffs["ATK Buff"]
        self.hp_buff = buffs["HP Buff"]
        self.shield_buff = buffs["Shield Buff"]
        self.armor_buff = buffs["Armor Buff"]
        self.reach_buff = buffs["Reach Buff"]

    def draw(self,):
        # template_pth = Path(CARD_PATHS[f"template_pth"]) / Path(f"gear.png")
        template_pth = Path(CARD_PATHS['template_pth']) / Path("gear.png")
        template = Image.open(template_pth)
        numfont = ImageFont.truetype(CARD_PATHS["font_path"], size=70)
        modfont = ImageFont.truetype(CARD_PATHS["font_path"], size=100)
        namefont = ImageFont.truetype(CARD_PATHS["font_path"], size=45)
        descfont = ImageFont.truetype(CARD_PATHS["font_path"], size=40)

        draw = ImageDraw.Draw(template)
        draw.text((80, 550), self.name, font=namefont, fill='black')
        draw.multiline_text((120, 620), massage_desc(self.desc, 18), font=descfont, fill='white')
        draw.text((625,850), str(int(self.cost)), font=numfont, fill='white')
        # atk_rot = rotate_text("+1", numfont, 270)
        # template.paste(ImageOps.colorize(atk_rot, (0,0,0), (255,255,84)), (475,750),  atk_rot)
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
        # stock_pth = Path("/home/dewdrop/Projects/ccb/round/spell-stock.png")
        # template_pth = Path("/home/dewdrop/Projects/ccb/roundspell.png")
        template = Image.open(template_pth)
        numfont = ImageFont.truetype(CARD_PATHS["font_path"], size=70)
        modfont = ImageFont.truetype(CARD_PATHS["font_path"], size=100)
        namefont = ImageFont.truetype(CARD_PATHS["font_path"], size=45)
        descfont = ImageFont.truetype(CARD_PATHS["font_path"], size=40)

        draw = ImageDraw.Draw(template)
        draw.text((80, 550), self.name, font=namefont, fill='black')
        draw.multiline_text((120,620), massage_desc(self.desc, 18), font=descfont, fill='white')
        draw.text((625,850), str(int(self.cost)), font=numfont, fill='white')
        # if self.pic != None:
        #     ...
        # numfont = ImageFont.truetype(CARD_PATHS["font_path"], size=70)
        # namefont = ImageFont.truetype(CARD_PATHS["font_path"], size=30)
        # descfont = ImageFont.truetype(CARD_PATHS["font_path"], size=25)
        # draw = ImageDraw.Draw(template)
        # draw.text((130, 290), massage_desc(self.name, 15), font=namefont, fill='black')
        # draw.multiline_text((40, 40), massage_desc(self.desc, 20), font=descfont, fill='black')
        # draw.text((50,310), str(int(self.cost)), font=numfont, fill='black')
        return template


def massage_desc(desc, char_len):
    white_space_idx = [i for i, char in enumerate(desc) if char == " "]
    desc_list = [i for i in desc]
    n_lines = 0
    prev_idx = 0
    for idx in white_space_idx:
        if idx+1 > (1 + n_lines) * char_len:
            desc_list[prev_idx] = '\n'
            n_lines += 1
            prev_idx = idx
        elif idx+1 == (1 + n_lines) * char_len:
            desc_list[idx] = '\n'
            n_lines += 1
            prev_idx = idx
        else:
            prev_idx = idx
    print(desc_list)
    return "".join(desc_list)

def rotate_text(text, font, angle, text_dims : tuple = (100, 100)):
    text = ImageText.Text(text, font)
    img = Image.new("L", text_dims)
    draw = ImageDraw.Draw(img)
    draw.text((0,0), text, fill=255)
    atk_rot = img.rotate(angle)
    return atk_rot

# def massage_desc(desc, char_len):
#     new_text = ""
#     i = 0
#     recent_white_space = 0
#     for j, char in enumerate(desc):
#         if i >= char_len:
#             if char == " ":
#                 new_text += char+"\n"
#                 i = 0
#             else:
#                 before = new_text[:recent_white_space]
#                 after = new_text[recent_white_space+1:]
#                 new_text = before + "\n" + after + char
#                 i = len(after) + 1
#         else:
#             if char == " ":
#                 recent_white_space = j
#             new_text += char
#             i += 1
#     return new_text

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
