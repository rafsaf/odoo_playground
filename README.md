# The tasks and some of my afterthoughts

It was surprisingly not simple to just start this app in local environment! :)

I'm using Ubuntu 20 and wsl2

# Download

The battle starts trying to download the project, after massive headache batteling docs, decided to go just with `odoo_13.0.latest.tar.gz` from download page, cloning the whole git repo probably would took few ages;)

# Install

This was even worse, final working setup looks like that:
  - some postgres defined in docker-compose.dev.yml
  - python3.7 in venv
  - requirments.txt (ldap for example but others maybe) also needed some apt installed stuff
  - odoo_config looked like this before it got overwritten by the app

    ```
    [options]
    admin_passwd=mysupersecretpassword
    dev=all
    
    addons_path=odoo/addons,custom
    
    http_interface=localhost
    http_port=8000
    
    db_user=very_unique_user
    database=postgres
    db_password=very_strong_password
    db_host=localhost
    db_port=5400
    
    test_enable=true
    ```
  - sweet, but `python odoo-bin -c odoo_config` refused to work, after some debugging it occured that windows could not communite wsl2 with localhost:8000 with browser on certain circumstances, https://github.com/microsoft/WSL/issues/5298... 
  - After killing Fast Startup Windows option, it... wasnt working also. 
  - **SUCCESS**, finally after another headache I found how to perform migrations or whatever it is called, `python odoo-bin -c odoo_config -d base` did the job, then- no way to login, but... username `admin` passwd `admin` worked, no idea for what reason I added `admin_passwd` to config earlier and what is it.
  - without a doubt this is not the simplest setup ever :)

#  The task

##  models 
I can see point of what we want - table with archived sale order and cron that is creating archived from old orders and removing the latter should not be complicated, right? Well... although I can see many common points and solution shared with Django or even things like Tortoise ORM, SQL Alchemy, this is in my opinion (after few hours of experience but still) a bit more powerful but not so readable, a bunch of methods, api, constraints, many fields kwargs, lack of IDE support

I leaved some notes in custom/models/models.py (btw created with `python odoo-bin scaffold sale_order_archive custom`)

## views
XML are something which should also be rather simple - but again it needs some experience, I did write demo list view

## controllers
For this part I sacrificed only few minutes, this should be the place where auth stuff (Sales Manager role) will be places

## Disclaimer

`python odoo-bin -c odoo_config -d sale_order_archive` is not working, there are some errors trying to migrate it, didn't really debugged it

# Sum up
This is the feedback I can provide, I can admit that to complete the tasks, some **odoo** specific knowledge is required or at least I would have to sacrifice for it **much, much** more time than few hours, it looks like powerful, but not too begginer-friendly (or friendly at all) piece of software. BUT - I can now perfectly understand why You use it (and make extensions) instead of wrriting something like that from scratch. The complexity of system is visible.