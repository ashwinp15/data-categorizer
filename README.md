## Overview
This is a simple Flask server that takes a dataset file, performs some predetermined tasks on the dataset and downloads the output.


## Installation

You must have pipenv installed in your system. Install it using the following command
```bash
pip install pipenv --user
```
Next you want to install the dependencies required to run this server. To do that, run the following command
```bash
pipenv install
```

## Configuration

You need to have a **.env** file in which you set the values of the Google OAuth API credentials and secret for signing cookies. <br>
See the env.example file for reference

## Usage

Once the above steps are taken care of, you can run the server using the command
```bash
pipenv run python app.py
```
The server is hosted on https://127.0.0.1:5000/ <br>
On following this link you will be presented with a single link to authorize using your Google account. <br>
After which you will be redirected to the same page with the option to upload files and submit <br>
After submitting the file, you will be presented with 3 links each for purpose of:
* Filtering on the basis of payment
* Filtering on the basis of content rating
* Rounding off the ratings

Clicking on these links will present a download prompt with the expected output.

