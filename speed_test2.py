from time import time

fruit  = range(4_000_000)

tic = time()
res = [True if i % 2 == 0 else False for i in fruit]
toc = time()
print(toc - tic)


tic = time()
list(map(lambda s: s % 2 == 0, fruit))
toc = time()
print(toc - tic)

tic = time()
res = []
for i in fruit:
    if i % 2 == 0:
        res.append(True)
    else:
        res.append(False)
toc = time()
print(toc - tic)