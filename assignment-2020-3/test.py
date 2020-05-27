import random

random.seed(42)


for i in range(50):
    print("counter:", i + 1, "number", random.randint(5, 10))