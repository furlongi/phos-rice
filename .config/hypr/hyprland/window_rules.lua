-- https://wiki.hypr.land/0.56.0/Configuring/Basics/Window-Rules/#window-rules
hl.window_rule({
  name = "tile-kitty",
  match = {
    class = "^(kitty)$"
  },
  tile = true
})

hl.window_rule({
  name = "tile-godot",
  match = {
    initial_title = "^(Godot Engine)$",
  },
  tile = false,
  float = false
})

hl.window_rule({
  name = "inhibit-idle",
  match = {
    fullscreen = true
  },
  idle_inhibit = "always"
})
