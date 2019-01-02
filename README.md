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


