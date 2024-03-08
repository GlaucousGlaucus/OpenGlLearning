import random

file_data = "\n".join(f"{random.randint(10, 40)}" for x in range(10))

with open("number_list_2.txt", "w") as f:
    f.write(file_data)
