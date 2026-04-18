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
        # template_pth = Path(CARD_PATHS[f"template_pth"]) / Path(f"{self.mtype}-{self.rank}.png")
        round_pth = Path("/home/dewdrop/Projects/ccb/round/")
        temp_outline_pth = round_pth / Path(f"round-outline.png")
        temp_stock_pth = round_pth / Path("round-stockimage.png")
        temp_type_pth = round_pth / Path(f"round-{self.mtype}.png")
        temp_level_pth = round_pth / Path(f"round-{self.rank}.png")
        temp_speed_pth = round_pth / Path(f"speed-{self.speed}.png")

        template = Image.open(temp_stock_pth)
        outline = Image.open(temp_outline_pth)
        mtype = Image.open(temp_type_pth)
        level = Image.open(temp_level_pth)
        speed = Image.open(temp_speed_pth)

        template.paste(outline, (0,0), outline)
        template.paste(mtype, (0,0), mtype)
        template.paste(level, (0,0), level)
        template.paste(speed, (0,0), speed)        

        numfont = ImageFont.truetype(CARD_PATHS["font_path"], size=80)
        namefont = ImageFont.truetype(CARD_PATHS["font_path"], size=40)
        descfont = ImageFont.truetype(CARD_PATHS["font_path"], size=40)
        
        # draw = ImageDraw.Draw(template)
        # numfont = ImageFont.truetype("/usr/share/fonts/TTF/GohuFont14NerdFont-Regular.ttf", size=100)
        # namefont = ImageFont.truetype("/usr/share/fonts/TTF/GohuFont14NerdFont-Regular.ttf", size=40)
        # descfont = ImageFont.truetype("/usr/share/fonts/TTF/GohuFont14NerdFont-Regular.ttf", size=40)
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
            
        
        draw = ImageDraw.Draw(template)
        
        
        #template.paste(seedling, (0,0), seedling)
        #Name
        # draw.text((90, 45), self.name, font=namefont, fill='white', stroke_width=1)
        draw.text((90, 45), name_text, fill='black')
        #draw_underlined_text(draw, (50, 150), mon.name, font=namefont, fill='black')
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
            
        draw.text((40,610), desc_text, fill='black')
        # draw.multiline_text((40,610), massage_desc(self.desc, 18), font=descfont, fill='black')
        
        # Rank
        #draw.text((80, 470), mon.rank[0], font=font, fill='black')
        # HP
        draw.text((530, 760), str(int(self.hp)), font=numfont, fill='green')
        # ATK
        draw.text((530, 610), str(int(self.atk)), font=numfont, fill='red')
        # if self.pic != None:
        #     ...
        # if self.speed != None:
        #     draw.text((200, 380), str(int(self.speed)), font=numfont, fill='yellow')
        # draw.text((105, 290), massage_desc(self.name, 15), font=namefont, fill='black')
        # draw.multiline_text((40, 40), massage_desc(self.desc, 23), font=descfont, fill='black')
        # draw.text((40, 290), str(int(self.hp)), font=numfont, fill='green')
        # draw.text((40, 380), str(int(self.atk)), font=numfont, fill='red')
        # draw.text((200, 380), str(int(self.speed)), font=numfont, fill='yellow')
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
        stock_pth = Path("/home/dewdrop/Projects/ccb/round/gear-stock.png")
        template_pth = Path("/home/dewdrop/Projects/ccb/roundgear.png")
        template = Image.open(stock_pth)
        outline = Image.open(template_pth)
        template.paste(outline, (0,0), outline)
        numfont = ImageFont.truetype(CARD_PATHS["font_path"], size=70)
        modfont = ImageFont.truetype(CARD_PATHS["font_path"], size=100)
        namefont = ImageFont.truetype(CARD_PATHS["font_path"], size=45)
        descfont = ImageFont.truetype(CARD_PATHS["font_path"], size=30)

        draw = ImageDraw.Draw(template)
        draw.text((40, 55), self.name, font=namefont, fill='black')
        draw.multiline_text((40, 500), massage_desc(self.desc, 18), font=descfont, fill='black')
        draw.text((525,42), str(int(self.cost)), font=numfont, fill='black')
        atk_rot = rotate_text("+1", numfont, 270)
        template.paste(ImageOps.colorize(atk_rot, (0,0,0), (255,255,84)), (475,750),  atk_rot)
        # draw.text((525, 700), atk_text, fill='black')
        
        # if self.pic != None:
        #     ...
        # numfont = ImageFont.truetype(CARD_PATHS["font_path"], size=70)
        # namefont = ImageFont.truetype(CARD_PATHS["font_path"], size=30)
        # descfont = ImageFont.truetype(CARD_PATHS["font_path"], size=22)

        # draw = ImageDraw.Draw(template)
        # draw.text((40, 40), self.name, font=namefont, fill='black')
        # draw.multiline_text((85, 290), massage_desc(self.desc, 18), font=descfont, fill='black')
        # draw.text((185,450), str(int(self.cost)), font=numfont, fill='black')
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
        # template_pth = Path(CARD_PATHS[f"template_pth"]) / Path(f"spell.png")
        stock_pth = Path("/home/dewdrop/Projects/ccb/round/spell-stock.png")
        template_pth = Path("/home/dewdrop/Projects/ccb/roundspell.png")
        template = Image.open(stock_pth)
        outline = Image.open(template_pth)
        template.paste(outline, (0,0), outline)
        numfont = ImageFont.truetype(CARD_PATHS["font_path"], size=70)
        modfont = ImageFont.truetype(CARD_PATHS["font_path"], size=100)
        namefont = ImageFont.truetype(CARD_PATHS["font_path"], size=45)
        descfont = ImageFont.truetype(CARD_PATHS["font_path"], size=30)

        draw = ImageDraw.Draw(template)
        draw.text((40, 55), self.name, font=namefont, fill='black')
        draw.multiline_text((40,610), massage_desc(self.desc, 18), font=descfont, fill='black')
        draw.text((525,42), str(int(self.cost)), font=numfont, fill='black')
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
