******************************************
Project structure
******************************************

The project includes
=====================

* package for work with API: **api**;
* three applications: **cards**, **gsi**, **log**;
* package with auxiliary functions: **core**;
* folder with statics (styles, java script files, the image to the project): **static**;
* folder with templates: **template**;
* package with custom tags: **tags**;
* folder with technical documentations: **docs**;


-- *"__init__.py"*: the file for to initialize of the packages.

-- *"urls.py"*: the file for the URLs of web pages.

-- *"admin.py"*: the file to display models in the admin part of the project.

-- *"migrations"*: the package migration of models. At each change in the tables creates a new migration.

-- *"template"*: the folder for templates of web pages.

-- *"static/css"*: the folder for styles of css.

-- *"static/js"*: the folder for JavaScript files which used in the project.

-- *"static/img"*: the folder for images which used in the project.

Structure of folders
========================

    **api** - source code to work with api::

    |── api
    |   ├── __init__.py
    |   └── views.py


    **cards** - source code to work with cards application::

    |── cards
    |   ├── admin.py
    |   ├── cards_forms.py
    |   ├── card_update_create.py
    |   ├── get_card_post.py
    |   ├── __init__.py
    |   ├── management
    |   |   ├── commands
    |   |   |   ├── fill_name_for_carditem_card.py
    |   |   |   └── __init__.py
    |   |   └── __init__.py
    |   ├── migrations
    |   |   ├── 0001_initial.py
    |   |   ├── ...
    |   |   ├── 0042_carditem_name.py
    |   |   ├── __init__.py
    |   ├── models.py
    |   ├── urls.py
    |   ├── views_card_runid_csid.py
    |   ├── views.py


    **gsi** - source code to work with gsi application::

    |── gsi
    |   ├── admin.py
    |   ├── gsi_forms.py
    |   ├── gsi_update_create.py
    |   ├── __init__.py
    |   ├── migrations
    |   |   ├── 0001_initial.py
    |   |   ├── ...
    |   |   ├── 0026_auto_20160909_0806.py
    |   |   └── __init__.py
    |   ├── models.py
    |   ├── settings_local.py
    |   ├── settings.py
    |   ├── signals.py
    |   ├── tests
    |   |   ├── __init__.py
    |   |   └── test_signals.py
    |   ├── urls.py
    |   ├── views_cs_card_runid_csid.py
    |   ├── views.py
    |   └── wsgi.py


    **log** - source code to work with log application::

    |── gsi
    |   ├── admin.py
    |   ├── __init__.py
    |   ├── logger.py
    |   ├── migrations
    |   |   ├── 0001_initial.py
    |   |   ├── 0002_logdebug.py
    |   |   ├── 0003_remove_logdebug_user.py
    |   |   └── __init__.py
    |   ├── models.py
    |   ├── tests.py
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
    |   |   ├── form_style.css
    |   |   ├── jquery.fs.selecter.css
    |   |   ├── main_reg.css
    |   |   └── styles.css
    |   ├── img
    |   |   ├── account-circle.png
    |   |   ├── anonim.png
    |   |   ├── back-18.png
    |   |   ├── background_log.jpg
    |   |   ├── back-to-up-18.png
    |   |   ├── chevron-double-right-18.png
    |   |   ├── copy-18.png
    |   |   ├── customer_section.png
    |   |   ├── delete-18.png
    |   |   ├── details_18.png
    |   |   ├── download-18.png
    |   |   ├── edit-18.png
    |   |   ├── editor
    |   |   |   ├── anchor.png
    |   |   |   ├── bold.png
    |   |   |   ├── border-image.png
    |   |   |   ├── code.png
    |   |   |   ├── header-3.png
    |   |   |   ├── header-4.png
    |   |   |   ├── image.png
    |   |   |   ├── italic.png
    |   |   |   ├── link.png
    |   |   |   ├── ordered.png
    |   |   |   ├── paragraph.png
    |   |   |   ├── quote.png
    |   |   |   ├── top.png
    |   |   |   ├── underline.png
    |   |   |   └── unordered.png
    |   |   ├── email_18.png
    |   |   ├── eye_18.png
    |   |   ├── file-18.png
    |   |   ├── file-archive-18.png
    |   |   ├── file-bin-18.png
    |   |   ├── file-document-18.png
    |   |   ├── file-image-18.png
    |   |   ├── file-pdf-18.png
    |   |   ├── file-word-18.png
    |   |   ├── folder-18.png
    |   |   ├── go-folder-18.png
    |   |   ├── image-18.png
    |   |   ├── logout.png
    |   |   ├── menu-down-18.png
    |   |   ├── order-18.png
    |   |   ├── overview.png
    |   |   ├── parallel-1-18.png
    |   |   ├── parallel-2-18.png
    |   |   ├── profile-18.png
    |   |   ├── settings.png
    |   |   ├── setup_new_run.png
    |   |   ├── setup_static_data.png
    |   |   ├── submit_a_run.png
    |   |   ├── upload.png
    |   |   └── view_run_progress.png
    |   ├── js
    |   |   ├── jquery.fs.selecter.min.js
    |   |   ├── modernizr.js
    |   |   ├── registrations.js
    |   |   ├── scripts_ajax.js
    |   |   ├── scripts_google_maps.js
    |   |   └── scripts.js


    **template** - folder with templates::

    |── template
    |   ├── base.html
    |   ├── base_registrations.html
    |   ├── base_wiki.html
    |   ├── cards
    |   |   ├── _calcstats_form.html
    |   |   ├── _collate_form.html
    |   |   ├── _create_processing_card_form.html
    |   |   ├── _mergecsv_form.html
    |   |   ├── _preproc_form.html
    |   |   ├── processing_card_new_run.html
    |   |   ├── _qrf_form.html
    |   |   ├── _randomforest_form.html
    |   |   ├── _remap_form.html
    |   |   ├── _rfscore_form.html
    |   |   ├── _rftrain_form.html
    |   |   ├── runid_csid_card.html
    |   |   └── _year_filter_form.html
    |   ├── gsi
    |   |   ├── _area_form.html
    |   |   ├── areas_list.html
    |   |   ├── audit_history.html
    |   |   ├── card_editions.html
    |   |   ├── card_item_update.html
    |   |   ├── _card_sequence_form.html
    |   |   ├── card_sequence.html
    |   |   ├── card_sequence_update.html
    |   |   ├── cards_list.html
    |   |   ├── _cs_calcstats_form.html
    |   |   ├── _cs_collate_form.html
    |   |   ├── _cs_mergecsv_form.html
    |   |   ├── _cs_preproc_form.html
    |   |   ├── _cs_qrf_form.html
    |   |   ├── _cs_randomforest_form.html
    |   |   ├── _cs_remap_form.html
    |   |   ├── _cs_rfscore_form.html
    |   |   ├── _cs_rftrain_form.html
    |   |   ├── _cs_year_filter_form.html
    |   |   ├── customer_section.html
    |   |   ├── _env_group_form.html
    |   |   ├── environment_groups_list.html
    |   |   ├── execute_run.html
    |   |   ├── gsi_map.html
    |   |   ├── home_variable_setup.html
    |   |   ├── index.html
    |   |   ├── _input_data_dir_form.html
    |   |   ├── input_data_dir_list.html
    |   |   ├── _modal_new_card.html
    |   |   ├── new_card_sequence.html
    |   |   ├── new_run.html
    |   |   ├── _ordered_card_items.html
    |   |   ├── _resolution_form.html
    |   |   ├── resolution_list.html
    |   |   ├── run_details.html
    |   |   ├── run_progress.html
    |   |   ├── run_setup.html
    |   |   ├── run_update.html
    |   |   ├── _satellite_form.html
    |   |   ├── satellite_list.html
    |   |   ├── static_data_item_edit.html
    |   |   ├── sub_card_details.html
    |   |   ├── submit_run.html
    |   |   ├── _tile_form.html
    |   |   ├── tiles_list.html
    |   |   ├── upload_file.html
    |   |   ├── view_log_file.html
    |   |   ├── view_log_file_sub_card.html
    |   |   ├── view_results_folder.html
    |   |   ├── view_results.html
    |   |   ├── _year_form.html
    |   |   ├── _years_group_form.html
    |   |   ├── years_group_list.html
    |   |   └── years_list.html
    |   ├── _modal_check_delete_items.html
    |   ├── _modal_preload.html
    |   ├── paginations.html
    |   ├── registration
    |   |   ├── login.html
    |   |   ├── password_change_done.html
    |   |   ├── password_change_form.html
    |   |   ├── password_reset_complete.html
    |   |   ├── password_reset_confirm.html
    |   |   ├── password_reset_done.html
    |   |   ├── password_reset_email.html
    |   |   ├── password_reset_form.html
    |   |   └── registration_form.html


    **tags** - folder with custom tags::

    |── tags
    |  ├── __init__.py
    |  ├── __init__.pyc
    |  └── templatetags
    |      ├── gsi_tags.py
    |      └── __init__.py


    **docs** - folder with technical documentations::


    |── docs
    |   ├── build
    |   │   ├── doctrees
    |   │   │   ├── environment.pickle
    |   │   │   ├── _general
    |   │   │   │   ├── _1_technologies
    |   │   │   │   │   ├── 1_1_backend.doctree
    |   │   │   │   │   └── 1_2_frontend.doctree
    |   │   │   │   ├── 1_used_technologies.doctree
    |   │   │   │   ├── 2_designation_of_graphical_icons.doctree
    |   │   │   │   ├── _3_frontend
    |   │   │   │   │   ├── 3_1_authorization.doctree
    |   │   │   │   │   ├── 3_2_sidebar.doctree
    |   │   │   │   │   └── 3_3_creating_of_cards.doctree
    |   │   │   │   ├── 3_frontend.doctree
    |   │   │   │   └── 4_backend.doctree
    |   │   │   ├── index.doctree
    |   │   │   └── _modules
    |   │   │       ├── api.doctree
    |   │   │       ├── cards.doctree
    |   │   │       ├── core.doctree
    |   │   │       ├── gsi.doctree
    |   │   │       ├── js.doctree
    |   │   │       ├── log.doctree
    |   │   │       └── structure.doctree
    |   ├── html
    |   |   ├── _general
    |   |   |   ├── _1_technologies
    |   |   |   |   ├── 1_1_backend.html
    |   |   |   |   └── 1_2_frontend.html
    |   |   |   ├── 1_used_technologies.html
    |   |   |   ├── 2_designation_of_graphical_icons.html
    |   |   |   ├── _3_frontend
    |   |   |   |   ├── 3_1_authorization.html
    |   |   |   |   ├── 3_2_sidebar.html
    |   |   |   |   └── 3_3_creating_of_cards.html
    |   |   |   ├── 3_frontend.html
    |   |   |   └── 4_backend.html
    |   ├── genindex.html
    |   ├── _images
    |   |   ├── card_01.png
    |   |   ├── card_02.png
    |   |   ├── card_03.png
    |   |   ├── card_04.png
    |   |   ├── copy.png
    |   |   ├── delete.png
    |   |   ├── details.png
    |   |   ├── edit_area.png
    |   |   ├── edit_eg.png
    |   |   ├── edit.png
    |   |   ├── edit_yg.png
    |   |   ├── env_group.png
    |   |   ├── fill_sr.png
    |   |   ├── full_areas.png
    |   |   ├── full_cards.png
    |   |   ├── full_cs_polugon_markers.png
    |   |   ├── full_idd.png
    |   |   ├── full_resolutions.png
    |   |   ├── full_satellites.png
    |   |   ├── full_tiles.png
    |   |   ├── full_utd.png
    |   |   ├── full_years.png
    |   |   ├── full_yg.png
    |   |   ├── home_var.png
    |   |   ├── login_full.png
    |   |   ├── logs_current_progress.png
    |   |   ├── new_run_1.png
    |   |   ├── new_run.png
    |   |   ├── overview.png
    |   |   ├── pass_reset.png
    |   |   ├── registration.png
    |   |   ├── run_progress.png
    |   |   └── select_card_item.png
    |   | this select
    |   ├── index.html
    |   ├── _modules
    |   |   ├── api
    |   |   |   └── views.html
    |   |   ├── api.html
    |   |   ├── cards
    |   |   |   ├── cards_forms.html
    |   |   |   ├── card_update_create.html
    |   |   |   ├── models.html
    |   |   |   ├── views_card_runid_csid.html
    |   |   |   └── views.html
    |   |   ├── cards.html
    |   |   ├── core
    |   |   |   ├── copy_card.html
    |   |   |   ├── get_post.html
    |   |   |   ├── multithreaded.html
    |   |   |   ├── paginations.html
    |   |   |   ├── utils.html
    |   |   |   └── validator_gsi.html
    |   |   ├── core.html
    |   |   ├── gsi
    |   |   |   ├── gsi_forms.html
    |   |   |   ├── gsi_update_create.html
    |   |   |   ├── models.html
    |   |   |   ├── signals.html
    |   |   |   ├── views_card_runid_csid.html
    |   |   |   └── views.html
    |   | this select 2
    |   |   ├── gsi2.html
