# COMANDOS PARA RODAR NO VS CODE (WINDOWS)

1. python -m venv .venv --without-pip (Cria o .venv)

2. Set-ExecutionPolicy -Scope Process -ExecutionPolicy RemoteSigned (Liberar para o Windonws)

3. .\.venv\Scripts\Activate.ps1 (Ativa o .venv)

4. pip install -r requirements.txt (Instala as dependências do arquivo requirements.txt)

5. uvicorn main:app --reload (Inicia o servidor uvicorn)