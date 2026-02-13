import copy
import numpy as np

from rich.console import Console
from rich.table import Table

max_cards = 40

# composition_dict = {
#     "Red" : {
#         "LVL1" : 8,
#         "LVL2" : 6,
#         "LVL3" : 5,
#     },
#     "Black" : {
#         "LVL1" : 8,
#         "LVL2" : 6,
#         "LVL3" : 5,
#     },
# }

composition_dict = {
    "Red" : {
        "LVL1" : 12,
        "LVL2" : 9,
        "LVL3" : 9,
    },
}

n_colors = 0
for key in composition_dict:
    n_colors += 1

deck = []
n_monsters = 0
draw_totals = {'Spells' : {'s' : 0}}

for color_key in composition_dict.keys():
    color_dict = composition_dict[color_key]
    draw_totals[color_key] = {}
    for level_key in color_dict:
        n_monsters += color_dict[level_key]
        draw_totals[color_key][level_key] = 0
        for n in range(color_dict[level_key]):
            deck.append([color_key,level_key])
        

n_spells = max_cards - n_monsters
composition_dict["Spells"] = {"s" : n_spells}
deck += [["Spells", "s"] for _ in range(n_spells)]
assert len(deck) <= max_cards, "You broke the rules!!!"

post_totals = copy.deepcopy(draw_totals)

n_samples = 10000
draw = 5
after_draw = 3

for n in range(n_samples):
    np.random.shuffle(deck)
    for i, char in enumerate(deck[:draw+after_draw]):
        if i <= draw:
            draw_totals[char[0]][char[1]] += 1
        else:
            post_totals[char[0]][char[1]] += 1

avg_draws = {color_key : {key : draw_totals[color_key][key] / n_samples for key in draw_totals[color_key].keys()} for color_key in draw_totals.keys()}
pavg_draws = {color_key : {key : post_totals[color_key][key] / n_samples for key in post_totals[color_key].keys()} for color_key in post_totals.keys()}


table_list = []
for color_key in avg_draws.keys():
    atable = Table(title=f"Deck Card Counts (color={color_key}, N={n_samples}, draw={draw})")
    color_dict = avg_draws[color_key]
    row_strings = []
    for key in color_dict.keys():
        atable.add_column(f"Total {key}", justify="right", style="magenta")
        atable.add_column(f"AVG {key}", justify="right", style="magenta")
        row_strings += [str(composition_dict[color_key][key])]
        row_strings += [str(color_dict[key])]
    atable.add_row(*row_strings)
    table_list.append(atable)
        # atable.add_column("# of LVL3", justify="right", style="red")
        # atable.add_column("# of LVL2", justify="right", style="blue")
        # atable.add_column("# of LVL1", justify="right", style="green")
        # atable.add_column("# of Spells", justify="right", style="cyan")x # 

    # atable.add_row(str(card_total), str(n_adults), str(n_teens), str(n_babies), str(n_spells))


    # table = Table(title=f"Initial Draw Statistics (N={n_samples}, draw={draw})")

    # table.add_column("AVG # of Adults", justify="right", style="red")
    # table.add_column("AVG # of Teens", justify="right", style="blue")
    # table.add_column("AVG # of Babies", justify="right", style="green")
    # table.add_column("AVG # of Spells", justify="right", style="cyan")

    # table.add_row(str(avg_adults), str(avg_teens), str(avg_babies), str(avg_spells))

# ptable = Table(title=f"After Draw Statistics (N={n_samples}, draw={after_draw})")

# ptable.add_column("AVG # of Adults", justify="right", style="red")
# ptable.add_column("AVG # of Teens", justify="right", style="blue")
# ptable.add_column("AVG # of Babies", justify="right", style="green")
# ptable.add_column("AVG # of Spells", justify="right", style="cyan")

# ptable.add_row(str(pavg_adults), str(pavg_teens), str(pavg_babies), str(pavg_spells))


console = Console()
for tb in table_list:
    console.print(tb)
# console.print(atable)
# console.print(table)
# console.print(ptable)
