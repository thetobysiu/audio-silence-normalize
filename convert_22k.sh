mkdir -p converted/"$1"/
for i in "$1"/*.wav; do
    o=converted/"$1"/${i#"$1"/}
    sox "$i" -r 22050 -c 1 "${o%}"
done
