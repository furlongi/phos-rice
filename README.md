# hypr-rice-phos

This is a rice setup made for hyprland and Opensuse.

## Requirements:

### sync.py

- Python
- rich

```
sudo zypper in python313 python313-rich
```

### Other Requirements

TODO
This is an incomplete list.

## sync.py

This is a python script to sync the files from the Github repo into the `.conf/` folder.

```
python3 sync.py
```

Arguments:

```
-p, --push      | Set to push mode. (Default is pull mode)
-s, --slow      | Set to slow mode for debugging.
-v, -verbose    | Verbose output for debugging.
--device <name> | Used for device specific confs.
```

Pull mode is when it pulls the `.conf` files into the github repo.
Push mode is when it pushes the github repo to the `.conf` files.

--device is used when this rice is used for multiple devices.
For example, my desktop has three monitors, but my laptop only has one.
So for desktop, it is already defaulted to "desktop".
But for laptop, I pass `--device laptop`.

Within `.conf/`, these device specific files are stored as `custom_device.conf`.
Example: `.conf/hypr/custom_device.conf`.
