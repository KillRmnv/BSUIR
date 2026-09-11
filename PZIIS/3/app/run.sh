#!/usr/bin/env bash
# Сборка и запуск без Maven/Gradle — только JDK. Работает на Arch и Void.
set -euo pipefail
cd "$(dirname "$0")"

javac -encoding UTF-8 -d out $(find src -name '*.java')
echo "Собрано в ./out"

if [ "${1:-}" = "--build-only" ]; then
  exit 0
fi
java -cp out app.Main "$@"
