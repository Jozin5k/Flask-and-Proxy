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

## Como instalar e usar

### 1. O Passo Zero: Instalando o Python
Como este projeto usa a linguagem Python, você precisará ter o Python instalado no seu computador para que os comandos funcionem.
* **Se você usa Windows ou Mac:** Baixe e instale a versão mais recente diretamente do site oficial (python.org). *Dica importante no Windows: Marque a caixinha "Add Python to PATH" durante a instalação!*
* **Se você usa Linux:** O Python geralmente já vem instalado. Você pode garantir que o gerenciador de pacotes está pronto abrindo o terminal e digitando: `sudo apt install python3 python3-pip`.

### 2. Preparando o terreno (Instalação)
Aqui na página do projeto no GitHub, baixe o arquivo zip contendo todos os arquivos necessários clicando em Download ZIP que pode ser acessado no botão verde Code no começo da página, logo extraia todos os arquivos em uma pasta.
Com o Python e seu gerenciador prontos, abra o terminal ou prompt de comando na pasta do projeto e instale as ferramentas necessárias rodando:

```bash
pip install -r requirements.txt
```

### 3. Como usar
Para ativar o proxy, execute o comando abaixo no seu terminal:

```bash
python proxy.py
```

### 4. Navegação
Com o sistema ligado, você não digita o endereço do site direto no navegador de forma convencional. Você precisa "pedir" para o proxy buscar a página para você.  Em vez de acessar diretamente um site, você vai digitar o seguinte formato na sua barra de endereços:

```
http://localhost:5000/http://www.site.com
```

## Como personalizar os filtros
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

## Tecnologia Utilizada
O projeto foi construído em Python utilizando uma ferramenta chamada **Flask**. Escolhemos essa combinação porque ela foi a tecnologia base trabalhada em aula, oferecendo uma estrutura simples para criar rotas de comunicação. Também utilizamos a biblioteca **requests** que funciona como o nosso "robô" encarregado de ir até a internet e buscar o conteúdo dos sites de origem.

## Vantagens e Dificuldades do Flask frente a alternativas:

### Frente a Sockets TCP puros (Abordagem de Baixo Nível):
Vantagens: Desenvolver o proxy diretamente sobre Sockets TCP exigiria gerenciar manualmente os buffers de leitura, fazer o parsing (leitura interpretada) manual dos cabeçalhos HTTP e estruturar cada resposta do zero. O Flask nos poupa desse trabalho massivo de infraestrutura, entregando uma estrutura de rotas pronta e tratando as requisições HTTP de forma nativa.

Dificuldades: Como o Flask foi desenhado para ser um servidor web tradicional (receber requisições e entregar páginas próprias) e não um Proxy dedicado, tivemos que adaptar o comportamento dele para capturar URLs externas como parâmetros de rota e repassá-las adiante. Ele adiciona uma camada de processamento (overhead) que não existiria em um socket TCP puro focado em alta performance.

### Frente a frameworks equivalentes (como FastAPI ou Django):
Vantagens: O Flask é minimalista e direto ao ponto. Ferramentas como o Django trariam uma estrutura excessivamente pesada e desnecessária para este escopo (como sistemas de banco de dados e autenticação nativos que não possuem utilidade aqui).

Dificuldades: Diferente do FastAPI, que possui suporte nativo e moderno para operações assíncronas (permitindo lidar com múltiplas requisições simultâneas de forma muito eficiente), o Flask por padrão lida com as requisições de forma mais síncrona/bloqueante, o que limita a velocidade se muitos acessos simultâneos fossem feitos através do proxy.

## Uso de Inteligência Artificial no Projeto
Para o desenvolvimento deste trabalho, unimos nossa base de programação com o auxílio de assistentes de Inteligência Artificial, utilizando-os como ferramentas de aprendizado e refinamento:

Claude (Anthropic): Como já tínhamos experiência prévia com a base de Python, HTML e JavaScript, focamos o uso do Claude para nos ajudar a dar os primeiros passos com o framework Flask. A IA foi fundamental para nos ensinar a configurar o servidor inicial (app Flask), organizar a estrutura dos arquivos para uma leitura melhor e legível, e nos sugerir quais bibliotecas seriam mais apropriadas para este trabalho.

Gemini (Google): Utilizado na etapa final do projeto para analisar e traduzir a linguagem estritamente técnica para um formato de README mais acessível e compreensível a qualquer pessoa, além de atuar na revisão estrutural e correção ortográfica do nosso relatório técnico.

## Limitação Importante (Sites com Cadeado / HTTPS)
Este sistema só funciona com sites que utilizam o protocolo **HTTP simples**.

Sabe aquele "cadeado de segurança" que aparece na barra de endereços da maioria dos sites modernos (HTTPS)? Ele indica que o site é criptografado. Como o nosso sistema preza pela segurança original do site, ele não consegue ler nem modificar essas páginas protegidas, fazendo com que elas não funcionem através deste proxy.

O protocolo HTTPS utiliza TLS/SSL para garantir uma comunicação cifrada de ponta a ponta (end-to-end). Para que este proxy fosse capaz de funcionar com HTTPS e interceptar e filtrar o conteúdo do HTML, seriam necessárias duas modificações estruturais complexas:

### 1. Implementação do Método CONNECT:
O proxy precisaria parar de agir como um intermediário comum de requisições GET/POST e passar a estabelecer um túnel cego de comunicação TCP bidirecional através do método HTTP CONNECT.

### 2. Interceptação SSL (Man-in-the-Middle):
Para ler e modificar o HTML filtrando os palavrões, o proxy precisaria quebrar a criptografia. Isso exigiria gerar certificados SSL falsificados dinamicamente para cada domínio acessado, além de obrigar o cliente/navegador a instalar e confiar em uma Autoridade Certificadora (CA) raiz gerada pelo próprio proxy. Do contrário, o navegador bloquearia o acesso acusando uma quebra de segurança severa.
