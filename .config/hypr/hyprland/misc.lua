-- https://wiki.hypr.land/0.56.0/Configuring/Basics/Variables/#misc
hl.config({
    misc = {
        disable_hyprland_logo = true, -- :(
        disable_splash_rendering = false,
        col = {
            splash = "0xffffffff"
        },

        disable_scale_notification = false,

        font_family = "Sans",
        splash_font_family = "",
        force_default_wallpaper = 0,
        
        vrr = 0,

        mouse_move_enables_dpms = false,
        key_press_enables_dpms = true,
        layers_hog_keyboard_focus = true,

        animate_manual_resizes = false,
        animate_mouse_windowdragging = false,

        disable_autoreload = false,

        enable_swallow = false,
        swallow_regex = "^(kitty)$",
        swallow_exception_regex= "",

        focus_on_activate = false,
        mouse_move_focuses_monitor = true,
        
        allow_session_lock_restore = true,

        initial_workspace_tracking = 1,
        middle_click_paste = false, -- Doesnt affect it :(
        render_unfocused_fps = 15,
    },

    debug = {
        error_position = 1
    }
})