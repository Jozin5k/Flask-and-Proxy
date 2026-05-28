import json
import re
from datetime import datetime
from flask import Flask, request, Response
import requests

app = Flask(__name__)

def carregar_bloqueados():
    with open("blocked.json", "r", encoding="utf-8") as f:
        dados = json.load(f)
    return dados["bloqueados"]

def carregar_palavroes():
    with open("words.json", "r", encoding="utf-8") as f:
        return json.load(f)

def salvar_log(url, acao):
    try:
        with open("log.json", "r", encoding="utf-8") as f:
            log = json.load(f)
    except:
        log = []

    log.append({
        "timestamp": datetime.now().isoformat(),
        "url": url,
        "acao": acao
    })

    with open("log.json", "w", encoding="utf-8") as f:
        json.dump(log, f, ensure_ascii=False, indent=2)

def pagina_bloqueio(dominio):
    html = f"""
    <!DOCTYPE html>
    <html lang="pt-BR">
    <head>
        <meta charset="UTF-8">
        <title>Acesso Bloqueado</title>
        <style>
            body {{
                background: #1a1a1a;
                color: white;
                font-family: Arial, sans-serif;
                display: flex;
                justify-content: center;
                align-items: center;
                height: 100vh;
                margin: 0;
            }}
            .caixa {{
                text-align: center;
                border: 2px solid red;
                padding: 40px;
                border-radius: 10px;
            }}
            h1 {{ color: red; }}
            .site {{ color: red; font-family: monospace; margin-top: 10px; }}
        </style>
    </head>
    <body>
        <div class="caixa">
            <h1>🚫 Acesso Bloqueado</h1>
            <p>Este site está bloqueado pelo administrador da rede.</p>
            <div class="site">{dominio}</div>
        </div>
    </body>
    </html>
    """
    return html, 403

def filtrar_conteudo(html, palavroes):
    filtrou = False
    for palavra, substituto in palavroes.items():
        novo, n = re.subn(re.escape(palavra), substituto, html, flags=re.IGNORECASE)
        if n > 0:
            html = novo
            filtrou = True
    return html, filtrou

@app.route("/", defaults={"url_alvo": ""})
@app.route("/<path:url_alvo>")
def proxy(url_alvo):
    if not url_alvo.startswith("http"):
        return "URL invalida. Use: http://localhost:5000/http://www.site.com", 400

    bloqueados = carregar_bloqueados()
    palavroes = carregar_palavroes()

    dominio = url_alvo.split("/")[2]

    # verifica se o dominio esta bloqueado
    if dominio in bloqueados:
        salvar_log(url_alvo, "bloqueado")
        html, status = pagina_bloqueio(dominio)
        return Response(html, status=status, mimetype="text/html")

    # busca o conteudo do site
    try:
        resposta = requests.get(url_alvo, timeout=10, headers={
            "User-Agent": "Mozilla/5.0"
        })
    except Exception as e:
        return f"Erro ao acessar o site: {e}", 502

    content_type = resposta.headers.get("Content-Type", "")

    # se for HTML, aplica o filtro de palavroes
    if "text/html" in content_type:
        resposta.encoding = resposta.apparent_encoding
        html, filtrou = filtrar_conteudo(resposta.text, palavroes)
        acao = "filtrado" if filtrou else "permitido"
        salvar_log(url_alvo, acao)
        return Response(html, status=resposta.status_code, mimetype="text/html")

    # outros tipos de conteudo repassa sem modificar
    salvar_log(url_alvo, "permitido")
    return Response(resposta.content, status=resposta.status_code, content_type=content_type)

if __name__ == "__main__":
    print("Proxy rodando em http://localhost:5000")
    print("Exemplo: http://localhost:5000/http://www.site.com")

    app.run(debug=True, port=5000)
