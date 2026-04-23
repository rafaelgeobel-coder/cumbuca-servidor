import requests
import time
import os
import json

URL = "https://cumbuca-servidor.up.railway.app/pedidos"
PASTA_DESTINO = r"C:\exe4_0\pedidos_entrada"

os.makedirs(PASTA_DESTINO, exist_ok=True)

baixados = set()

while True:
    try:
        r = requests.get(URL)
        pedidos = r.json()

        for pedido in pedidos:
            nome = pedido.get("cliente", "sem_nome")

            nome_arquivo = f"{nome}_{hash(str(pedido))}.json"
            caminho = os.path.join(PASTA_DESTINO, nome_arquivo)

            if nome_arquivo not in baixados:
                with open(caminho, "w", encoding="utf-8") as f:
                    json.dump(pedido, f, indent=2, ensure_ascii=False)

                print("Baixado:", nome_arquivo)
                baixados.add(nome_arquivo)

    except Exception as e:
        print("Erro:", e)

    time.sleep(5)