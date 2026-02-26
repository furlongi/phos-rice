# hypr-rice: Phos

This is a rice setup made for hyprland and Opensuse.

It is not meant to be plug and play since this is my own custom setup. But I am making it public for anyone to reference and/or copy.

# Setup:

## **sync.py (optional)**

This is a script to push and pull these dot files between the github folder and `~/.config`. More info at the bottom. This is made for changing device specific dotfiles between for example a desktop setup and laptop setup.

Requirements:
- Python
- rich

```
sudo zypper in python313 python313-rich
```

## Hyprland

Can be installed via zypper. But Opensuse does not include hyprpm due to a bug https://bugzilla.opensuse.org/show_bug.cgi?id=1218422.

Plugins would need to be built and installed manually.

To build Hyprland:
https://wiki.hypr.land/Getting-Started/Installation/#manual

Install the documented requirements:
```
sudo zypper in gcc-c++ git meson cmake "pkgconfig(cairo)" "pkgconfig(egl)" "pkgconfig(gbm)" "pkgconfig(gl)" "pkgconfig(glesv2)" "pkgconfig(libdrm)" "pkgconfig(libinput)" "pkgconfig(libseat)" "pkgconfig(libudev)" "pkgconfig(pango)" "pkgconfig(pangocairo)" "pkgconfig(pixman-1)" "pkgconfig(vulkan)" "pkgconfig(wayland-client)" "pkgconfig(wayland-protocols)" "pkgconfig(wayland-scanner)" "pkgconfig(wayland-server)" "pkgconfig(xcb)" "pkgconfig(xcb-icccm)" "pkgconfig(xcb-renderutil)" "pkgconfig(xkbcommon)" "pkgconfig(xwayland)" "pkgconfig(xcb-errors)" glslang-devel Mesa-libGLESv3-devel tomlplusplus-devel
```

Install additional libraries for build to pass (may be incomplete):
```
sudo zypper in re2-devel muparser-devel hyprwire-devel hyprland-protocols-devel glaze-devel pugixml-devel
```

Download the repository. I recommend in the `/tmp` folder.
```
cd /tmp
git clone --recursive https://github.com/hyprwm/Hyprland
cd Hyprland
```

Building will fail because Hyprland relies on `glaze-devel` at version ~3, but Opensuse installs verion ~4.
To resolve the build failures:

- Replace instances of `<glz::generic>` with `<glz::json_t>`.

Especially for `/start/src/helpers/Nix.cpp`.

Then build:

```
make all
```

```
sudo make install
```

## Quickshell
Quickshell is not available as a package in Opensuse.
https://git.outfoxxed.me/quickshell/quickshell/src/branch/master/BUILD.md

```
sudo zypper in cmake qt6-base-devel qt6-declarative-devel qt6-declarative-private-devel qt6-shadertools-devel spirv-tools-devel pkgconf cli11-devel qt6-wayland-devel qt6-wayland-private-devel qt6-waylandclient-private-devel libpolkit-qt6-1-devel jemalloc-devel jemalloc qt6-svg-devel
```

Opensuse does not have a breakpad library available, so disable crash reporter.
```
cmake -GNinja -B build -DCMAKE_BUILD_TYPE=RelWithDebInfo -DCRASH_REPORTER=OFF -DCMAKE_C_FLAGS="-I/usr/include/wayland" -DCMAKE_CXX_FLAGS="-I/usr/include/wayland"
```

```
cmake --build build
```

```
sudo cmake --install build
```

## AGS / Astal

https://aylur.github.io/astal/guide/installation

Astal dependencies:
```
sudo zypper install meson vala vala-cmake-modules valadoc gobject-introspection-devel wayland-protocols-devel gtk3-devel gtk-layer-shell-devel gtk4-devel gtk4-layer-shell-devel libvaladoc-0_56-devel valadoc-doclet-devhelp valadoc-doclet-gtkdoc valadoc-doclet-html
``` 

Astal IO
Due to a `graphviz` package, building will fail. Edit the `meson.build` with these edits:
https://github.com/Aylur/astal/issues/372

```
cd lib/astal/io
meson setup build
meson install -C build
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
Although right now it does not handle deleted files.

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

# Fixes
## Steam
Steam for some reason either:
- Will not launch under wayland due to steamwebhelper infinitely looping on failure
- Cannot be killed. Will restart itself due to thinking it crashed on error

To resolve the first:
```
env = SDL_VIDEODRIVER, x11
```

To resolve the second:
Turn off GPU acceleration in steam settings.

You can probably force steam to run with the above issues by doing `STEAM_RUNTIME=0 steam`.

Hyprland's [solution](https://wiki.hypr.land/Configuring/Uncommon-tips--tricks/#minimize-steam-instead-of-killing) does work, but `windowunmap` will unmap Steam from initializing again under wayland due to lost mapping (from what I understand), so its PID needs to be stored ahead of time to know how it will be unmapped. But that is extra work.

## Discord
Discord will not close correctly and crash when trying to kill it and produce memory leaks.
Also screen recording will not work under wayland.

Add the following launch option:
```
--enable-features=UseOzonePlatform --ozone-platform=wayland
```
Can either be done to the keybind or in the `.desktop` typically found `/usr/share/applications/discord.desktop`

## AMD GPU - Crash After Suspend
(potential solution)

When using high frame rate monitors with high display port version, it is possible to get this error due to timing of communication between the GPU and waking monitor:
```
kernel: [drm:retrieve_link_cap [amdgpu]] *ERROR* retrieve_link_cap: Read receiver caps dpcd data failed
```
It is also possible that on an idle GPU, Hyprland randomly crashes and reboots.

Current fix is to add this to the grub/refind or other boot loader kernel parameter arguments:
```
amdgpu.dpm=1 amdgpu.ppfeaturemask=0xf7fff
```
This enables Dynamic Power Management, which can bring more stability by adjusting the core clocks. And disables PP_GFXOFF_MASK, the  "Dynamic Graphics Engine Power Control" that causes the idle GPU issues.

Investigating these other params. It could be a GPU vram issue:

amdgpu.reset_method=2 amdgpu.noretry=0 pcie_aspm=off

persistence:
amdgpu.reset_method=2

vram:
amdgpu.noretry=0 amdgpu.ppfeaturemask=0xfffffff

bootsplash:
initcall_blacklist=simpledrm_platform_driver_init