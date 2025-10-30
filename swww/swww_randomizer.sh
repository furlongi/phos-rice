RESIZE_TYPE="fit"
DEFAULT_DIRECTORY="/home/ivan/Pictures/desktop/"

# if [ $# -lt 1 ] || [ ! -d "$1" ]; then
# 	printf "Usage:\n\t\e[1m%s\e[0m \e[4mDIRECTORY\e[0m [\e[4mINTERVAL\e[0m]\n" "$0"
# 	printf "\tChanges the wallpaper to a randomly chosen image in DIRECTORY every\n\tINTERVAL seconds (or every %d seconds if unspecified)." "$DEFAULT_INTERVAL"
# 	exit 1
# fi

find $DEFAULT_DIRECTORY -type f \
| while read -r img; do
    echo "$(</dev/urandom tr -dc a-zA-Z0-9 | head -c 8):$img"
done \
| sort -n | cut -d':' -f2- \
| while read -r img; do
    echo $img
    # swww img --resize="$RESIZE_TYPE" "$img" -o "DP-1"
    swww img "$img" -o "DP-1" --transition-type left --transition-step 2 --transition-fps 60
    break
done

