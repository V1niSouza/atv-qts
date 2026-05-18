# 📦 Projeto Testes - CI/CD

Este projeto é uma aplicação web desenvolvida em Flask, estruturada para facilitar o desenvolvimento, testes e manutenção. Ele inclui configuração de ambiente virtual, execução local e suíte de testes automatizados (incluindo testes E2E).

---

## 🚀 Como executar o projeto localmente

### 1. Criar ambiente virtual

Windows:
```bash
python -m venv venv
venv\Scripts\activate
```

Linux:
```bash
python3 -m venv venv
source venv/bin/activate
```
---

### 2. Instalar dependências
```bash
pip install -r requirements.txt
```
---

### 3. Executar a aplicação
```bash
python run.py
```
A aplicação estará disponível em: http://127.0.0.1:5000

---

## 🧪 Testes e qualidade de código
```bash
black .
flake8 .
pytest
```
---

### ⚠️ Observação sobre testes E2E

Os testes E2E iniciam automaticamente o servidor Flask durante o pytest, então não é necessário manter a aplicação rodando com python run.py.

---

## 📌 Tecnologias utilizadas

- Python
- Flask
- Pytest
- Black
- Flake8

---

## Autor

Vinícius Souza Ramos
