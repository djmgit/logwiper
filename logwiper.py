#! /usr/bin/python

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
    dirs = execute("sudo du {0} -d 1 | sort -n -r | awk '{print $2}'".format(LOG_PATH))
    list_dirs = dirs.split("\n")[1:-1]

    # select only the top n directories
    list_dirs = list_dirs[0: TOP_N]

    return list_dirs

def clean_dirs(time_limit):
	dirs = get_dirs()

	# enter each directory and clean
	for cdir in dirs:
		print ("cleaning {}".format(cdir))
		#command = "sudo find {}/ -type f -mtime {} -delete".format(cdir, time_limit)
		command = "sudo find {}/ -type f -delete".format(cdir)
		print (command)
		response = execute(command)

def get_log_status():
	command = "df -Th | awk '{print $6,$7}' | grep -E '/$'"
	response = execute(command)
	# get the usage corresponding to rootfs
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

	return get_log_status()


if __name__ == "__main__":
	parser = optparse.OptionParser()
	parser.add_option('-n', '--top_dirs', dest="top_dirs", help="Max number of dirs occupying most of the disk space to be cleaned, sorted in descending order. Default is 5")
	parser.add_option('-d', '--desired_disk_usage', dest='desired_disk_usage', help="Desired disk for rootfs which should not be crosses. Wiping will be trigered it this value is crosses. Give value in percentage. Do not use the '%' symbol. Default is 85.")
	parser.add_option('-l', '--time_limits', dest="time_limits", help="List of time limits in days. For eg: '10,5,2'. Script will attemp to wipe out logs in that order. In this case, first 10 days old logs, then 5 days and then 2 days. Default is [10,5,2]")
	parser.add_option('-p', '--log_dir', dest="log_dir", help="path of log dir. Default is /var/log")

	option, args = parser.parse_args()

	if option.top_dirs:
		TOP_N = int(option.top_dirs)
	if option.desired_disk_usage:
		DESIRED = int(option.desired_disk_usage)
	if option.log_dir:
		LOG_PATH = option.log_dir
	if option.time_limits:
		ORDER = [int(limit.strip()) for limit in option.time_limits.split(",")]

	print (TOP_N)
	print (DESIRED)
	print (LOG_PATH)
	print (ORDER)

	status = get_log_status()
	print (status, DESIRED)
	after_cleanup = ""

	if status > DESIRED:
		#try:
		after_cleanup = run_clean()
		#except:
			#print ('Cannot clean logs. Faced exception.')
			#exit(0)

		if after_cleanup > DESIRED:
			print ("Cleaned logs but could reduce much.")
		else:
			print ("Cleaned logs, reduced below desired usage.")
	else:
		print ("Cleaning not required")

	exit(0)
