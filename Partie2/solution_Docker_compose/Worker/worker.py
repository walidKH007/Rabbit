import requests,json,docker,time,sys,os
from git import Repo


def get_tache(file):
    try:
        r = requests.get("http://192.168.56.101:5000/rabbit/get_queue/"+file)
    except Exception as e:
        return "False"
    return r.text

def send_msg(resultat,file):
    param = {"data" : json.dumps(resultat)}
    r = requests.post("http://192.168.56.101:5000/rabbit/"+file,data=param)
    print(r.text)

def exec_tache(git_url,repo_dir, client, image_name, commande):
    try:
        repo = Repo(repo_dir)
        for url in repo.remotes.origin.urls:
            if url==git_url:
                print("Repository already cloned")
    except Exception as e:
        repo = Repo.clone_from(git_url, repo_dir)
        print("clone done.")
        repo.remotes.origin.pull()
        print("pull done.")
        client.images.build(path=repo_dir,tag=image_name)
        print("build done.")
        resultat=client.containers.run(image=image_name, command=commande, detach=False, auto_remove=True)
        print("container execute.")
        resultat_json={}
        resultat_json["tache_id"] = int(tache_json["tache_id"])
        resultat_json["soustache_id"] = int(tache_json["soustache_id"])
        resultat_json["result"] = resultat.decode().strip('\n')
        print(resultat_json)
        send_msg(resultat_json,"Done")



client = docker.from_env()
image_name = "n_queue"
repo_workdir = "walid_test_queue"
    
tache = get_tache("ToDo")
print(tache)
tache_json = json.loads(tache)
exec_tache(tache_json["git"],repo_workdir, client, image_name, tache_json["cmd"])
