# README:
# What does this script do: Runs the erase_flash, write_flash, flash_id, and copy code to pyboard scripts available in the esptool.py script.
# Notes: The current version of the script hardcodes the PORT, BAUD, FIRMWARE, and location of my custom code. This was done while quickly scripting this script for my own purposes. This is not good practice and will be updated for better maintability in the future as I need it.
# How to use: 1) Using Terminal navigate to the folder where you have your code folder, firmware binary, and your Python3 venv that has the micropython library available. 2) Make sure your ESP32 board is connected via micro usb 3) Run the script using the following command: python3 erase_and_flash_pyboard.py.

import subprocess
import time

separating_line = "__________________________"

# Command to erase everything on the board
erase_board_command = ["esptool.py", "--port", "/dev/tty.usbserial-0001", "erase_flash"]

# Command to write the firmware to the board and run flash_id to make sure the board is working
write_firmware_to_board_command = ["esptool.py", "--chip", "esp32", "--port", "/dev/tty.usbserial-0001", "--baud", "115200", "write_flash", "-z", "0x1000", "ESP32_GENERIC-20240602-v1.23.0.bin"]
flash_board_command = ["esptool.py", "-p", "/dev/tty.usbserial-0001", "flash_id"]

# Commands to connect to the board using rshell and then copying the code to the board
connect_to_board_using_rshell_command = ["rshell", "-p", "/dev/tty.usbserial-0001", "-b", "115200"]
repl_copy_code_to_board_command = ["cp code/* /pyboard"]


def write_separation_message(message):
    print(separating_line)
    print(message)
    print(separating_line)


def run_subprocess(command):
    write_separation_message(f"Running command={command}")

    with subprocess.Popen(command, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as proc:
        for line in proc.stdout:
            print(line, end="")

    time.sleep(5)
    write_separation_message(f"Done running command={command}")
    

def run_repl_subproccess(commands):
    write_separation_message("Starting rshell and running rshell commands")

    with subprocess.Popen(connect_to_board_using_rshell_command, stdin=subprocess.PIPE, stderr=subprocess.PIPE, text=True) as proc:
        for cmd in commands:
            proc.stdin.write(cmd)
            proc.stdin.flush()
            time.sleep(0.5)

        output, error = proc.communicate()
        if output:
            print("REPL Output:")
            print(output)

        if error:
            print("Error:")
            print(error)

    time.sleep(5)
    write_separation_message("Done running rshell commands")


def main():
    run_subprocess(erase_board_command)
    run_subprocess(write_firmware_to_board_command)
    run_subprocess(flash_board_command)
    run_repl_subproccess(repl_copy_code_to_board_command)


if __name__ == '__main__':
    main()
