#!/usr/bin/env bash

godotEditorTitle="^((.*)- Godot Engine)"
godotDebugTitle="^((.*) \(DEBUG\))"

function handle {
    echo "1 ${1}"
    echo "2 ${1:15:7}"
    case $1 in
        windowtitlev2*)
            if [[ ${1:23} =~ $godotEditorTitle ]]; then
                echo "success"
                hyprctl dispatch settiled $window
                #   hyprctl dispatch resizewindowpixel exact 300 1080,$window
                #   hyprctl dispatch movewindowpixel exact 2048 72,$window
            fi

            
            
            ;;
    esac


#   if [[ ${1:0:13} == "windowtitlev2" ]]; then
#     window=address:0x${1:15:12}
#     if [[ ${1:23} =~ $godotEditorTitle ]]; then
#       echo "success"
#       hyprctl dispatch settiled $window
#     #   hyprctl dispatch resizewindowpixel exact 300 1080,$window
#     #   hyprctl dispatch movewindowpixel exact 2048 72,$window
#     fi
#   fi
}

socat - "UNIX-CONNECT:$XDG_RUNTIME_DIR/hypr/$HYPRLAND_INSTANCE_SIGNATURE/.socket2.sock" | while read -r line; do handle "$line"; done