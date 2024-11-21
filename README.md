# PharmacIA  

O **PharmacIA** é um assistente virtual de farmácia desenvolvido para oferecer suporte inteligente e eficiente no Telegram. Ele utiliza inteligência artificial para realizar as tarefas que você precisar de forma prática e personalizada.  

---

## Como Usar  

Siga os passos abaixo para configurar e utilizar o PharmacIA:  

### 1. Configurar o Bot no Telegram  
1. Crie um bot no Telegram usando o [BotFather](https://core.telegram.org/bots#botfather).  
2. Copie o **token de autenticação** gerado para o seu bot.  
3. Dentro do projeto, crie um arquivo chamado `config.py` e insira o seguinte conteúdo:  

```python
TELEGRAM_BOT_TOKEN = 'SeuToken'
```
### 2. Configurar o Ngrok
Crie uma conta no Ngrok e instale o Ngrok no seu computador.
Execute o seguinte comando para expor o servidor local:
```bash
ngrok http 5000
```
Isso gerará um link público, como https://abcd-1234.ngrok.io, que será usado para conectar ao Telegram.

### 3. Conectar o Bot ao Servidor
Instale as dependências do projeto listadas no arquivo requirements.txt:
```bash
pip install -r requirements.txt
```
Registre o webhook do Telegram utilizando o PowerShell:
```powershell
$token = "SeuTokenVaiAqui"
$webhookUrl = "LinkGeradoDoNgrok/webhook"
$telegramApiUrl = "https://api.telegram.org/bot$token/setWebhook"
Invoke-RestMethod -Uri $telegramApiUrl -Method Post -Body @{url = $webhookUrl}
```
4. Executar o Projeto
Inicie o bot executando o arquivo principal do projeto:

```python
app.py
```
Agora, basta enviar uma mensagem para o bot no Telegram para começar a usar o PharmacIA! 🎉

💡 Dica:

Certifique-se de que o token do bot e o link gerado pelo Ngrok estão configurados corretamente.
Caso enfrente problemas, verifique os logs do servidor para identificar erros.
