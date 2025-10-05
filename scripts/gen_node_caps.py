import random
import csv

def generate_random_numbers():
    return random.randint(1 , 10)

def write_to_csv(x):
    with open('cpu & memory.csv', 'w', newline='') as file:
        writer = csv.writer(file, delimiter=' ')
        writer.writerow(["Number", "Column 2", "Column 3"])
        for num in range(x + 1):
            col2 = generate_random_numbers()
            col3 = generate_random_numbers()
            writer.writerow([num, col2, col3])

if __name__ == "__main__":
    try:
        x = int(input("Enter the value of x: "))
        write_to_csv(x)
        print("Data written to random.csv")
    except ValueError:
        print("Please enter a valid integer.")
