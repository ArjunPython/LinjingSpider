#!/bin/sh
clean(){
  for file in $1/*
  do
    if [ -d $file ]
    then
        clean $file
    else
      echo $file
         temp=$(tail -1000 $file)
      echo "$temp" > $file
    fi
  done
}

dir=/home/jun/Desktop/yun_spider/PlatformTarget/PlatformTarget/logs
clean $dir 
