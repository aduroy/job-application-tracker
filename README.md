# Job Application Tracker

This project provides a Web interface for keeping track of job applications, prospects and some insights.

> Data is stored locally using SQLite in a file called `database/database.db`.

# Screenshots

## Job application overview

![n-gram representation](https://github.com/aduroy/NGramGenerator/blob/master/data/ngram_prob.png)

## Prospects

![n-gram representation](https://github.com/aduroy/NGramGenerator/blob/master/data/ngram_prob.png)

## Insights

![n-gram representation](https://github.com/aduroy/NGramGenerator/blob/master/data/ngram_prob.png)

# How to

## Requirements

### Install Python

```commandline
$ python --version
Python 3.10.x
```

### Install dependencies

```commandline
pip install -r requirements.txt
```

### Environment variables

```commandline
REACT_VERSION=18.2.0
```

### Run

```commandline
python app.py
```

### Generate fake data

```commandline
python database/controllers_applications.py
```

