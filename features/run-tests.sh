rm -r ./reports
behave $1
for entry in "./reports"/*.xml
do
  junit2html "$entry" "${entry%.*}.html"
done
