import matplotlib.pyplot as plt

# Reading numbers from a file into a list
with open("number_list_2.txt", "r") as fin:
    text_list = fin.readlines()

number_list = [float(text_item) for text_item in text_list]
print(number_list)

# Finding Min and Max values
min_value = min(number_list)
max_value = max(number_list)

# Mean Value
mean_value = sum(number_list)/len(number_list)

print(min_value, max_value, mean_value)

# Mod using Histogram

# Defining the min, max, and step
max_value = 40
min_value = 10
step = 5

# Calculating the number of bins for the histogram
num_bins = int((max_value-min_value) // step)  # Gives the number of bins for the given min, max, and step
bins = [0 for i in range(num_bins + 1)]  # + 1 to include the max value

# Tally the data
for value in sorted(number_list):
    if min_value <= value <= max_value:
        # This will give us which bin the value belongs to
        bin_index = int(value - min_value) // step
        # Increment the count
        bins[bin_index] += 1

# Print Results
for i, bin in enumerate(bins):
    print("Bin:", min_value + step * i, min_value + step * i + step, "Value:", bin)

plt.hist(number_list, bins=num_bins)
plt.show()
