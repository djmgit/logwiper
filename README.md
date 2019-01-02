## Logwiper

### Usage

```
./logwiper.py -n [number_of_directories_to_clean] -d [desired_disk_uage_for_log] -p [path_to_log_dir] -l [time_limits_in_order]

./logwiper.py -h
Usage: logwiper.py [options]

Options:
  -h, --help            show this help message and exit
  -n TOP_DIRS, --top_dirs=TOP_DIRS
                        Max number of dirs occupying most of the disk space to
                        be cleaned, sorted in descending order. Default is 5
  -d DESIRED_DISK_USAGE, --desired_disk_usage=DESIRED_DISK_USAGE
                        Desired disk for rootfs which should not be crosses.
                        Wiping will be trigered it this value is crosses. Give
                        value in percentage. Do not use the '%' symbol.
                        Default is 85.
  -l TIME_LIMITS, --time_limits=TIME_LIMITS
                        List of time limits in days. For eg: '10,5,2'. Script
                        will attemp to wipe out logs in that order. In this
                        case, first 10 days old logs, then 5 days and then 2
                        days. Default is [10,5,2]
  -p LOG_DIR, --log_dir=LOG_DIR
                        path of log dir. Default is /var/log


```

### What the script does

The script first checks whether the disk space occupied by rootfs is greater than the desired value
(passed as -d). If current value is less than the desired value then it does nothing. however, if
it is more, then it finds out what are the directories under the log directory (default /var/log, 
also can be provided with -p) and sorts them according to their size on disk in the descending order.

After that, it selects the **top n** directories and removes log files from withing them which are older
than the number of days list passes with parameter -l. It does so in steps

**Example**

Suppose the time limit list is **[10,5,2]**. Then first the script will remove logs from each of the top
n directories which are older then 10 days, it will then check if the current disk usage of rootfs is
less than the default value. If it is less then the script will exit. If not, the script will repeat the
entire cleaning process with the next value, that is it will try to remove all the logs in the top n
directories which are 5 days old and so on.

If after the entire process, the disk usage still does not go below the desired value, then the script will exit telling reduction not possible.  


