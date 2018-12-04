from topk import TopK
from random import randint
from collections import Counter

for _ in range(10000):
    upper = randint(0, 1)
    size = randint(0, 500)

    xs = [randint(0, upper) for _ in range(randint(0, size))]
    ys = [randint(0, 1) for _ in range(len(xs))]

    top = TopK()
    cou = Counter()
    for i, (x, y) in enumerate(zip(xs, ys)):
        op = 'inc' if y == 0 else 'dec'
        if y == 0:
            top.inc(x)
            cou.update([x])
        else:
            top.dec(x)
            if x in cou: cou.subtract([x])
            if cou[x] == 0: del cou[x]

        if cou != top.counts():
            items = [x[0] for x in reversed(sorted(cou.items(), key=lambda x: x[1]))]
            print(i, xs, ys, top.ordered, items, cou, top.counts())
            break

        for (a, b) in zip(top.ordered, top.ordered[1:]):
            if top.keys[a][1] < top.keys[b][1]:
                print("> ", xs, top.ordered)
                break
