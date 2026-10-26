import random
from contestants import Contestant, GroupedContestants

def main():
    cs = GroupedContestants()
    cs.add_random(10)

    while len(cs.get_living()) > 1:
        cs.attack()

    print(f"{cs.get_living()[0].name} survived. They were the only one.")

if __name__ == "__main__":
    main()