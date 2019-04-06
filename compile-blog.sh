#!/bin/bash

FILE="$1"
TMP="/tmp"
grep -Po "(?<=<title type='text'>)[^<]*(?=</title>)" "$FILE" > $TMP/titles
grep -Po "(?<=<link rel='alternate' type='text/html' href=')[^']*(?=')" "$FILE" > $TMP/hrefs
grep -Po "(?<=<published>)[^<]*(?=<)" "$FILE" > $TMP/times

paste $TMP/titles $TMP/hrefs $TMP/times
rm $TMP/titles $TMP/hrefs $TMP/times
