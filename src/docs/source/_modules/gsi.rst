******************************************
Project structure
******************************************

-- The project includes:

* four applications: **api**, **cards**, **gsi**, **log**;
* folder with auxiliary functions: **core**;
* folder with statics (styles, java script files, the image to the project): **static**;
* folder with templates: **template**;
* folder with custom tags: **tags**;

-- Structure of folders:

    **api** - source code to work with api::

    |── api
    |     ├── __init__.py
    |     └── views.py


    **cards** - source code to work with cards application::

    |── cards
    |   ├── admin.py
    |   ├── cards_forms.py
    |   ├── card_update_create.py
    |   ├── get_card_post.py
    |   ├── __init__.py
    |   ├── management
    |   │   ├── commands
    |   │   │   ├── fill_name_for_carditem_card.py
    |   │   │   └── __init__.py
    |   │   └── __init__.py
    |   ├── migrations
    |   │   ├── 0001_initial.py
    |   │   ├── ...
    |   │   ├── 0042_carditem_name.py
    |   │   ├── __init__.py
    |   ├── models.py
    |   ├── urls.py
    |   ├── views_card_run_csid.py
    |   ├── views_card_runid_csid.py
    |   ├── views_card_runid.py
    |   ├── views_card_run.py
    |   ├── views.py

    **gsi**

    **log**



::

|── api
|        ├── admin.py
|        ├── editor
|        │   ├── ed.js
|        │   ├── images
|        │   │   ├── bold.gif
|        │   │   ├── code.gif
|        │   │   ├── image.gif
|        │   │   ├── italic.gif
|        │   │   ├── link.gif
|        │   │   ├── ordered.gif
|        │   │   ├── quote.gif
|        │   │   ├── Thumbs.db
|        │   │   ├── underline.gif
|        │   │   └── unordered.gif
|        │   └── styles.css
|        ├── __init__.py
|        ├── migrations
|        │   ├── 0001_initial.py
|        │   ├── __init__.py
|        ├── models.py
|        ├── tests.py
|        ├── urls.py
|        └── views.py




Cards aplication
=================

Cards models
------------------

.. automodule:: cards.models
    :members:

Cards views
------------------

.. automodule:: cards.views
    :members:


Gsi aplication
===============

Gsi models
------------------

.. automodule:: gsi.models
    :members:

Gsi views
------------------

.. automodule:: gsi.views
    :members:
