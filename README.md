# anikore-scrapy

Scrapy project for anikore(https://www.anikore.jp/)

## Description

Cralwer & Scraper for anikore.
This can get bellow data.
- animes
- tags
- reviews
- users 

## Features

- Connected MongoDB

## Requirement

Read requirements.txt

## Usage

1. Modify settings.py
modify MONGODB_COLLECTION to your collection name. 
```
MONGODB_COLLECTION = [collection_name]
```
2. Get crawl spider
```
scrapy crawl [spider_name] 
```

## Installation

Plz Download by hand. 

## Author

@watanta
