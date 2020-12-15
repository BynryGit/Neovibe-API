from django.shortcuts import render


# Create your views here.
def a():
    ab = {
        "roles":[
            {
                "name" : "role1",
                "id_string" : "",
                "modules" : [
                    {
                        "module" : "S&M",
                        "submodules" : [
                            {
                                "name" : "sub_module1",
                                "privileges" : [
                                    {
                                        "access" : "View"
                                    }
                                ]
                            }
                        ]
                    },
                    {
                        "module": "S&M",
                        "submodules": [
                            {
                                "name": "sub_module1",
                                "privileges": [
                                    {
                                        "access": "View"
                                    }
                                ]
                            }
                        ]
                    }
                ]
            }
        ]
    }


cd = {
    "modules" : [
        {
            "module" : "S&M",
            "submodules" : [
                {
                    "name" : "submodule1",
                    "privileges" : [
                        {
                            "access" : "view"
                        }
                    ],
                    "role" : {
                        "name" : "admin"
                    }
                }
            ]
        },
        {
            "module" : "S&M",
            "submodules" : [
                {
                    "name" : "submodule1",
                    "privileges" : [
                        {
                            "access" : "view"
                        }
                    ],
                    "role" : {
                        "name" : "admin"
                    }
                }
            ]
        }
    ]
}
