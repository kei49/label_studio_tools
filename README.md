# label_studio_tools

## Purpose

These python scripts help download audio file stored in Azure Blob Storage locally by providing csv file exported from Label Studio audio annotation projects.

## Setup

1: Export csv files from Label Studio
2: Place it in ./data/import

```
mkdir data
mkdir data/import
cp xxx.csv data/import
```

3: Update the csv file in label_studio_tools/main.py

4: Create .env referencing .env.example

## Install dependencies

```
poetry install
```

## Run to download audio files

The file name of each audio file will be the task id of Label Studio project.

```
python label_studio_tools/main.py
```
