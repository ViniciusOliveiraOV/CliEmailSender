# 📬 SecureEmailSender

Envia e-mails com anexos via **Gmail OAuth2**, de forma segura, rápida e totalmente via CLI. Ideal para devs que precisam zipar e mandar projetos automaticamente, com autenticação moderna e sem armazenar senha no código.

## ⚙️ Tecnologias

- Python 3.11+
- Gmail API via OAuth2
- `google-auth`, `google-auth-oauthlib`
- SMTP com `smtplib`
- MIME attachments
- `.zip` automático do projeto
- Execução via terminal

---

## 🚀 Como usar

### 1. Clone o repositório

```bash
git clone https://github.com/seu-user/SecureEmailSender.git
cd SecureEmailSender

python -m venv venv
source venv/bin/activate
pip install google-auth google-auth-oauthlib google-api-python-client
```

4. Configure o Google OAuth2

    Vá até Google Cloud Console

    Crie um projeto

    Ative a Gmail API

    Vá em OAuth consent screen → configure como External/Internal

    Vá em Credentials → Create OAuth Client ID → escolha Desktop App

    Baixe o arquivo credentials.json e coloque na raiz do projeto

🧪 Enviar email zipado (modo CLI)

```
python send_email.py
```


O script irá:

    Solicitar o caminho do diretório a ser zipado

    Criar um .zip do conteúdo

    Pedir o email remetente e destinatário

    Autenticar com Gmail via navegador (OAuth2)

    Enviar o email com o .zip como anexo



