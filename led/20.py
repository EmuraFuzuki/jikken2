import gpiozero
import time


def main():
    switch = gpiozero.DigitalInputDevice(23, pull_up=False)

    while True:
        if switch.value == 1:
            print("###################")
        else:
            print("...................")
        time.sleep(0.3)


if __name__ == "__main__":
    main()
