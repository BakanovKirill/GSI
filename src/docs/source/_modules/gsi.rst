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


    **gsi** - source code to work with gsi application::

    |── gsi
    |   ├── admin.py
    |   ├── gsi_forms.py
    |   ├── gsi_items_update_create.py
    |   ├── __init__.py
    |   ├── migrations
    |   │   ├── 0001_initial.py
    |   │   ├── ...
    |   │   ├── 0026_auto_20160909_0806.py
    |   │   └── __init__.py
    |   ├── models.py
    |   ├── settings_local.py
    |   ├── settings.py
    |   ├── signals.py
    |   ├── tests
    |   │   ├── __init__.py
    |   │   └── test_signals.py
    |   ├── update_create.py
    |   ├── urls.py
    |   ├── views_cs_card_run_csid.py
    |   ├── views_cs_card_runid_csid.py
    |   ├── views.py
    |   └── wsgi.py


    **log** - source code to work with log application::

    |── gsi
    |   ├── admin.py
    |   ├── __init__.py
    |   ├── logger.py
    |   ├── migrations
    |   │   ├── 0001_initial.py
    |   │   ├── 0002_logdebug.py
    |   │   ├── 0003_remove_logdebug_user.py
    |   │   └── __init__.py
    |   ├── models.py
    |   └── views.py


    **core** - folder with auxiliary functions::

    |── core
    |   ├── copy_card.py
    |   ├── get_post.py
    |   ├── __init__.py
    |   ├── multithreaded.py
    |   ├── paginations.py
    |   ├── utils.py
    |   └── validator_gsi.py


    **static** - folder with statics::

    |── static
    |   ├── css
    |   │   ├── form_style.css
    |   │   ├── jquery.fs.selecter.css
    |   │   ├── main_reg.css
    |   │   └── styles.css
    |   ├── img
    |   │   ├── account-circle.png
    |   │   ├── anonim.png
    |   │   ├── back-18.png
    |   │   ├── background_log.jpg
    |   │   ├── back-to-up-18.png
    |   │   ├── bold.gif
    |   │   ├── chevron-double-right-18.png
    |   │   ├── code.gif
    |   │   ├── copy-18.png
    |   │   ├── customer_section.png
    |   │   ├── delete-18.png
    |   │   ├── details_18.png
    |   │   ├── download-18.png
    |   │   ├── edit-18.png
    |   │   ├── editor
    |   │   │   ├── anchor.png
    |   │   │   ├── bold.png
    |   │   │   ├── border-image.png
    |   │   │   ├── code.png
    |   │   │   ├── header-3.png
    |   │   │   ├── header-4.png
    |   │   │   ├── image.png
    |   │   │   ├── italic.png
    |   │   │   ├── link.png
    |   │   │   ├── ordered.png
    |   │   │   ├── paragraph.png
    |   │   │   ├── quote.png
    |   │   │   ├── top.png
    |   │   │   ├── underline.png
    |   │   │   └── unordered.png
    |   │   ├── email_18.png
    |   │   ├── eye_18.png
    |   │   ├── file-18.png
    |   │   ├── file-archive-18.png
    |   │   ├── file-bin-18.png
    |   │   ├── file-document-18.png
    |   │   ├── file-image-18.png
    |   │   ├── file-pdf-18.png
    |   │   ├── file-word-18.png
    |   │   ├── folder-18.png
    |   │   ├── go-folder-18.png
    |   │   ├── image-18.png
    |   │   ├── image.gif
    |   │   ├── italic.gif
    |   │   ├── link.gif
    |   │   ├── logout.png
    |   │   ├── menu-down-18.png
    |   │   ├── order-18.png
    |   │   ├── ordered.gif
    |   │   ├── overview.png
    |   │   ├── parallel-1-18.png
    |   │   ├── parallel-2-18.png
    |   │   ├── profile-18.png
    |   │   ├── quote.gif
    |   │   ├── settings.png
    |   │   ├── setup_new_run.png
    |   │   ├── setup_static_data.png
    |   │   ├── submit_a_run.png
    |   │   ├── underline.gif
    |   │   ├── unordered.gif
    |   │   ├── upload.png
    |   │   └── view_run_progress.png
    |   └── js
    |       ├── jquery.fs.selecter.min.js
    |       ├── modernizr.js
    |       ├── registrations.js
    |       ├── scripts_ajax.js
    |       ├── scripts_google_maps.js
    |       ├── scripts.js
    |       └── upload_file.js



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
