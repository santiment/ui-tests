rm -r ./reports
start=$(date +"%T")
SECONDS=0
behave $1
finish=$(date +"%T")
for entry in "./reports"/*.xml
do
  junit2html "$entry" "${entry%.*}.html"
done
python discord_bot.py $start $finish $SECONDS