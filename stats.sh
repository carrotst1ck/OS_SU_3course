#!/usr/bin/env bash

# Count ERROR records in every log file, then report the largest count.
error_total=0
largest_count=-1
largest_log=""

for log_path in data/*.log; do
    [[ -f "$log_path" ]] || continue

    error_count=$(grep -c "ERROR" "$log_path" || true)
    printf '%s: %s ошибок\n' "$log_path" "$error_count"

    (( error_total += error_count ))
    if (( error_count > largest_count )); then
        largest_count=$error_count
        largest_log=$log_path
    fi
done

printf 'Всего ошибок: %s\n' "$error_total"
if [[ -n "$largest_log" ]]; then
    printf 'Больше всего ошибок: %s (%s)\n' "$largest_log" "$largest_count"
fi
