# hypr-rice: Phos

This is a rice setup made for Hyprland and Fedora.

It is not meant to be plug and play since this is my own custom setup. But I am making it public for anyone to reference and/or copy.

There is an abandoned Opensuse branch that has its own set of instructions.

# Setup

## Applications

Regular applications:

```
sudo dnf install kitty fish wofi dolphin kate chromium fuse-libs wireguard-tools vlc docker-cli docker-compose freerdp qt6ct git pip
```

Set fish as default shell

```
chsh -s $(which fish)
```

Set dolphin as default (if non kde)

```
xdg-mime default org.kde.dolphin.desktop inode/directory
```

RPM Fusion:

```
sudo dnf install https://download1.rpmfusion.org/free/fedora/rpmfusion-free-release-$(rpm -E %fedora).noarch.rpm
sudo dnf install https://download1.rpmfusion.org/nonfree/fedora/rpmfusion-nonfree-release-$(rpm -E %fedora).noarch.rpm
```

External Applications:

```
xdg-open https://obsidian.md/download
```

Brave:

```
sudo dnf install dnf-plugins-core
sudo dnf config-manager addrepo --from-repofile=https://brave-browser-rpm-release.s3.brave.com/brave-browser.repo
sudo dnf install brave-browser
```

VsCodium

```
bash
sudo tee -a /etc/yum.repos.d/vscodium.repo << 'EOF'
[gitlab.com_paulcarroty_vscodium_repo]
name=gitlab.com_paulcarroty_vscodium_repo
baseurl=https://paulcarroty.gitlab.io/vscodium-deb-rpm-repo/rpms/
enabled=1
gpgcheck=1
repo_gpgcheck=1
gpgkey=https://gitlab.com/paulcarroty/vscodium-deb-rpm-repo/raw/master/pub.gpg
metadata_expire=1h
EOF

sudo dnf install codium
```

Librewolf

```
sudo dnf config-manager addrepo --from-repofile=https://repo.librewolf.net/librewolf.repo
sudo dnf install librewolf
```

rEFInd
https://www.rodsbooks.com/refind/

```
sudo dnf in rEFInd
refind-install
```

Remember to add the PARTUUID of /boot in the configs
`/boot/efi/EFI/refind/refind.conf`

There are more applications used that are mapped to keybinds, but the full install list of those applications
are not included right now.

## Hyprland

```
sudo dnf copr enable solopasha/hyprland
sudo dnf install hyprland
sudo dnf install hyprpolkitagent hypridle
```

Hyprpm dependencies:

```
sudo dnf install cmake meson cpio pkg-config git g++ gcc udis86 mesa-libGLU-devel aquamarine-devel hyprlang-devel hyprcursor-devel hyprutils-devel hyprgraphics-devel uuid uuid-devel wayland-devel libxkbcommon-devel wayland-protocols-devel cairo-devel pango-devel libXcursor-devel libinput-devel libdrm-devel mesa-libgbm-devel libuuid-devel hyprwayland-scanner-devel re2-devel xcb-util-errors-devel xcb-util-wm-devel xcb-util-wm-devel tomlplusplus-devel
```

```
hyprpm update
hyprpm add https://github.com/outfoxxed/hy3
hyprpm add https://github.com/hyprwm/hyprland-plugins
hyprpm enable hy3
hyprpm enable hyprexpo
```

### AGS / Astal

https://aylur.github.io/astal/guide/installation

Astal dependencies:

```
sudo dnf install meson vala valadoc gobject-introspection-devel wayland-protocols-devel gtk3-devel gtk-layer-shell-devel gtk4-devel gtk4-layer-shell-devel cmake
```

```
cd /tmp
git clone https://github.com/aylur/astal.git
cd ./astal/lib/astal
```

astal-io / astal3 / astal4

```
cd ./io
meson setup build
meson install -C build
cd ../gtk3
meson setup build
meson install -C build
cd ../gtk4
meson setup build
meson install -C build
```

```
cd /tmp
git clone https://github.com/aylur/ags.git
cd ags
```

AGS dependencies:

```
sudo dnf install npm meson ninja golang gobject-introspection-devel gtk3-devel gtk-layer-shell-devel gtk4-devel gtk4-layer-shell-devel gjs-devel sass json-glib-devel
```

```
npm install
meson setup build
meson install -C build
```

For Hyprland Astal integration:
```
sudo dnf install astal
```


# TODO

- Install sway notification center command
- Enable timeshift
- Improve the astal bar (this will take a while)
    - command center
    - wifi ctl
    - bluetooth ctl
    - vpn ctl
    - theme switcher
    - audio ctl
    - tray
- Customize wofi

### Applications

# sync.py

This is a python script to sync the files from the Github repo into the `.conf/` folder, and vice versa.

This handles specific device configs, like between a desktop to a laptop setup which will be different from each other in minor areas.


```
pip install rich
```


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

This enables Dynamic Power Management, which can bring more stability by adjusting the core clocks. And disables PP_GFXOFF_MASK, the "Dynamic Graphics Engine Power Control" that causes the idle GPU issues.

Investigating these other params. It could be a GPU vram issue:

amdgpu.reset_method=2 amdgpu.noretry=0 pcie_aspm=off

persistence:
amdgpu.reset_method=2

vram:
amdgpu.noretry=0 amdgpu.ppfeaturemask=0xfffffff

bootsplash:
initcall_blacklist=simpledrm_platform_driver_init
