from load_contracts import read_contract, preprocess_text
import argparse

def add_trigger(trigger, filename):
    cur_tiggers = get_raw_triggers(filename)
    if trigger in cur_tiggers:
        print("trigger already exists")
    else:
        with open("./triggers/" + filename, "a") as f:
            f.write("%s\n" % trigger)

def get_raw_triggers(filename):
    f = open("./triggers/" + filename, "r")
    triggers = [x.strip("\n") for x in f]
    return triggers

def get_proccessed_triggers(filename):
    triggers = get_raw_triggers(filename)
    triggers = [preprocess_text(trigger) for trigger in triggers]
    triggers = [trigger.split(" ") for trigger in triggers]
    return triggers


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Add triggers')
    parser.add_argument('filename', metavar='f', type=str, nargs='+',
                        help='file of trigger file')
    args = parser.parse_args()
    filename = args.filename[0]
    while True:
        trigger = input("Enter trigger: ")
        if trigger == "q":
            break
        add_trigger(trigger, filename)
        print("added trigger to", filename)