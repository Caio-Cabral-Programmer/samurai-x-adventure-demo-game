# Guia de Python, Ambiente Virtual e Execução do Projeto Samurai

## 1. Análise rápida do projeto

Este projeto é um jogo em `pygame`.

- Arquivo de entrada: `main.py`
- Módulos do jogo: `objects.py`
- Recursos visuais e sons: `Assets/` e `Sounds/`
- Dependência principal: `pygame`

Observação: o jogo usa caminhos relativos como `Assets/...` e `Sounds/...`, então execute o comando na raiz do projeto (a pasta `Samurai-game`).

## 2. Qual versão do Python você tem

Foi verificado no seu ambiente:

- `python --version` -> `Python 3.13.5`
- `py --version` -> `Python 3.13.5`
- Executável ativo -> `C:\Python313\python.exe`

Também foi validado:

- `pip` funcionando
- `pygame 2.6.1` instalado e importando corretamente

## 3. Vale a pena atualizar o Python agora?

Resposta curta: **não é necessário atualizar agora** para este projeto.

Motivos:

- O projeto já roda com `Python 3.13.5`.
- `pygame` está funcionando no seu ambiente atual.
- Atualizar sem necessidade pode introduzir incompatibilidades desnecessárias.

Quando atualizar:

- Quando sair correção de segurança importante.
- Quando você começar um novo projeto e quiser padronizar em uma versão específica.
- Quando alguma biblioteca exigir versão mais nova.

## 4. `venv` ou `.venv`? O que é mais profissional?

Use **`.venv`** na raiz do repositório.

Por que `.venv` é melhor na prática profissional:

- É um padrão muito comum em times Python.
- Fica oculto por começar com ponto.
- Fácil de ignorar no Git (`.gitignore`).
- Ferramentas como VS Code detectam bem esse padrão.

Resumo:

- Tecnicamente, `venv` e `.venv` funcionam igual.
- Profissionalmente, prefira `.venv`.

## 5. Como rodar o projeto (Windows + PowerShell)

Na pasta do projeto (`Samurai-game`), execute:

```powershell
python -m venv .venv
```

Ative o ambiente virtual:

```powershell
.\\.venv\\Scripts\\Activate.ps1
```

Se der erro de política de execução no PowerShell, rode apenas para a sessão atual:

```powershell
Set-ExecutionPolicy -Scope Process -ExecutionPolicy Bypass
.\\.venv\\Scripts\\Activate.ps1
```

Instale dependência:

```powershell
python -m pip install --upgrade pip
python -m pip install pygame
```

Execute o jogo:

```powershell
python main.py
```

Para sair do ambiente virtual:

```powershell
deactivate
```

## 6. Boas práticas recomendadas

1. Criar um `requirements.txt` para fixar dependências:

```powershell
python -m pip freeze > requirements.txt
```

2. Em outra máquina, instalar tudo com:

```powershell
python -m pip install -r requirements.txt
```

3. Garantir que o ambiente virtual não vá para o Git. Exemplo de `.gitignore`:

```gitignore
.venv/
__pycache__/
*.pyc
```

## 7. Comandos de diagnóstico úteis

```powershell
python --version
py --version
python -m pip --version
python -c "import pygame; print(pygame.__version__)"
```

## 8. Conclusão objetiva

- Sua versão atual: `Python 3.13.5`.
- Para este projeto: pode manter essa versão.
- Padrão profissional para ambiente virtual: usar `.venv` na raiz do projeto.
- Comandos para rodar: criar `.venv`, ativar, instalar `pygame`, executar `python main.py`.
