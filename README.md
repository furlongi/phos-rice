# hypr-rice: Phos

This is a rice setup made for hyprland and Opensuse.

# Setup:

## **sync.py (optional)**

This is a script to push and pull these dot files with the github folder and `~/.config`. More info at the bottom.

- Python
- rich

```
sudo zypper in python313 python313-rich
```

### Hyprland

Can be installed via zypper. But Opensuse does not include hyprpm due to a bug https://bugzilla.opensuse.org/show_bug.cgi?id=1218422.

Plugins would need to be built and installed manually.

To build Hyprland:
https://wiki.hypr.land/Getting-Started/Installation/#manual

```
zypper in gcc-c++ git meson cmake "pkgconfig(cairo)" "pkgconfig(egl)" "pkgconfig(gbm)" "pkgconfig(gl)" "pkgconfig(glesv2)" "pkgconfig(libdrm)" "pkgconfig(libinput)" "pkgconfig(libseat)" "pkgconfig(libudev)" "pkgconfig(pango)" "pkgconfig(pangocairo)" "pkgconfig(pixman-1)" "pkgconfig(vulkan)" "pkgconfig(wayland-client)" "pkgconfig(wayland-protocols)" "pkgconfig(wayland-scanner)" "pkgconfig(wayland-server)" "pkgconfig(xcb)" "pkgconfig(xcb-icccm)" "pkgconfig(xcb-renderutil)" "pkgconfig(xkbcommon)" "pkgconfig(xwayland)" "pkgconfig(xcb-errors)" glslang-devel Mesa-libGLESv3-devel tomlplusplus-devel
```

(may be incomplete)

```
sudo zypper in re2-devel muparser-devel hyprwire-devel hyprland-protocols-devel glaze-devel pugixml-devel
```

Building will fail because Hyprland relies on `glaze-devel` at version ~3, but Opensuse installs verion ~4.
To resolve the build failures:

- Replace instances of `<glz::generic>` with `<glz::json_t>`.

Especially for `/start/src/helpers/Nix.cpp`.

```
git clone --recursive https://github.com/hyprwm/Hyprland
cd Hyprland
make all
```

```
sudo make install
```

## **Plugins**

- Hy3 - https://github.com/outfoxxed/hy3
- Hyprland-Plugins - https://github.com/hyprwm/hyprland-plugins
  - hyprexpo

```
hyprpm update
hyprpm add https://github.com/outfoxxed/hy3
hyprpm add https://github.com/hyprwm/hyprland-plugins

hyprpm enable hy3
hyprpm enable hyprexpo
```

## **Dependencies**

TODO - This is an incomplete list.

```
sudo zypper ref
```

### Desktop / Rice

```
sudo zypper in kitty fish wofi dolphin SwayNotificationCenter
```

### Applications

```
sudo zypper in discord
```

- https://obsidian.md/download
- https://librewolf.net/installation/opensuse/
- https://brave.com/linux/#opensuse
- https://floorp.app/download (or flatpak)

# sync.py

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

`--device` is used when this rice is used for multiple devices.

For example, my desktop has three monitors, but my laptop only has one.

So for desktop, it is already defaulted to "desktop".
But for laptop, I pass `--device laptop`.

Within `.conf/`, these device specific files are stored as `custom_device.conf`.
Example: `.conf/hypr/custom_device.conf`.
