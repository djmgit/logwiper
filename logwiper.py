#! /usr/bin/python3

import subprocess
import optparse

LOG_PATH = "/var/log"
TOP_N = 5
ORDER = [100, 50]
DESIRED = 85

def execute(command):
	proc = subprocess.Popen(command, shell=True, stdout=subprocess.PIPE)
	response = proc.communicate()
	exit_val = proc.returncode

	if exit_val != 0:
		exit(exit_val)

	data = response[0].decode()

	return data

def get_dirs():
    dirs = execute("sudo du /var/log -d 1 | sort -n -r | awk '{print $2}'")
    list_dirs = dirs.split("\n")[1:-1]

    # select only the top n directories
    list_dirs = list_dirs[0: TOP_N]

    return list_dirs

def clean_dirs(time_limit):
	dirs = get_dirs()

	# enter each directory and clean
	for cdir in dirs:
		print ("cleaning {}".format(cdir))
		command = "sudo find {}/ -type f -mtime {} -delete".format(cdir, time_limit)
		print (command)
		response = execute(command)

def get_log_status():
	command = "df -Th | awk '{print $6,$7}' | grep -E '/$'"
	response = execute(command)
	# get the size corresponding to rootfs
	root_size = int(response.split()[0].strip("%"))
	return root_size

def run_clean():
	# run for all the limits in ORDER list
	for limit in ORDER:
		# clean dirs for each limit
		clean_dirs(limit)
		# check for status after each clean
		status = get_log_status()
		# if usage is below desired, then end process
		if status < DESIRED:
			break

	return get_log_status


if __name__ == "__main__":
	pass


