#!/data/data/com.termux/files/usr/bin/bash

LICENSE_FILE="$HOME/.dark_key"
SERVER="https://darknet.gamer.gd/check"

if [ ! -f "$LICENSE_FILE" ]; then
read -p "License Key: " k
echo "$k" > $LICENSE_FILE
fi

k=$(cat $LICENSE_FILE)
res=$(curl -s "$SERVER?key=$k")

if [[ "$res" == *"valid"* ]]; then
echo "✅ License aktif"
elif [[ "$res" == *"expired"* ]]; then
echo "⏳ License expired"
rm -f $LICENSE_FILE
exit
else
echo "❌ License invalid"
rm -f $LICENSE_FILE
exit
fi

sleep 1

while true; do
echo "[1] Play"
echo "[2] MP3"
echo "[0] Exit"

read -p ">> " p

case $p in
1) read -p "URL: " u; yt-dlp -o - "$u" | mpv - ;;
2) read -p "URL: " u; yt-dlp -x --audio-format mp3 "$u" ;;
0) exit ;;
*) echo "error" ;;
esac

done
