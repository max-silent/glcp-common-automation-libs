# glcp-common-automation-libs


#### How to use the libs in your repo:

Add this line to your project repo in `[tool.poetry.dependencies]` section of pyproject.toml file:- 

hpe-glcp-automation-lib = "^2.1.0"

 #
### In case of failed Lint step in CI on PR pipeline, need to manually fix formatting by executing scripts/fix-lint.sh
To run autoformatting script ensure that corresponding libraries are installed in your environment, 
or install them with `pip install mypy autoflake black isort`
#
#### 1. Make sure Jfrog creds are available on your env:
_Mac:_

`export JFROG_USERNAME="username"`

`export JFROG_PASSWORD="password"`

_Windows (Powershell):_

`$Env:JFROG_USERNAME="username"`

`$Env:JFROG_PASSWORD="password"`


#### 2. Install and configure poetry:
`pip install poetry`

`poetry config virtualenvs.create true`

_Mac:_ `poetry config http-basic.jfrog "${JFROG_USERNAME}" "${JFROG_PASSWORD}"`

_Windows (Powershell):_ `poetry config http-basic.jfrog $Env:JFROG_USERNAME $Env:JFROG_PASSWORD`

Run `poetry install` to create/update poetry.lock file.

_**Note:** if you've got "Warning: poetry.lock is not consistent with pyproject.toml." - then remove poetry.lock via `rm poetry.lock` and rerun `poetry install`_

Make sure playwright is installed in your project repo:

#### 3. Steps to install playwright in python env:

`pip install pytest-playwright`

`pip install playwright pytest`

`playwright install-deps`

`playwright install chromium`


#### Example how to import and use a module:

from hpe_glcp_automation_lib.libs.ui_doorway.user_api.ui_doorway import UIDoorway

my_uid_sess = UIDoorway('cluster_url_wo_https://', 'username', 'password', 'pcid')

eg: my_uid_sess = UIDoorway('polaris.ccs.arubathena.com', 'username', 'password', 'pcid')

To view all the methods supported in my_uid_sess run:- dir(my_uid_sess)

get_devices = my_uid_sess.list_devices()


#### Library Help for functions and methods when adding new libs method or a function:

    """What is the function about and what does it do.

    Args:
        What are the args, example of args.
    Returns:
        What will be returned.
    Raises:
        Errors if args are not provided.
        Errors if value is not returned.

    """.


#### Page-object classes hierarchy
For work with web-pages each page has related page-object class with methods, which implement actions,
available on this page. Some of common methods and attributes are inherited from parent classes.
Current hierarchy of page-object classes is following:

1. Top level parent class:
* **BasePage** - _main parent class. Used as parent (direct or mediated) for the rest of page-object classes._

2. Inherited from BasePage:
* intermediate parent class:
  * **HeaderedPage**
* page-object classes related to corresponding pages without navigation header:
  * **CreateUserPage**
  * **CreateAcctPage**

3. Inherited from HeaderedPage:
 * page-object classes related to corresponding pages with navigation header
   * **HomePage**
   * **ManageAccount**
   * **Identity**
   * **Users**
   * **Roles**
   * **MyApplications**
   * **DevicesInventory**
   * **DeviceSubscriptions**


#### How to fix CERT errors in your local environment:
If you see something like this (On Windows) during **playwright install chromium**:

Error: unable to get local issuer certificate
    at TLSSocket.onConnectSecure (node:_tls_wrap:1539:34)
    at TLSSocket.emit (node:events:513:28)
    at TLSSocket._finishInit (node:_tls_wrap:953:8)
    at TLSWrap.ssl.onhandshakedone (node:_tls_wrap:734:12) {
  code: 'UNABLE_TO_GET_ISSUER_CERT_LOCALLY'

1. Go to https://playwright.azureedge.net/ and click the lock icon next to the address
2. Click on "Connection is secure" and "Certificate details" and then Details
3. Select each cert one by one (there should be four) and download them to ~
4. Using Powershell, put all the downloaded certs into one file like this:
- gc '.\Zscaler Root CA.crt' |ac cacert.pem
- gc '.\Zscaler Intermediate Root CA (zscalerthree.net) (t)_.crt' | ac .\cacert.pem
- gc '.\Zscaler Intermediate Root CA (zscalerthree.net).crt' | ac .\cacert.pem
- gc .\_.azureedge.net.crt | ac .\cacert.pem
5. Copy the cacert.pem file to c:\
6. export NODE_EXTRA_CA_CERTS=/c/cacert.pem (Git Bash, use appropriate export for your shell)
7. Now it should install. If you see "Warning: Ignoring extra certs from cacert.pem, load failed" - you did the export wrong
    
