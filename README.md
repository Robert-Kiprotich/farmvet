
# SoinVet web application

## Hosted

https://ishasr.pythonanywhere.com/

SoinVet is a web-based system  written in Python 3 and using Django framework with the following functionalities.
1.Register new users (Veterinary officers, Farmers and Students)
2.Log in registered users and be directed to their respective dashboards.
3.Veterinary officers can take appointments from farmers.
4.Veterinary officers can take veterinary related records like artificial insemination, breeding record, calf registration, clinical approach, consultation, death approach, deworming, livestock inventory, pregnancy diagnosis, sick approach and vaccination. 
5.Farmers can view and book appointments with Veterinary officers.
6.Farmers can retrieve their respective forms entered by veterinary officers.
7.Farmers can take inventory of their farm.
8.Admin can create learning resources for students
9.Students can access learning resources 

## In progress
3.Veterinary officers can take appointments from farmers.
5.Farmers can view and book appointments with Veterinary officers.
7.Farmers can take inventory of their farm
8.Admin can create learning resources for students
9.Students can access learning resources 

## Getting Started

These instructions will get you a copy of the project up and running on your local machine for development and testing purposes.


### Prerequisites
You will find hereafter what I use to develop and to run the project
* Python 3.9.1
* Django 3.1.5
* pipenv (not mandatory but highly recommended)

### Installation

Get a local copy of the project directory by cloning "SoinVet" from github.

```bash
git clone git@github.com:BabGee/SoinVet.git
```

cd into the folder

```bash
cd SoinVet
```

I use pipenv for developing this project so I recommend you to create a virtual environment and activate it.

```bash
python -m pipenv shell
```

Install the requirements

```bash
python -m pip install -r requirements.txt
```

Then follow these steps:
1. Move to root folder 

```bash
cd vetWeb/soin
```
2. Create a `.env` file in the root folder, provide the required database information  to the `.env` file (.env.example file is provided to help set this information)

3. Create the tables with the django command line

```bash
python manage.py makemigrations
```
then migrate the changes
 
```bash
python manage.py migrate
```

4. Finally, run the django server

```bash
python manage.py runserver
```

## Built With

* [Python 3](https://www.python.org/downloads/) - Programming language
* [Django](https://www.djangoproject.com/) - Web framework 


## Versioning
I use exclusively Github

## License

This is an open source project not under any particular license.
However framework, packages and libraries used are on their own licenses.
