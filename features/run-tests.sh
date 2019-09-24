rm -r ./reports
START=$(date +"%T")
behave $1
FINISH=$(date +"%T")
for entry in "./reports"/*.xml
do
  junit2html "$entry" "${entry%.*}.html"
done
python discord_bot.py $START $FINISH