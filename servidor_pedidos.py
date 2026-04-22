from http.server import BaseHTTPRequestHandler, HTTPServer
import json
import os
import time

PASTA = r"C:\exe4_0\pedidos_entrada"
os.makedirs(PASTA, exist_ok=True)

class Handler(BaseHTTPRequestHandler):

    # 🔥 RESOLVE O ERRO OPTIONS (CORS)
    def do_OPTIONS(self):
        self.send_response(200)
        self.send_header("Access-Control-Allow-Origin", "*")
        self.send_header("Access-Control-Allow-Methods", "POST, OPTIONS")
        self.send_header("Access-Control-Allow-Headers", "Content-Type")
        self.end_headers()

    def do_GET(self):
        try:
            caminho = self.path
    
            # 🔥 REMOVE PARÂMETROS (?t=123 etc)
            if "?" in caminho:
                caminho = caminho.split("?")[0]
    
            if caminho == "/":
                caminho = "/index.html"
    
            caminho = caminho.lstrip("/")
    
            with open(caminho, "rb") as f:
    
                if caminho.endswith(".html"):
                    content_type = "text/html"
                elif caminho.endswith(".css"):
                    content_type = "text/css"
                elif caminho.endswith(".js"):
                    content_type = "application/javascript"
                elif caminho.endswith(".json"):
                    content_type = "application/json"
                elif caminho.endswith(".png"):
                    content_type = "image/png"
                elif caminho.endswith(".jpg") or caminho.endswith(".jpeg"):
                    content_type = "image/jpeg"
                else:
                    content_type = "application/octet-stream"
    
                self.send_response(200)
                self.send_header("Content-Type", content_type)
                self.end_headers()
    
                self.wfile.write(f.read())
    
        except Exception as e:
            print("Erro GET:", e)
            self.send_response(404)
            self.end_headers()

    def do_POST(self):
        if self.path == "/pedido":
            content_length = int(self.headers.get('Content-Length', 0))
            body = self.rfile.read(content_length)

            try:
                pedido = json.loads(body)

                nome_arquivo = f"pedido_{int(time.time() * 1000)}.json"
                caminho = os.path.join(PASTA, nome_arquivo)

                with open(caminho, "w", encoding="utf-8") as f:
                    json.dump(pedido, f, indent=2, ensure_ascii=False)

                self.send_response(200)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()

                self.wfile.write(b"OK")

                print("Pedido salvo:", caminho)

            except Exception as e:
                self.send_response(500)
                self.send_header("Access-Control-Allow-Origin", "*")
                self.end_headers()

                self.wfile.write(str(e).encode())

# 🔥 RODA SERVIDOR
server = HTTPServer(("0.0.0.0", 5000), Handler)
print("Servidor rodando na porta 5000...")
server.serve_forever()