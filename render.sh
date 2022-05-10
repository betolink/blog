#!/usr/bin/env bash

find . -type f -name "*.qmd" | xargs -i quarto render {} --execute-debug

