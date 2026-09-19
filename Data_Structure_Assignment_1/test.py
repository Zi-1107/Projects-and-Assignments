def ex31():
    while True:
        name = input("Enter name (-1 to quit): ")
        if name == "-1":
            break
        age = int(input("Enter age: "))
        w = int(input("Enter weight (kg): "))
        h = int(input("Enter height (cm): "))

        ava = []
        tab = {
            "haunted house": [17, (0, 500), (0, 500)],
            "roller coaster": [18, (40, 70), (-140, 500)],
            "ferris wheel": [13, (40, 60), (0, 500)],
            "carousels": [14, (0, 75), (0, 170)],
            "water rides": [10, (0, 80), (-145, 500)],
            "bumpy cars": [0, (0, 500), (-140, 170)]

        }
        for k, v in tab.items():
            if age >= v[0]:
                if v[1][0] <= w & w <= v[1][1]:
                    if 0 <= (h + v[2][0]) and (h + v[2][1]) <= (2 * v[2][1]):
                        ava.append(k)
        
        print(f"Hi {name}, you can visit the following facilities: ")
        for i in ava:
            print(f"> {i}")
        print("\n")

def ex32():
    n = int(input("Enter n: "))
    for i in range(n, 1, -1):
        print(" " * (n-i), end="")
        print("@" * abs(i-n), end="")
        print("*" * abs(i-n), end="")
        print(" " * (n-i), end="\n")

ex32()