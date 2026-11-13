#!/bin/bash
# What a null access does in an exported Godot game (game-engines §5).
#
# Exports this project as a macOS release and a macOS debug build, then runs
# each case separately: "none" (control, no error), "untyped" (method call on
# an untyped null variable), "typed" (method call on a `var n: Node = null`)
# and "prop" (property access on null). Prints each run's output and exit code.
#
# Needs Godot at /Applications/Godot.app with matching export templates.
# First run 2026-11-13 on Godot 4.7.2.stable (macOS, Apple silicon):
#   release: untyped and prop print nothing and the function carries on;
#            typed exits with 139 (segmentation fault)
#   debug:   every case logs a SCRIPT ERROR, aborts the function, game runs on
set -u
S="$(cd "$(dirname "$0")" && pwd)"
G=/Applications/Godot.app/Contents/MacOS/Godot
cd "$S"
rm -rf out && mkdir -p out/release out/debug
for mode in release debug; do
  "$G" --headless --path proj --export-$mode "macOS" "$S/out/$mode/test.zip" >/dev/null 2>&1
  (cd "out/$mode" && unzip -q test.zip)
done
for mode in release debug; do
  BIN="out/$mode/NullTest.app/Contents/MacOS/NullTest"
  for which in none untyped typed prop; do
    echo "=== $mode / $which"
    "$BIN" --headless -- "$which" < /dev/null > "out/$mode-$which.log" 2>&1
    rc=$?
    command grep -v -E '^\s*$|GDScript backtrace|^\s+\[[0-9]\]' "out/$mode-$which.log" | head -8
    echo "--- exit code $rc"
  done
done
