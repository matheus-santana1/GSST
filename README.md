# 🚀 Guia de Instalação do Ambiente Python

Este projeto utiliza **Python isolado via `pyenv` + `venv`** para garantir compatibilidade, estabilidade e facilidade de
deploy.

---

## 📌 1. Listar as versões mais recentes do Python

```bash
pyenv install --list | grep -E "^[[:space:]]*3\.[0-9]+\.[0-9]+$" | tail -n 10
```

---

## ⬇️ 2. Instalar a versão recomendada

```bash
pyenv install 3.13.2
```

---

## 🌍 3. Definir o Python global do sistema

```bash
pyenv global 3.13.2
```

Verifique:

```bash
python --version
```

---

## 📦 4. Criar ambiente virtual do projeto

```bash
python -m venv .venv
```

---

## 🔌 5. Ativar o ambiente virtual

```bash
source .venv/bin/activate
```

Ao ativar, o terminal exibirá:

```
(.venv)
```

---

## 🧪 6. Validar o Python ativo

```bash
which python
```

Resultado esperado:

```
.../seu_projeto/.venv/bin/python
```

---

## 📁 7. (Opcional) Salvar dependências

```bash
pip freeze > requirements.txt
```

---

## 🚪 8. Sair do ambiente virtual

```bash
deactivate
```

---

## ✅ Ambiente pronto!

Agora seu projeto está usando um **Python totalmente isolado, reprodutível e seguro para produção e deploy**.