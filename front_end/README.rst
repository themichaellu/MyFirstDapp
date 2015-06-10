factserver
==============================

Etherium fact server

.. image:: https://codeship.com/projects/d9916e80-a0ae-0132-c300-3e3486fb28a9/status?branch=master
   :target: https://codeship.com/projects/65474
   :alt: Codeship Status for alfetopito/et_factserver


---------------


Settings
------------

For configuration purposes, the following table maps the 'factserver' environment variables to their Django setting:

======================================= =========================== ============================================== ===========================================
Environment Variable                    Django Setting              Development Default                            Production Default
======================================= =========================== ============================================== ===========================================
DJANGO_AWS_ACCESS_KEY_ID                AWS_ACCESS_KEY_ID           n/a                                            raises error
DJANGO_AWS_SECRET_ACCESS_KEY            AWS_SECRET_ACCESS_KEY       n/a                                            raises error
DJANGO_AWS_STORAGE_BUCKET_NAME          AWS_STORAGE_BUCKET_NAME     n/a                                            raises error
DJANGO_CACHES                           CACHES                      locmem                                         memcached
DJANGO_DATABASES                        DATABASES                   See code                                       See code
DJANGO_DEBUG                            DEBUG                       True                                           False
DJANGO_EMAIL_BACKEND                    EMAIL_BACKEND               django.core.mail.backends.console.EmailBackend django.core.mail.backends.smtp.EmailBackend
DJANGO_SECRET_KEY                       SECRET_KEY                  CHANGEME!!!                                    raises error
DJANGO_SECURE_BROWSER_XSS_FILTER        SECURE_BROWSER_XSS_FILTER   n/a                                            True
DJANGO_SECURE_SSL_REDIRECT              SECURE_SSL_REDIRECT         n/a                                            True
DJANGO_SECURE_CONTENT_TYPE_NOSNIFF      SECURE_CONTENT_TYPE_NOSNIFF n/a                                            True
DJANGO_SECURE_FRAME_DENY                SECURE_FRAME_DENY           n/a                                            True
DJANGO_SECURE_HSTS_INCLUDE_SUBDOMAINS   HSTS_INCLUDE_SUBDOMAINS     n/a                                            True
DJANGO_SESSION_COOKIE_HTTPONLY          SESSION_COOKIE_HTTPONLY     n/a                                            True
DJANGO_SESSION_COOKIE_SECURE            SESSION_COOKIE_SECURE       n/a                                            False
======================================= =========================== ============================================== ===========================================

* Note that not all settings listed here are currently in use.

Getting up and running
----------------------

To get the development version running, all you need to have is vagrant/virtualbox combo.

Get into the root folder, run a::

    $ vagrant up

You are all set. The provision script will take care of:

* install python 3.4.2
* install postgresql
* create required database/user
* install the project requiremets
* migrate whatever is needed

It will forward the port 8050.

If using PyCharm, copy this_ ``.idea`` folder and place it inside the project root.

.. _this: https://www.dropbox.com/sh/hs5ptw6gbsdg93l/AABNXxaherT8eZVsbViQeZyra?dl=0

Then on PyCharm go to ``File > Open... > project root folder`` and it will be all set.


Deployment
----------

We are using Dokku for both local (I'll call it staging) and production.


Staging: Vagrant
^^^^^^^^^^^^^^^^

* Clone dokku::

    $ git clone https://github.com/progrium/dokku.git

* Set the local IP in your ``/etc/hosts`` file (to whatever IP you have chosen, 10.0.0.2 is the default)::

    10.0.0.2 dokku.me

* Create the VM::

    $ cd /path/to/dokku/clone
    $ vagrant up

* Access http://dokku.me, paste your ssh public key, the one you use with the git repository for this project -- generally from ``cat ~/.ssh/id_rsa.pub``.

* Paste **dokku.me** on Hostname input, and check the **Virtualhost naming** box. This will make the app accessible later as ``app-name.dokku.me``.

Just a reminder that you will have to add ``app-name.dokku.me`` to your ``/etc/hosts`` as well, using the same IP.

* Install the plugins:

.. code-block:: bash

    $ cd /path/to/dokku/clone
    $ vagrant ssh
    $ cd /var/lib/dokku/plugins
    $ sudo git clone https://github.com/Kloadut/dokku-pg-plugin postgresql
    $ sudo git clone https://github.com/statianzo/dokku-supervisord.git /var/lib/dokku/plugins/dokku-supervisord
    $ sudo git clone https://github.com/alfetopito/dokku-ethereum-plugin.git ethereum
    $ sudo dokku plugins-install

* Create the database. You can do this either inside the VM or outside:

.. code-block:: bash

    $ dokku postgresql:create factserver                   # server side
    $ ssh -t dokku@dokku.me postgresql:create factserver   # client side

Save the ``Url: 'postgres://...'``, we will need this in a minute.

* Set the new machine as a git remote on the project::

    $ git remote add local-dokku dokku@dokku.me:factserver

Now you are all set! Next step is pushing the app.


Production: AWS
^^^^^^^^^^^^^^^

* Boot a new VM with Ubuntu 14.04 x64 t2.micro within a security group with access to ports 22 and 80.

* Either have a dns point at the new machine or set it on you ``/etc/hosts``::

    <machine ip>  dokku.aws.me

* Ssh the new machine and install dokku:

.. code-block:: bash

    $ ssh -i /path/to/.pem/file ubuntu@dokku.aws.me
    $ sudo su
    # cd /root
    # wget -qO- https://raw.github.com/progrium/dokku/v0.3.15/bootstrap.sh | sudo DOKKU_TAG=v0.3.15 bash
    # wget -qO- https://raw.github.com/progrium/dokku/v0.3.15/bootstrap.sh | sudo DOKKU_TAG=v0.3.15 bash

Yes, I meant to run it twice.

* Install the web installer:

.. code-block:: bash

    # cd /root/dokku
    # make dokku-installer

* Access http://dokku.aws.me, paste your ssh public key, the one you use with the git repository for this project -- generally from ``cat ~/.ssh/id_rsa.pub``.

* Paste **dokku.aws.me** on Hostname input, and check the **Virtualhost naming** box. This will make the app accessible later as ``app-name.dokku.aws.me``.

Just a reminder that you will have to add ``app-name.dokku.aws.me`` to your ``/etc/hosts`` as well, using the same IP.

* Install the plugins. Ssh to the machine, then:

.. code-block:: bash

    $ cd /var/lib/dokku/plugins
    $ sudo git clone https://github.com/statianzo/dokku-supervisord.git /var/lib/dokku/plugins/dokku-supervisord
    $ sudo git clone https://github.com/alfetopito/dokku-ethereum-plugin.git ethereum
    $ sudo dokku plugins-install

* Create and RDS instance using Postgresql. Remember the username, password port and database name you set during the instance creation.
* Open the database port you used in the previous step on the security group the new RDS instance is running.

If you did it right, at RDS management console when you select the instance, after the Endpoint you should see in green *authorized*.

* Now that you have the Endpoint, build a url like so::

    postgresql://<username>:<password>@<endpoint>/<dbname>

Keep it, we will need it in a minute.

* Set the new machine as a git remote on the project::

    $ git remote add aws-dokku dokku@dokku.aws.me:factserver

Now you are all set! Next step is pushing the app.


Push the app
^^^^^^^^^^^^

..  code-block:: bash

    $ git push local-dokku master  # local
    $ git push aws-dokku master  # aws

It will trigger the deployment, install all the dependencies and set nginx to point at http://factserver.dokku<.aws>.me.

But we are not done yet, for the first time there are a couple of env vars to set, migrations to migrate, superusers to create.


One time configs
^^^^^^^^^^^^^^^^

* The base:

..  code-block:: bash

    ssh -t dokku@dokku.me config:set factserver DATABASE_URL=<remember the Url I told you to keep?>
    ssh -t dokku@dokku.me config:set factserver DJANGO_CONFIGURATION=Production
    ssh -t dokku@dokku.me config:set factserver DJANGO_SECRET_KEY=<something random>

* This is for serving the static files from S3:

..  code-block:: bash

    ssh -t dokku@dokku.me config:set factserver DJANGO_AWS_ACCESS_KEY_ID=AKIAJRYKUV6BERUCHOPA
    ssh -t dokku@dokku.me config:set factserver DJANGO_AWS_SECRET_ACCESS_KEY=YOUR_AWS_SECRET_ACCESS_KEY_HERE
    ssh -t dokku@dokku.me config:set factserver DJANGO_AWS_STORAGE_BUCKET_NAME=etfactserver

* Email settings:

..  code-block:: bash

    ssh -t dokku@dokku.me dokku config:set factserver DJANGO_EMAIL_HOST_PASSWORD=YOUR_SENDGRID_USERNAME
    ssh -t dokku@dokku.me dokku config:set factserver DJANGO_EMAIL_HOST_USER=gnosis.ethereum@gmail.com

* We also need to start the Ethereum cpp client and link it to our app:

.. code-block:: bash

    ssh -t dokku@dokku.me eth:create
    ssh -t dokku@dokku.me eth:link factserver

* This will migrate the db, you might need to do this more times in the future::

    ssh -t dokku@dokku.me run factserver python factserver/manage.py migrate

* And this will create you a super user::

    ssh -t dokku@dokku.me run factserver python factserver/manage.py createsuperuser

When deploying via Dokku make sure you backup your database in some fashion as it is NOT done automatically.
