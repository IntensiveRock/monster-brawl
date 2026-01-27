import numpy as np

from rich.console import Console
from rich.table import Table


n_adults = 5
n_teens = 7
n_babies = 10
n_monsters = n_adults + n_teens + n_babies
n_spells = 8
card_total = n_monsters + n_spells

adults = ["a" for _ in range(n_adults)]
teens = ["t" for _ in range(n_teens)]
babies = ["b" for _ in range(n_babies)]
spells = ["s" for _ in range(n_spells)]

n_samples = 10000
draw = 5
after_draw = 3
draw_totals = {"a" : 0,
               "t" : 0,
               "b" : 0,
               "s" : 0}

post_totals = {"a" : 0,
               "t" : 0,
               "b" : 0,
               "s" : 0}

for n in range(n_samples):
    deck = adults + teens + babies + spells
    np.random.shuffle(deck)
    for i, char in enumerate(deck[:draw+after_draw]):
        if i <= draw:
            draw_totals[char] += 1
        else:
            post_totals[char] += 1
    
avg_adults = draw_totals["a"] / n_samples
avg_teens = draw_totals["t"] / n_samples
avg_babies = draw_totals["b"] / n_samples
avg_spells = draw_totals["s"] / n_samples

pavg_adults = post_totals["a"] / n_samples
pavg_teens = post_totals["t"] / n_samples
pavg_babies = post_totals["b"] / n_samples
pavg_spells = post_totals["s"] / n_samples

atable = Table(title=f"Deck Card Counts (N={n_samples}, draw={draw})")

atable.add_column("Total Cards", justify="right", style="magenta")
atable.add_column("# of Adults", justify="right", style="red")
atable.add_column("# of Teens", justify="right", style="blue")
atable.add_column("# of Babies", justify="right", style="green")
atable.add_column("# of Spells", justify="right", style="cyan")

atable.add_row(str(card_total), str(n_adults), str(n_teens), str(n_babies), str(n_spells))

table = Table(title=f"Initial Draw Statistics (N={n_samples}, draw={draw})")

table.add_column("AVG # of Adults", justify="right", style="red")
table.add_column("AVG # of Teens", justify="right", style="blue")
table.add_column("AVG # of Babies", justify="right", style="green")
table.add_column("AVG # of Spells", justify="right", style="cyan")

table.add_row(str(avg_adults), str(avg_teens), str(avg_babies), str(avg_spells))

ptable = Table(title=f"After Draw Statistics (N={n_samples}, draw={after_draw})")

ptable.add_column("AVG # of Adults", justify="right", style="red")
ptable.add_column("AVG # of Teens", justify="right", style="blue")
ptable.add_column("AVG # of Babies", justify="right", style="green")
ptable.add_column("AVG # of Spells", justify="right", style="cyan")

ptable.add_row(str(pavg_adults), str(pavg_teens), str(pavg_babies), str(pavg_spells))


console = Console()
console.print(atable)
console.print(table)
console.print(ptable)
