apt update && apt upgrade -y

apt install sudo curl git nginx mc

копируем конфиг /deploy/infosec.esu.gsp.local в /etc/nginx/sites-available/infosec.esu.gsp.local.conf


ln -s /etc/nginx/sites-available/infosec.esu.gsp.local.conf /etc/nginx/sites-enabled/infosec.esu.gsp.local.conf

установка GitLab Runner из офф репы
wget https://packages.gitlab.com/install/repositories/runner/gitlab-runner/script.deb.sh

bash ./script.deb.sh

apt install gitlab-runner

```bash
sudo mkdir -p /usr/local/share/ca-certificates/gsp.local
sudo wget -O /usr/local/share/ca-certificates/gsp.local/gsp-rca.crt http://cdp.gsp.local/pki/gsp-rca.crt
sudo wget -O /usr/local/share/ca-certificates/gsp.local/gsp-sca1.crt http://cdp.gsp.local/pki/gsp-sca\(1\).crt
openssl x509 -inform der -in /usr/local/share/ca-certificates/gsp.local/gsp-rca.crt -out /usr/local/share/ca-certificates/gsp.local/gsp-rca.pem
openssl x509 -inform der -in /usr/local/share/ca-certificates/gsp.local/gsp-sca1.crt -out /usr/local/share/ca-certificates/gsp.local/gsp-sca1.pem
sudo update-ca-certificates
```

```bash
mkdir -p /etc/docker/certs.d/git.esu.gsp.local/
cp /usr/local/share/ca-certificates/gsp.local/gsp-rca.pem /etc/docker/certs.d/git.esu.gsp.local/gsp-rca.crt
cp /usr/local/share/ca-certificates/gsp.local/gsp-sca1.pem /etc/docker/certs.d/git.esu.gsp.local/gsp-sca1.crt
```

```bash
mkdir -p /etc/docker/certs.d/registry.esu.gsp.local/
cp /usr/local/share/ca-certificates/gsp.local/gsp-rca.pem /etc/docker/certs.d/registry.esu.gsp.local/gsp-rca.crt
cp /usr/local/share/ca-certificates/gsp.local/gsp-sca1.pem /etc/docker/certs.d/registry.esu.gsp.local/gsp-sca1.crt
```


### Настройка авторизации по ключу ssh на целевом хосте (куда деплоить будем)

1. Добавление нового пользователя от имени которого будет осуществляться деплой
```bash
sudo adduser --disabled-password --gecos "" shiki
```
*--disabled-password* – запрещает вход по паролю (можно потом задать через passwd)
*--gecos ""* – пропускает запросы имени и т. д.

Добавление в группу
```bash
sudo usermod -aG www-data shiki
```

2. Генерация SSH-ключа
```bash
mkdir -p /home/shiki/.ssh
ssh-keygen -t ed25519 -C "shiki" -f /home/shiki/.ssh/id_ed25519
```

3. Копируем публичный ключ, и переносим его в переменную $SSH_PRIVATE_KEY на GitLab 
```bash
cat /home/shiki/.ssh/id_ed25519
```

cat /home/shiki/.ssh/id_ed25519.pub >> /home/shiki/.ssh/authorized_keys && chmod 600 /home/shiki/.ssh/authorized_keys


sudo -u shiki chmod 700 /home/shiki/.ssh
sudo -u shiki chmod 600 /home/shiki/.ssh/authorized_keys



3.1. Копирование публичного ключа на сервер (усли ключ генерировался на локальной машине)
```bash
cat /home/ssh_other/id_ed25519.pub | ssh shiki@172.21.32.25 "mkdir -p /home/shiki/.ssh && chmod 700 /home/shiki/.ssh && cat >> /home/shiki/.ssh/authorized_keys && chmod 600 /home/shiki/.ssh/authorized_keys"
```

4. Настройка сервера
```bash
sudo nano /etc/ssh/sshd_config
```

Убедиться, что есть такие настройки:
```
PubkeyAuthentication yes
AuthorizedKeysFile .ssh/authorized_keys
PasswordAuthentication no  # Отключить парольную аутентификацию (опционально)
PermitRootLogin no        # Запретить вход root (рекомендуется)
```

```bash
sudo systemctl restart sshd
```

ssh -i ~/ssh_other/id_app-01_ed25519 shiki@172.21.32.25



5. Проверка подключения

```bash
ssh -v -i ~/ssh_other/id_app-01_ed25519 shiki@172.21.32.25
```




openssl s_client -showcerts -connect git.esu.gsp.local:443 -servername git.esu.gsp.local < /dev/null 2>/dev/null | openssl x509 -outform PEM > /etc/gitlab-runner/git.esu.gsp.local.crt

echo | openssl s_client -CAfile /etc/gitlab-runner/git.esu.gsp.local.crt -connect git.esu.gsp.local:443 -servername git.esu.gsp.local


gitlab-runner register  \
    --tls-ca-file=/etc/gitlab-runner/git.esu.gsp.local.crt \
    --url https://git.esu.gsp.local  \
    --token glrt-LNHX-X-X-X-X-X-X-X-X-X-X-X-X-X-X-X <-- как то так выглядеть должен