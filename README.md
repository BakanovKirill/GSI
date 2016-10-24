## INSTALLATION


`python bootstrap-buildout.py`

`bin/buildout`

## STARTING in the Local Environment


`cd gsi`

`source .env/bin/activate`

`make run`

## DATABASE (locally deploy a working version)


`cd gsi`

`source .env/bin/activate`

`createdb gsi`

`make update_dev_db`
#### To run this command, you must specify three parameters in the fabfile.py:
`GSI_APP_SERVER = <username> @ <server name>`

`REMOTE_CODE_DIR = root folder of the project`

`ENV_PASS = password to login on ssh.`

`These data are in module "local".`





### Project page:

http://indy4.epcc.ed.ac.uk/
