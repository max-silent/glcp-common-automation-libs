from random import randint


class AuthzAppApiPayload:
    # `app_onboard_min` is a minified version of app_onboard payload
    # that contains the minimal set of information for it
    @staticmethod
    def app_onboard_min(app_id, app_instance_id):
        payload = AuthzAppApiPayload.app_onboard(app_id, app_instance_id)

        for attr in ["permissions", "roles", "application_resources", "scope_resources"]:
            del payload[attr]

        return payload

    # `app_upgrade_min` is a minified version of app_upgrade payload
    # that contains the minimal set of information for it
    @staticmethod
    def app_upgrade_min(app_instance_id):
        payload = AuthzAppApiPayload.app_upgrade(app_instance_id)

        for attr in ["permissions", "roles", "application_resources", "scope_resources"]:
            del payload[attr]

        return payload

    # `app_onboard` is the complete app_onboard payload
    # refer to https://docs.ccs.arubathena.com/internal/authz/#tag/app-instance-on-boarding
    @staticmethod
    def app_onboard(app_id, app_instance_id):
        return {
            "application_id": app_id,
            "app_instance_id": app_instance_id,
            "application_slug": f"authz/app/test-{randint(0,9999)}",
            "broker_url": "/app-service/broker/v1/",
            "version": "1.0",
            "permissions": [
                {
                    "name": "foo",
                    "slug": "my-app.foo.read",
                    "description": "foo permision",
                    "tags": {
                        "hidden": False,
                        "mandatory": False,
                        "default": False,
                        "level": "WORKSPACE",
                    },
                }
            ],
            "application_resources": [
                {
                    "name": "foo",
                    "slug": "/my-app/foo/bar",
                    "description": "foo app resource",
                    "tags": {
                        "hidden": False,
                        "mandatory": False,
                        "level": "WORKSPACE",
                        "programs": ["fooBar"],
                    },
                    "account_types": ["string"],
                    "scope_resources": [{"slug": "/my-app/foo/bar"}],
                    "permissions": [
                        {
                            "slug": "my-app.foo.read",
                            "name": "foo",
                            "description": "foo description",
                            "tags": {
                                "hidden": False,
                                "mandatory": False,
                                "default": False,
                                "level": "WORKSPACE",
                            },
                        }
                    ],
                    "default_permissions": [{"slug": "my-app.foo.read", "name": "foo"}],
                }
            ],
            "scope_resources": [
                {
                    "name": "foo bar",
                    "slug": "/my-app/foo/bar",
                    "description": "foo scope resource",
                    "tags": {
                        "hidden": False,
                        "mandatory": False,
                        "level": "WORKSPACE",
                        "programs": ["string"],
                    },
                    "broker_url": "/app-service/broker/v1/",
                }
            ],
            "roles": [
                {
                    "slug": "fooBar",
                    "name": "string",
                    "description": "string",
                    "tags": {
                        "hidden": False,
                        "tac": False,
                        "activate": False,
                        "ccs": True,
                        "default": False,
                        "no_default_rrp": True,
                        "level": "WORKSPACE",
                        "readonly": False,
                    },
                    "resource_policies": [
                        {
                            "resource": {"matcher": "/my-app/foo/"},
                            "permissions": [
                                {"slug": "my-app.foo.read", "name": "string"}
                            ],
                            "effect": "ALLOW",
                        }
                    ],
                }
            ],
        }

    # `app_upgrade` is the complete app_upgrade payload
    # refer to https://docs.ccs.arubathena.com/internal/authz/#tag/app-instance-application-upgrade
    @staticmethod
    def app_upgrade(app_instance_id):
        return {
            "app_instance_id": app_instance_id,
            "broker_url": "/app-service/broker/v1/",
            "version": "1.0",
            "permissions": {
                "add": [
                    {
                        "name": "foo",
                        "slug": "my-app.foo.read",
                        "description": "foo permission",
                        "tags": {
                            "hidden": False,
                            "mandatory": False,
                            "default": False,
                            "level": "WORKSPACE",
                        },
                    }
                ],
                "update": [
                    {
                        "slug": "my-app.foo.read",
                        "name": "string",
                        "description": "string",
                        "tags": {
                            "hidden": False,
                            "mandatory": False,
                            "default": False,
                            "level": "WORKSPACE",
                        },
                    }
                ],
                "delete": ["string"],
            },
            "application_resources": {
                "add": [
                    {
                        "name": "foo",
                        "slug": "/my-app/foo/bar",
                        "description": "foo app resource",
                        "tags": {
                            "hidden": False,
                            "mandatory": False,
                            "level": "WORKSPACE",
                            "programs": ["string"],
                        },
                        "account_types": ["string"],
                        "scope_resources": [{"slug": "/my-app/foo/bar"}],
                        "permissions": [
                            {
                                "slug": "my-app.foo.read",
                                "name": "string",
                                "description": "string",
                                "tags": {
                                    "hidden": False,
                                    "mandatory": False,
                                    "default": False,
                                    "level": "WORKSPACE",
                                },
                            }
                        ],
                        "default_permissions": [
                            {"slug": "my-app.foo.read", "name": "foo"}
                        ],
                    }
                ],
                "update": [
                    {
                        "slug": "/my-app/foo/bar",
                        "name": "string",
                        "description": "string",
                        "tags": {
                            "hidden": False,
                            "mandatory": False,
                            "level": "WORKSPACE",
                            "programs": ["string"],
                        },
                        "account_types": ["string"],
                        "scope_resources": [{"slug": "/my-app/foo/bar"}],
                        "permissions": {
                            "add": [
                                {
                                    "slug": "my-app.foo.read",
                                    "name": "string",
                                    "description": "string",
                                    "tags": {
                                        "hidden": False,
                                        "mandatory": False,
                                        "default": False,
                                        "level": "WORKSPACE",
                                    },
                                }
                            ],
                            "update": [
                                {
                                    "slug": "my-app.foo.read",
                                    "name": "string",
                                    "description": "string",
                                    "tags": {
                                        "hidden": False,
                                        "mandatory": False,
                                        "default": False,
                                        "level": "WORKSPACE",
                                    },
                                }
                            ],
                        },
                        "default_permissions": [
                            {"slug": "my-app.foo.read", "name": "string"}
                        ],
                    }
                ],
                "delete": ["string"],
            },
            "scope_resources": {
                "add": [
                    {
                        "name": "foo",
                        "slug": "/my-app/foo/bar",
                        "description": "foo scope resource",
                        "tags": {
                            "hidden": True,
                            "mandatory": True,
                            "level": "WORKSPACE",
                            "programs": ["string"],
                        },
                        "broker_url": "/app-service/broker/v1/",
                    }
                ],
                "update": [
                    {
                        "slug": "/my-app/foo/bar",
                        "name": "foo",
                        "description": "foo scope resource",
                        "tags": {
                            "hidden": False,
                            "mandatory": False,
                            "level": "WORKSPACE",
                            "programs": ["string"],
                        },
                        "broker_url": "/app-service/broker/v1/",
                    }
                ],
                "delete": ["string"],
            },
            "roles": {
                "add": [
                    {
                        "slug": "fooBar",
                        "name": "foo",
                        "description": "foo role",
                        "tags": {
                            "hidden": False,
                            "tac": False,
                            "activate": False,
                            "ccs": True,
                            "default": False,
                            "no_default_rrp": True,
                            "level": "WORKSPACE",
                            "readonly": False,
                        },
                        "resource_policies": [
                            {
                                "resource": {"matcher": "/my-app/foo/"},
                                "permissions": [
                                    {"slug": "my-app.foo.read", "name": "foo"}
                                ],
                                "effect": "ALLOW",
                            }
                        ],
                    }
                ],
                "update": [
                    {
                        "slug": "fooBar",
                        "name": "foo",
                        "description": "foo role",
                        "tags": {
                            "hidden": False,
                            "tac": False,
                            "activate": False,
                            "ccs": True,
                            "default": False,
                            "no_default_rrp": True,
                            "level": "WORKSPACE",
                            "readonly": False,
                        },
                        "resource_policies": {"add": [], "update": [], "delete": []},
                    }
                ],
                "delete": ["string"],
            },
        }
