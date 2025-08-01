@echo off
mkdir blog\themes
cd blog\themes

git clone https://github.com/adityatelange/hugo-PaperMod.git PaperMod

cd ..\..

mkdir blog\static\images
mkdir blog\content\posts
mkdir blog\content\search
mkdir blog\content\archives
mkdir blog\content\categories

echo --- > blog\content\search\index.md
echo title: "Search" >> blog\content\search\index.md
echo layout: "search" >> blog\content\search\index.md
echo summary: "search" >> blog\content\search\index.md
echo --- >> blog\content\search\index.md

echo --- > blog\content\archives\index.md
echo title: "Archives" >> blog\content\archives\index.md
echo layout: "archives" >> blog\content\archives\index.md
echo url: "/archives/" >> blog\content\archives\index.md
echo summary: archives >> blog\content\archives\index.md
echo --- >> blog\content\archives\index.md
