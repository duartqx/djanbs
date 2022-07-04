# Djanbs

Djanbs is a personal project of a website/webapp for companies to offer jobs and candidate users to apply to these offers, built using Python and Django.
It's currently a work in progress and not production ready

## How to run Djanbs Locally

First you need to have Python and Django installed

` pip install -r requirements.txt `

Them run the development server with:

` python manage.py runserver `

And open any browser on page ` http://localhost:8000 `

## Running the Application with Docker

If you don't want to install django locally you could run inside a docker container

cd into the djanbs folder and run

` docker build -t djanbs .`

This command will generate a docker image that you can run with the following command

` docker run -it -p 8000:8000 djanbs `

## Seeing the service in Action

To see the service in action you can create a new user, either a candidate or a company user and see how everything works
By clicking their login name at the top of the app user can access their profiles. There Candidate users also have access to a list with all their candidated job offers where they can give up. Also on their profiles, users can click on a link to edit their informations.

The main page for candidates show a list of currently open job offers where they can see more details about the offer and candidate themselves

For Companies the mainpage lists their job offers where they can see how many users candidated themselves to those offers, edit each offer or delete them
There's also a details link that shows every candidate to these offers and their infos and if these candidates fit into the offers requirements
