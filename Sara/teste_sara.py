import requests
res = requests.post("http://localhost:8001/responder",
                    json={"mensagem": "Olá Sara, estás aí?", "emissor": "utilizador"})
print(res.json())