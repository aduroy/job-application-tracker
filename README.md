# Job Application Tracker

This project provides a Web interface for keeping track of job applications, prospects and some insights.

> Data is stored locally using SQLite in a file called `database/database.db`.

# Screenshots

## Job application overview

![Job Application Overview](https://github.com/aduroy/job-application-tracker/blob/main/screenshots/job_applications_overview.png)

## Prospects

![Prospects](https://github.com/aduroy/job-application-tracker/blob/main/screenshots/prospects_overview.png)

## Insights

![Insights](https://github.com/aduroy/job-application-tracker/blob/main/screenshots/insights_overview.png)

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

