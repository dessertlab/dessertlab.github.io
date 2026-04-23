#!/usr/bin/env bash
set -euo pipefail

repo="${1:-.}"

echo "Files with site.base before conversion:"
rg -n 'site\.base' "$repo" || true
echo

files="$(rg -l 'site\.base' "$repo" || true)"

if [ -z "$files" ]; then
  echo "No site.base occurrences found."
  exit 0
fi

echo "$files" | while IFS= read -r f; do
  [ -z "$f" ] && continue

  perl -0pi -e '
    s/\{\%\s*capture\s+proj-url\s*\%\}\s*\{\{\s*site\.base\s*\}\}\s*\{\{\s*project\.url\s*\}\}\.html\s*\{\%\s*endcapture\s*\%\}/{% capture proj-url %}{{ project.url | append: ".html" | relative_url }}{% endcapture %}/g;
    s/\{\%\s*capture\s+proj-url\s*\%\}\s*\{\{\s*site\.base\s*\}\}\s*\{\{\s*topic\.url\s*\}\}\.html\s*\{\%\s*endcapture\s*\%\}/{% capture proj-url %}{{ topic.url | append: ".html" | relative_url }}{% endcapture %}/g;

    s/\{\%\s*capture\s+imgurl\s*\%\}\s*\{\{\s*site\.base\s*\}\}\s*\{\{\s*project\.image\s*\}\}\s*\{\%\s*endcapture\s*\%\}/{% capture imgurl %}{{ project.image | relative_url }}{% endcapture %}/g;
    s/\{\%\s*capture\s+imgurl\s*\%\}\s*\{\{\s*site\.base\s*\}\}\s*\{\{\s*topic\.image\s*\}\}\s*\{\%\s*endcapture\s*\%\}/{% capture imgurl %}{{ topic.image | relative_url }}{% endcapture %}/g;

    s/\{\{\s*site\.base\s*\}\}\s*\{\{\s*post\.url\s*\}\}/{{ post.url | relative_url }}/g;
    s/\{\{\s*site\.base\s*\}\}\s*\{\{\s*item\.link\s*\}\}/{{ item.link | relative_url }}/g;

    s/\{\{\s*site\.base\s*\}\}\s*(\/[^}"'\''\s<]*)/{{ "$1" | relative_url }}/g;
  ' "$f"
done

echo
echo "Files with site.base after conversion:"
rg -n 'site\.base' "$repo" || true
echo
git diff
