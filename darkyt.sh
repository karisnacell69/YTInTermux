#!/data/data/com.termux/files/usr/bin/bash

g="\033[1;32m"; r="\033[1;31m"; c="\033[1;36m"; w="\033[1;37m"

center() {
    termwidth=$(tput cols)
    padding=$(( (termwidth - ${#1}) / 2 ))
    printf "%*s%s\n" "$padding" "" "$1"
}

DB="$HOME/.dark_users"
[ ! -f "$DB" ] && echo "admin:dark123" > $DB

clear
echo -e "$g"; center "[ BOOTING DARK SYSTEM ]"; sleep 1
for i in {1..5}; do center "Loading $i..."; echo -e "\a"; sleep 0.3; done
center "[ READY ]"; sleep 1; clear

echo -e "$g"; center "🔐 LOGIN"; echo ""
read -p "Username: " user
read -sp "Password: " pass; echo ""

grep -q "^$user:$pass$" $DB || { echo -e "$r"; center "ACCESS DENIED"; exit; }

center "ACCESS GRANTED"; sleep 1; clear

cmatrix -b -u 2 -C green & pid=$!
sleep 2; kill $pid; clear

echo -e "$g"
center "██ DARK SYSTEM ██"
echo -e "$r"; center "☠ FINAL BOSS ☠"
echo -e "$w"; center "subang corporation"
echo ""

while true; do
echo -e "$c"
center "[1] Play"
center "[2] Audio"
center "[3] Search"
center "[4] MP3"
center "[5] Add User"
center "[0] Exit"
echo ""

read -p "root@dark# " p

case $p in
1) read -p "URL: " u; yt-dlp -o - "$u" | mpv - ;;
2) read -p "URL: " u; yt-dlp -f bestaudio -o - "$u" | mpv - ;;
3) ytfzf ;;
4) read -p "URL: " u; yt-dlp -x --audio-format mp3 "$u" ;;
5) read -p "User: " nu; read -sp "Pass: " np; echo ""; echo "$nu:$np" >> $DB ;;
0) exit ;;
*) echo "error" ;;
esac

read -p "ENTER..."
clear
done
