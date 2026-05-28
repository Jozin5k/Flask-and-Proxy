# Web Proxy com Controle de Conteúdo

Trabalho do 1º Bimestre — Sistemas para Internet 2 — FURG 2026/1

## O que o projeto faz

É um proxy HTTP feito em Python com Flask. O proxy fica entre o navegador e a internet e pode fazer três coisas dependendo do site acessado:

- Repassar o conteúdo normalmente
- Bloquear o acesso se o domínio estiver na lista negra
- Filtrar palavrões do HTML antes de entregar pro cliente

## Arquivos

- `proxy.py` — código principal do proxy
- `blocked.json` — lista de domínios bloqueados
- `words.json` — palavrões e suas substituições
- `log.json` — gerado automaticamente, registra todos os acessos

## Como instalar

```bash
pip install -r requirements.txt
```

## Como usar

Rode o proxy:

```bash
python proxy.py
```

Acesse sites pelo proxy no navegador:

```
http://localhost:5000/http://www.site.com
```

## Configurando os filtros

Para bloquear um site, adicione o domínio no `blocked.json`:

```json
{
  "bloqueados": ["www.sitex.com", "redes-sociais.net"]
}
```

Para filtrar palavrões, edite o `words.json`:

```json
{
  "merda": "macacos me mordam",
  "idiota": "ingênuo"
}
```

## Tecnologia escolhida

Usamos Python com Flask porque foi a tecnologia vista em aula e tem uma forma simples de criar rotas HTTP. A biblioteca `requests` foi usada para buscar o conteúdo dos sites de origem.

## Limitação com HTTPS

O proxy só funciona com sites HTTP. Sites HTTPS não funcionam porque o conteúdo é criptografado — o proxy não consegue ler nem modificar o HTML. Para funcionar com HTTPS seria necessário implementar o método CONNECT e usar certificados SSL.
