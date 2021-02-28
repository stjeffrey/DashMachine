import json
from flask import render_template_string
import requests

class OpenMediaVault(object):
    # def __init__(self, url, username, password):
    def __init__(self, url, cookie):
        self.url = url
        # self.username = username
        # self.password = password
        self.cookie = cookie

    def refresh(self):
        # response = requests.post(
        #     self.url + "/rpc.php",
        #     json= {'service':'session','method':'login','params':{'username':self.username,'password':self.password}}
        # )

        # if(response.status_code == 200):
            # cookie = response.cookies.get("X-OPENMEDIAVAULT-SESSIONID")
        self.data = requests.post(
            self.url + "/rpc.php",
            json= {'service':'FileSystemMgmt','method':'enumerateMountedFilesystems','params':{'includeRoot': True}},
            cookies= {"X-OPENMEDIAVAULT-SESSIONID": self.cookie}
        ).json()

class Platform:
    def __init__(self, *args, **kwargs):
        # parse the user's options from the config entries
        for key, value in kwargs.items():
            self.__dict__[key] = value

        if not hasattr(self, "url"):
            print(
                "Please set the url of your OpenMediaVault server"
            )
            exit(1)

        # if not hasattr(self, "username"):
        #     print(
        #         "Please set the username for your OpenMediaVault server"
        #     )
        #     exit(1)

        # if not hasattr(self, "password"):
        #     print(
        #         "Please set the password for your OpenMediaVault server"
        #     )
        #     exit(1)
        
        if not hasattr(self, "cookie"):
            print(
                "Please set the session cookie for your OpenMediaVault server"
            )
            exit(1)

        # self.openmediavault = OpenMediaVault(self.url, self.username, self.password)
        self.openmediavault = OpenMediaVault(self.url, self.cookie)

    def process(self):
        self.openmediavault.refresh()
        value_template = render_template_string(
            self.value_template, **self.openmediavault.__dict__
        )
        return value_template
