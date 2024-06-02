#!/bin/bash

# 비밀 정보가 포함된 파일 경로 목록
files=(
"견적왕 견적서 뽑기 크롤링/최종/RAG/.env"
"RAG/컴퓨터견적추천_ipynb의_사본의_사본.py"
)

# Git 기록에서 파일 제거
for file in "${files[@]}"
do
  git filter-repo --path $file --invert-paths
done
