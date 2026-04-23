from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import time

# Se rodar no Railway, usa o diretório atual; se rodar no PC, usa o caminho que você preferir
if os.name == 'nt':  # Windows
    PASTA = r"C:\exe4_0\pedidos_entrada"
else:  # Linux (Railway)
    PASTA = "pedidos_entrada"

os.makedirs(PASTA, exist_ok=True)

class Handler(BaseHTTPRequestHandler):

    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*") # <--- AQUI
        self.send_header("Access-Control-Allow-Methods", "POST, GET, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_POST(self):
        if self.path == "/pedido":
            # ... (seu código que lê e salva o JSON) ...
            
            try:
                # ... (lógica de salvar o arquivo) ...

                # AQUI É O SEGREDO:
                self.send_response(200)
                self.send_header("Access-Control-Allow-Origin", "*") # <--- ADICIONE ISSO
                self.send_header("Content-Type", "text/plain")
                self.end_headers()
                self.wfile.write(b"OK")
            except Exception as e:
                self.send_response(500)
                self.send_header("Access-Control-Allow-Origin", "*") # <--- E ISSO NO ERRO TAMBÉM
                self.end_headers()
                self.wfile.write(str(e).encode())

    def do_GET(self):
        try:
            # Limpa o caminho de parâmetros como ?t=123
            caminho = self.path.split("?")[0]

            # 1. Rota especial para listar pedidos salvos
            if caminho == "/pedidos":
                arquivos = os.listdir(PASTA_PEDIDOS)
                lista = []
                for nome in arquivos:
                    if nome.endswith(".json"):
                        with open(os.path.join(PASTA_PEDIDOS, nome), "r", encoding="utf-8") as f:
                            lista.append(json.load(f))
                
                self.send_response(200)
                self.send_header("Content-Type", "application/json")
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(json.dumps(lista).encode())
                return

            # 2. Servir arquivos estáticos (HTML, JSON do cardápio, Imagens)
            if caminho == "/":
                caminho = "/index.html"
            
            # Remove a barra inicial para abrir o arquivo na pasta local
            caminho_arquivo = caminho.lstrip("/")
            
            if os.path.exists(caminho_arquivo):
                with open(caminho_arquivo, "rb") as f:
                    self.send_response(200)
                    
                    # Define o tipo de conteúdo baseado na extensão
                    if caminho_arquivo.endswith(".html"):
                        self.send_header("Content-Type", "text/html")
                    elif caminho_arquivo.endswith(".json"):
                        self.send_header("Content-Type", "application/json")
                    elif caminho_arquivo.endswith(".png"):
                        self.send_header("Content-Type", "image/png")
                    elif caminho_arquivo.endswith(".jpg") or caminho_arquivo.endswith(".jpeg"):
                        self.send_header("Content-Type", "image/jpeg")
                    
                    self.send_header("Access-Control-Allow-Origin", "*")
                    self.end_headers()
                    self.wfile.write(f.read())
                return
            else:
                self.send_response(404)
                self.end_headers()

        except Exception as e:
            print("Erro no GET:", e)
            self.send_response(500)
            self.end_headers()

    def do_POST(self):
        if self.path == "/pedido":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)

            try:
                pedido = json.loads(body)
                nome_arquivo = f"pedido_{int(time.time() * 1000)}.json"
                caminho_completo = os.path.join(PASTA_PEDIDOS, nome_arquivo)

                with open(caminho_completo, "w", encoding="utf-8") as f:
                    json.dump(pedido, f, indent=2, ensure_ascii=False)

                self.send_response(200)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(b"OK")
                print("Pedido recebido e salvo em:", caminho_completo)

            except Exception as e:
                print("Erro ao processar POST:", e)
                self.send_response(500)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()
                self.wfile.write(str(e).encode())

# Inicialização do servidor
PORT = int(os.environ.get("PORT", 5000))
server = HTTPServer(("0.0.0.0", PORT), Handler)
print(f"Servidor Sabores Cumbuca ativo na porta {PORT}")
print(f"Acesse o site em: http://localhost:{PORT}")
server.serve_forever()