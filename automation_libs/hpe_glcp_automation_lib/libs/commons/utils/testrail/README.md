# Organization of this folder

This folder contains testrails lib, splitted each part of TestRail interaction in a respective file, to allow easier reuse of common TestRail operations in other environments beyond PyTest, like RobotFramework.

Now the the files are organized in the following inheritance order:

```
TestRailsBase < TestRailUtils < HPETestRails < PyTestRails
```

Each one of these class/files is descripted bellow:

* TestRailBase is based on TestRail examples for the two basic operations that TestRail API support: get, set, as well as keep track of connection stuff
* TestRailUtils contains all the basic Verbs that we can issue against TestRail API. New Verbs should be created here. NO project or HPE related things should be defined here
* HPETestRails contains all HPE related operations, config files loading, default URLs and project definitions as well as common business operations regarding the ways we want Testrail to be organized.
* PyTestRail class/file was maintained to keep legacy compatibility with previous uses. This file also contains a CLI operation mode that was keet without changes.
* TestRail_defines file contains base types and enums defined to be used close together with TestRails