# Настраиваем dns для нового поддомена
# ...

# Настраиваем ssl для нового поддомена
sudo certbot certonly --nginx -d protectchannelgroupbot.shashkovs.ru
   # /etc/letsencrypt/live/protectchannelgroupbot.shashkovs.ru/fullchain.pem
   # Your key file has been saved at:
   # /etc/letsencrypt/live/protectchannelgroupbot.shashkovs.ru/privkey.pem


# Содержимое каждого сайта будет находиться в собственном каталоге, поэтому создаём нового пользователя
sudo useradd protectchannelgroupbot -b /web/ -m -U -s /bin/false

# Он таки будет логиниться через SSH
sudo chsh -s /bin/bash protectchannelgroupbot
sudo passwd protectchannelgroupbot
... # dnnVE9MjmvfN958Jz7WbjGTV

# Делаем юзера и его группу владельцем  всех своих папок
# Делаем так, чтобы всё новое лежало в группе
# Изменяем права доступа на каталог
sudo chown -R protectchannelgroupbot:protectchannelgroupbot /web/protectchannelgroupbot
sudo chmod -R 2770 /web/protectchannelgroupbot
sudo find /web/protectchannelgroupbot -type d -exec chmod 2770 '{}' \;
sudo setfacl -R -d -m group:protectchannelgroupbot:rwx /web/protectchannelgroupbot
sudo setfacl -R -m group:protectchannelgroupbot:rwx /web/protectchannelgroupbot


# Чтобы Nginx получил доступ к файлам сайта, добавим пользователя nginx в группу
sudo usermod -a -G protectchannelgroupbot nginx
sudo usermod -a -G protectchannelgroupbot serge
sudo usermod -a -G protectchannelgroupbot root













# Создаём ключ для ssh+github
sudo mkdir /web/protectchannelgroupbot/.ssh
sudo chmod 0700 /web/protectchannelgroupbot/.ssh
sudo touch /web/protectchannelgroupbot/.ssh/authorized_keys
sudo chmod 0644 /web/protectchannelgroupbot/.ssh/authorized_keys
sudo ssh-keygen -t ed25519 -C "protectchannelgroupbot@protectchannelgroupbot.shashkovs.ru"
  /web/protectchannelgroupbot/.ssh/protectchannelgroupbot_rsa_key_for_github

sudo chmod 0600 /web/protectchannelgroupbot/.ssh/protectchannelgroupbot_rsa_key_for_github

sudo cat /web/protectchannelgroupbot/.ssh/protectchannelgroupbot_rsa_key_for_github.pub
sudo nano /web/protectchannelgroupbot/.ssh/authorized_keys
 ...
# Копируем ключ для гитхаба
sudo cat /web/protectchannelgroupbot/.ssh/protectchannelgroupbot_rsa_key_for_github.pub
# Вставляем в deploy keys https://github.com/ShashkovS/protectchannelgroupbot/settings/keys

# Создаём настройки для github'а
sudo touch /web/protectchannelgroupbot/.ssh/config
sudo chmod 0644 /web/protectchannelgroupbot/.ssh/config
sudo nano /web/protectchannelgroupbot/.ssh/config
Host github.com
  IdentityFile /web/protectchannelgroupbot/.ssh/protectchannelgroupbot_rsa_key_for_github

sudo chown -R protectchannelgroupbot:protectchannelgroupbot /web/protectchannelgroupbot/.ssh





# Перелогиниваемся


# Клонируем репу
cd /web/protectchannelgroupbot
sudo -H -u protectchannelgroupbot git clone git@github.com:ShashkovS/protectchannelgroupbot.git protectchannelgroupbot
cd /web/protectchannelgroupbot/protectchannelgroupbot
sudo -H -u protectchannelgroupbot git pull

# виртуальное окружение
cd /web/protectchannelgroupbot
export LD_LIBRARY_PATH=/usr/local/lib # Это для того, чтобы использовать свежий sqlite!
python3.12 -m venv --without-pip protectchannelgroupbot_env
source /web/protectchannelgroupbot/protectchannelgroupbot_env/bin/activate.fish
curl https://bootstrap.pypa.io/get-pip.py | /web/protectchannelgroupbot/protectchannelgroupbot_env/bin/python3.12
deactivate
source /web/protectchannelgroupbot/protectchannelgroupbot_env/bin/activate.fish
pip install --upgrade -r protectchannelgroupbot/requirements.txt
deactivate


# Cекреты
cd /web/protectchannelgroupbot/protectchannelgroupbot
sudo nano backend/creds_prod/bot_config_prod.json
{
  "config_name": "protectchannelgroupbot_prod",

  "telegram_bot_name": "protectchannelgroupbot",
  "telegram_bot_token": "6969370262:XXX",

  "use_webhooks": true,
  "webhook_host": "protectchannelgroupbot.shashkovs.ru",
  "webhook_port": 443,
  "db_filename": "../db/protectchannelgroupbot.sqlite",
  "exceptions_channel_public": "@qwqw",
  "exceptions_channel": -999,
  "sos_channel_public": "@qwqw",
  "sos_channel": -999,
  "set_admin_password": "XXX",
  "sentry_dsn": ""
}






# Делаем юзера и его группу владельцем  всех своих папок
sudo chown -R protectchannelgroupbot:protectchannelgroupbot /web/protectchannelgroupbot
# Делаем так, чтобы всё новое лежало в группе





# Настраиваем systemd для поддержания приложения в рабочем состоянии
# Начинаем с описания сервиса
tee /web/protectchannelgroupbot/gunicorn.protectchannelgroupbot.service << EOF
[Unit]
Description=Gunicorn instance to serve protectchannelgroupbot
After=network.target

[Service]
PIDFile=/web/protectchannelgroupbot/protectchannelgroupbot.pid
Restart=always
RestartSec=0
User=protectchannelgroupbot
Group=nginx
RuntimeDirectory=gunicorn
WorkingDirectory=/web/protectchannelgroupbot/protectchannelgroupbot/backend/src
Environment="PATH=/web/protectchannelgroupbot/protectchannelgroupbot_env/bin"
Environment="PROD=true"
Environment="LD_RUN_PATH=/usr/local/lib"
Environment="LD_LIBRARY_PATH=/usr/local/lib"
ExecStart=/web/protectchannelgroupbot/protectchannelgroupbot_env/bin/gunicorn  --pid /web/protectchannelgroupbot/protectchannelgroupbot.pid  --workers 1  --bind unix:/web/protectchannelgroupbot/protectchannelgroupbot.socket --worker-class aiohttp.GunicornUVLoopWebWorker -m 007  main:app
ExecReload=/bin/kill -s HUP \$MAINPID
ExecStop=/bin/kill -s TERM \$MAINPID
PrivateTmp=true

[Install]
WantedBy=multi-user.target
EOF

sudo ln -s /web/protectchannelgroupbot/gunicorn.protectchannelgroupbot.service /etc/systemd/system/gunicorn.protectchannelgroupbot.service

# Тестовый запуск
cd /web/protectchannelgroupbot/protectchannelgroupbot/backend/src && sudo -H -u protectchannelgroupbot PROD=true /web/protectchannelgroupbot/protectchannelgroupbot_env/bin/gunicorn  --pid /web/protectchannelgroupbot/protectchannelgroupbot.pid  --workers 1  --bind unix:/web/protectchannelgroupbot/protectchannelgroupbot.socket --worker-class aiohttp.GunicornUVLoopWebWorker -m 007  main:app


# Настраиваем nginx (здесь настройки СТРОГО отдельного домена или поддомена). Если хочется держать в папке, то настраивать nginx нужно по-другому
tee /web/protectchannelgroupbot/protectchannelgroupbot.conf << EOF
    server {
        listen [::]:443 ssl http2; # managed by Certbot
        listen 443 ssl http2; # managed by Certbot
        server_name protectchannelgroupbot.shashkovs.ru; # managed by Certbot

        ssl_certificate /etc/letsencrypt/live/protectchannelgroupbot.shashkovs.ru/fullchain.pem; # managed by Certbot
        ssl_certificate_key /etc/letsencrypt/live/protectchannelgroupbot.shashkovs.ru/privkey.pem; # managed by Certbot
        include /etc/letsencrypt/options-ssl-nginx.conf; # managed by Certbot
        ssl_dhparam /etc/pki/nginx/dhparam.pem;
        add_header Strict-Transport-Security "max-age=31536000; includeSubDomains; preload" always;

        location / {
          proxy_set_header Host \$http_host;
          proxy_redirect off;
          proxy_buffering off;
          proxy_pass http://unix:/web/protectchannelgroupbot/protectchannelgroupbot.socket;
        }
        location /static {
          root /web/protectchannelgroupbot/protectchannelgroupbot/dist/static;
          try_files $uri $uri/ =404;
        }
    }
EOF

sudo ln -s /web/protectchannelgroupbot/protectchannelgroupbot.conf /etc/nginx/conf.d/protectchannelgroupbot.conf



# Проверяем корректность конфига. СУПЕР-ВАЖНО!
sudo nginx -t
# Перезапускаем nginx
sudo systemctl reload nginx.service


# Говорим, что нужен автозапуск
sudo systemctl enable gunicorn.protectchannelgroupbot
# Запускаем
sudo systemctl start gunicorn.protectchannelgroupbot
sudo journalctl -u gunicorn.protectchannelgroupbot --since "5 minutes ago" -f
# Проверяем
curl --unix-socket /web/protectchannelgroupbot/protectchannelgroupbot.socket http


# Обновление
cd /web/protectchannelgroupbot/protectchannelgroupbot
sudo -H -u protectchannelgroupbot git checkout main
sudo -H -u protectchannelgroupbot git pull
sudo systemctl daemon-reload
sudo systemctl stop gunicorn.protectchannelgroupbot
sudo systemctl start gunicorn.protectchannelgroupbot
sudo journalctl -u gunicorn.protectchannelgroupbot --since "1 minutes ago"


# Настройка
sudo visudo
protectchannelgroupbot ALL=(ALL) NOPASSWD: /usr/bin/systemctl restart gunicorn.protectchannelgroupbot
protectchannelgroupbot ALL=(ALL) NOPASSWD: /usr/bin/journalctl -u gunicorn.protectchannelgroupbot --since *


# Сборка под пользователем
cd /web/protectchannelgroupbot/protectchannelgroupbot
git checkout main
git reset --hard
git clean -f
git pull
source /web/protectchannelgroupbot/protectchannelgroupbot_env/bin/activate
pip install -r requirements.txt
deactivate
#npm set progress=false && npm ci
#npm run build
sudo systemctl restart gunicorn.protectchannelgroupbot
sleep 15
sudo journalctl -u gunicorn.protectchannelgroupbot --since "30 seconds ago"
#curl --unix-socket /web/protectchannelgroupbot/protectchannelgroupbot.socket http
#curl https://protectchannelgroupbot.shashkovs.ru/tester



# онлайн лог
sudo journalctl -u gunicorn.protectchannelgroupbot --since "1 minutes ago" -f
