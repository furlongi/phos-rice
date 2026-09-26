function hyprlockrestart --description 'Restarts a crashed hyprlock'
  killall -9 hyprlock
  sleep 0.5
  hyprctl --instance 0 'keyword misc:allow_session_lock_restore 1'
  sleep 0.5
  hyprctl --instance 0 'dispatch exec hyprlock'
  sleep 0.5
end
