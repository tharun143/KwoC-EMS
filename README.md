![ForTheBadge built-with-love](http://ForTheBadge.com/images/badges/built-with-love.svg) ![Open Source Love png2](https://badges.frapsoft.com/os/v2/open-source.png?v=103) ![MIT Licence](https://badges.frapsoft.com/os/mit/mit.png?v=103)

# Enterprise-Management-System
Enterprise Management System (EMS) mainly intends on making the enterprise work ease and effortless. It focuses on managing the accounts of the Enterprise by jotting down the transactions done by an enterprise. The transactions are updated by the enterprise to the accountant through the website.

The application is having separate portals for both the enterprise and the accountant. The transactions are secured and the application maintains data abstraction from the other enterprises.

## Enterpreneur

The enterprise portal holds text fields to enter the details of transactions and a dropbox for uploading documents. Additionally, it can also show the status of the transactions and the entreprenuer can get the returns of his transactions.

### Fields included in Enterpreneur Portal
- Transaction ID
- Date
- Transaction Type
- Amount
- Description
- Status
- Drop box
- Edit access
- Comment access

## Accountant

The accountant portal consists of transactions from an enterprise. The transactions also contain relevant documents and proofs. If there are no valid documents for a particular transaction then the accountant can comment on the particular transaction. Once the transaction is verified the accountant updates the status of the transaction(pending or done). The accountant can generate the Income Tax returns of an Enterprise.
By this, we can make sure that the transaction is not lost and delivered.

### Fields included in Accountant Portal
- Transaction ID
- Date
- Transaction Type
- Amount
- Description
- Status
- Comment access

To know more about the project and to understand the code base refer Reports section.

# Installation Guide :inbox_tray:

Follow the below instructions to set up the environment in your host system.

## Virtual Environment

1. Create a Virtual Environemnt for this project. Because I don't want you to mess up with your host system.

Ubuntu 18.04 ships with Python 3.6 by default. You can verify that Python 3 is installed on your system by running:

> python3 -V

The output should look like this:

> Python 3.6.5

2. Starting from Python 3.6, the recommended way to create a virtual environment is to use the venv module.

Let’s start by installing the python3-venv package that provides the venv module.

> sudo apt install python3-venv

3. Once the module is installed we are ready to create virtual environments for Python 3.

Switch to the directory where you would like to store your Python 3 virtual environments. Within the directory run the following command to create your new virtual environment:

> python3 -m venv my-project-env

The command above creates a directory called my-project-env, which contains a copy of the Python binary, the Pip package manager, the standard Python library and other supporting files.

4. To start using this virtual environment, you need to activate it by running the activate script:

> source my-project-env/bin/activate

5. Once activated, the virtual environment’s bin directory will be added at the beginning of the $PATH variable. Also your shell’s prompt will change and it will show the name of the virtual environment you’re currently using. In our case that is my-project-env:

> $ source my-project-env/bin/activate

6. After running the above command you should see the below output.

> (my-project-env) $

## Cloning Repo

Clone the repo in to your local pc

> git clone https://github.com/tharun143/Enterprise-Management-System.git

Navigate to your repository

> cd Enterprise-Management-System

## Requirements

Now that the virtual environment is activated, we can start installing, upgrading, and removing packages using pip.
To install all the requirements of this project in virtaul environment. Execute the below command:

> pip install -r requirements.txt

## Running in localhost

To see the output of this project. Execute the below command in the terminal

> flask run

After executing the command you should see something like this in the terminal

 * Environment: production
   WARNING: This is a development server. Do not use it in a production deployment.
   Use a production WSGI server instead.
 * Debug mode: off
 * Running on http://127.0.0.1:5000/ (Press CTRL+C to q)
 
 Enter the http://127.0.0.1:5000/ in the search engine and preview the website. 
