# 📝 Taskly

Um site de **To-Do List** moderno e eficiente, construído com Django, Docker, PostgreSQL e hospedado na **Google Cloud Platform (GCP)**.

🔗 Acesse o site em produção: [Taskly](https://taskly-205948654599.southamerica-east1.run.app)

---

## ✨ Funcionalidades

- ✅ Criação, edição e exclusão de tarefas
- 🔐 Autenticação de usuários (login e logout)
- 💾 Cache de tarefas para usuários não autenticados (modo visitante)
- 📦 Backend robusto com Django + PostgreSQL
- 🐳 Containerizado com Docker
- ☁️ Deploy na Google Cloud (Cloud Run)

---

## 🛠️ Tecnologias Utilizadas

- [Python 3.11+](https://www.python.org/)
- [Django 4+](https://www.djangoproject.com/)
- [PostgreSQL](https://www.postgresql.org/)
- [Docker](https://www.docker.com/)
- [Google Cloud Platform (Cloud Run)](https://cloud.google.com/run)
- Cache: `locmem` (ou Redis, dependendo da configuração)

---

## 🚀 Como rodar localmente

### Pré-requisitos

- Docker e Docker Compose instalados
- Git

### Passos

```bash
# Clone o repositório
git clone https://github.com/Kabadayan/taskly
