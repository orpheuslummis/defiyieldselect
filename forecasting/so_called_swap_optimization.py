import itertools

# here are some possible pairs of Price % and APR %
possibilities = [(x,y) for x,y in itertools.product(range(-100,100+1), range(-100,100+1))]
# [print(f"price {x}, apr {y}") for x,y in possibilities]
# print(len(possibilities))

# we want our algorithm to perform well in all of these cases