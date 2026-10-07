
-- Global Paths
local hypr = "~/.config/hypr"
local hypr_hypr = hypr .. "/hyprland"
local hypr_binds = hypr .. "/binds"
local hypr_plugin = hypr .. "/plugins"
local hypr_scripts = hypr .. "/scripts"
local hypr_layout = hypr .. "/layout"


require(hypr .. "/custom_device")
require(hypr_binds .. "/*")
require(hypr_plugin .. "/*")
require(hypr_layout .. "/*")
require(hypr_hypr .. "/*")


-- Startup
-- https://wiki.hypr.land/0.56.0/Configuring/Basics/Autostart/
hl.on("hyprland.start", function()
    hl.exec_cmd("sudo systemctl start NetworkManager.service")
    hl.exec_cmd("nmcli agent secret")
    hl.exec_cmd("/usr/libexec/kf6/polkit-kde-authentication-agent-1 &")
    hl.exec_cmd("/usr/libexec/pam_kwallet_init")
    hl.exec_cmd("hyprpm reload -n")
    hl.exec_cmd("hyprctl setcursor Adwaita 24")
    -- hl.exec_cmd("ags run")
    hl.exec_cmd("GDK_BACKEND=wayland")
    -- hl.exec_cmd("hypridle")
    -- hl.exec_cmd("hyprpaper")
    hl.exec_cmd("sudo systemctl start docker")
    hl.exec_cmd("mpris-proxy") -- Forward bluetooth media commands to MPRIS
    hl.exec_cmd("noctalia")
end)

-- Plugins

-- For Noctalia Color templates
require("noctalia").apply_theme()
