
#from email import policy

try:
    import espdm.urequests as requests
except:
    import requests

import json 

class PolicyClient:

    def __init__(self, device_id, filename="config.json"):
        self.device_id = device_id
        self.filename = filename+".sha256"
        self.policyname = filename

    def load_hash(self):
        try:
            f = open(self.filename,"r")
            hash = f.read()
            f.close()
            return hash
        except:
            return None

    def save_hash(self, hash):
        f = open(self.filename,"w")
        f.write(hash)
        f.close()

    def save_policy(self, policy):
        f = open(self.policyname,"w")
        f.write(json.dumps(policy, indent=2))
        f.close()


    def download_policy_hash(self):
        req = requests.get("http://localhost:8080/policy/check/"+self.device_id+"/")
        if req.status_code == 200:
            data = req.json()
            return data["hash"]
        else:
            return None

    def download_policy(self):
        req = requests.get("http://localhost:8080/policy/"+self.device_id+"/")
        if req.status_code == 200:
            data = req.json()
            return data
        else:
            return None

    def auto_check(self):
        local = self.load_hash()
        remote = self.download_policy_hash()

        # If the policy hash is not found local then save it. 
        if not local:
            self.save_hash(remote)

        # If local != remote the save the NEW policy and hash
        if local != remote:
            policy = self.download_policy()
            if policy:
                self.save_policy(policy)
                self.save_hash(remote)






pc = PolicyClient("RELAY-7C9EBDF43F50")
pc.auto_check()

