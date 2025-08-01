#!/bin/bash

# Hugo 테마 디렉토리 생성
mkdir -p blog/themes
cd blog/themes

# PaperMod 테마 클론
git clone https://github.com/adityatelange/hugo-PaperMod.git PaperMod

# 상위 디렉토리로 이동
cd ../..

# 정적 파일 디렉토리 생성
mkdir -p blog/static/images
mkdir -p blog/content/posts
mkdir -p blog/content/search
mkdir -p blog/content/archives
mkdir -p blog/content/categories

# 검색 페이지 생성
echo '---
title: "Search"
layout: "search"
summary: "search"
---' > blog/content/search/index.md

# 아카이브 페이지 생성
echo '---
title: "Archives"
layout: "archives"
url: "/archives/"
summary: archives
---' > blog/content/archives/index.md
