#!/usr/bin/env bash
previous_tag=$(git tag --sort=-creatordate | sed -n 1p)
git shortlog "${previous_tag}.." | sed 's/^./    &/'
