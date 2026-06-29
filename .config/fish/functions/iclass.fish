function iclass
 xprop | grep WM_CLASS | awk '{ print $4 }'
end
