#!/bin/bash

# Checkout each branch, pull the latest changes
for branch in langsmith main ex6 ex5 ex4 ex3 ex2 ex1; do
  git checkout $branch && git pull;
done
