#!/usr/bin/env bash

LOG_FILE="${1:-/var/log/nginx/access.log}"

if [[ ! -f "$LOG_FILE" ]]; then
    echo "Error: Log file not found -> $LOG_FILE"
    exit 1
fi

TMP_CLEAN=$(mktemp)
trap 'rm -f "$TMP_CLEAN"' EXIT

# Extract:
# IP | STATUS | ENDPOINT
awk '
{
    ip="-"; status="-"; endpoint="-";

    # Extract IP (first column usually)
    if ($1 ~ /^[0-9]+\.[0-9]+\.[0-9]+\.[0-9]+$/) {
        ip=$1
    }

    # Extract status (3-digit number)
    for (i=1; i<=NF; i++) {
        if ($i ~ /^[1-5][0-9][0-9]$/) {
            status=$i
        }
    }

    # Extract endpoint (inside quotes: "METHOD /path HTTP/x.x")
    match($0, /"(GET|POST|PUT|DELETE|PATCH|HEAD|OPTIONS) [^ ]+/, arr)
    if (arr[0] != "") {
        split(arr[0], parts, " ")
        endpoint=parts[2]
    }

    # Only print if at least IP exists
    if (ip != "-") {
        print ip, status, endpoint
    }
}
' "$LOG_FILE" > "$TMP_CLEAN"

TOTAL_REQUESTS=$(wc -l < "$TMP_CLEAN")

UNIQUE_IPS=$(awk '{print $1}' "$TMP_CLEAN" | sort | uniq | wc -l)

ERROR_4XX=$(awk '$2 ~ /^4/ {count++} END {print count+0}' "$TMP_CLEAN")
ERROR_5XX=$(awk '$2 ~ /^5/ {count++} END {print count+0}' "$TMP_CLEAN")

# Avoid division by zero
if [[ "$TOTAL_REQUESTS" -gt 0 ]]; then
    PCT_4XX=$(awk -v e="$ERROR_4XX" -v t="$TOTAL_REQUESTS" 'BEGIN {printf "%.2f", (e/t)*100}')
    PCT_5XX=$(awk -v e="$ERROR_5XX" -v t="$TOTAL_REQUESTS" 'BEGIN {printf "%.2f", (e/t)*100}')
else
    PCT_4XX="0.00"
    PCT_5XX="0.00"
fi

TOP_IPS=$(awk '{print $1}' "$TMP_CLEAN" \
    | sort | uniq -c | sort -nr | head -10)

TOP_ENDPOINTS=$(awk '$3 != "-" {print $3}' "$TMP_CLEAN" \
    | sort | uniq -c | sort -nr | head -10)

echo "=== Nginx Log Analysis Report ==="

printf "Total Requests: %d\n" "$TOTAL_REQUESTS"
printf "Unique IPs: %d\n" "$UNIQUE_IPS"
printf "4xx Errors: %d (%s%%)\n" "$ERROR_4XX" "$PCT_4XX"
printf "5xx Errors: %d (%s%%)\n" "$ERROR_5XX" "$PCT_5XX"

echo ""
echo "Top 10 IPs:"
rank=1
echo "$TOP_IPS" | while read -r count ip; do
    printf " %2d. %-15s %d requests\n" "$rank" "$ip" "$count"
    ((rank++))
done

echo ""
echo "Top 10 Endpoints:"
rank=1
echo "$TOP_ENDPOINTS" | while read -r count endpoint; do
    printf " %2d. %-30s %d requests\n" "$rank" "$endpoint" "$count"
    ((rank++))
done