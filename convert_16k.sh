mkdir -p converted
for i in "$1"/*.wav; do
    o=converted/${i#"$1"/}
    sox "$i" -r 16000 -c 1 "${o%}"
done
