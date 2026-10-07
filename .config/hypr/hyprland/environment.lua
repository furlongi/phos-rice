-- Toolkit backends --
hl.env("AQ_DRM_DEVICES", "/dev/dri/card1")
hl.env("GDK_BACKEND", "wayland,x11,*")
hl.env("QT_QPA_PLATFORM", "wayland;xcb")
hl.env("CLUTTER_BACKEND", "wayland")
hl.env("QT_QPA_PLATFORMTHEME", "qt5ct")

-- hl.env("env = SDL_VIDEODRIVER", "wayland,windows")
-- -- [TRIAGE] Turn this one on if games have compatibility issues
-- -- with Wayland
hl.env("env = SDL_VIDEODRIVER", "x11")


-- XDG specifications --
hl.env("XDG_CURRENT_DESKTOP", "Hyprland")
hl.env("XDG_SESSION_TYPE", "wayland")
hl.env("XDG_SESSION_DESKTOP", "Hyprland")


-- QT Variables --
hl.env("QT_AUTO_SCREEN_SCALE_FACTOR", "1")
hl.env("QT_QPA_PLATFORM", "wayland;xcb")
-- hl.env("QT_WAYLAND_DISABLE_WINDOWDECORATION", "1")
hl.env("QT_QPA_PLATFORMTHEME", "qt5ct")


-- Wayland Fixes --
hl.env("MOZ_ENABLE_WAYLAND", "1")
hl.env("ELECTRON_OZONE_PLATFORM_HINT", "auto")
-- hl.env("AQ_NO_ATOMIC", "1") -- Not recommended


-- https://wiki.hypr.land/0.56.0/Configuring/Basics/Variables/#xwayland
hl.config({
    xwayland = {
        force_zero_scaling = true
    }
})

-- https://wiki.hypr.land/0.56.0/Configuring/Basics/Variables/#ecosystem
hl.config({
    ecosystem = {
        no_update_news = false,
        no_donation_nag = true, -- I will donate when I can *empty wallet gif*
        enforce_permissions = false,
    }
})
