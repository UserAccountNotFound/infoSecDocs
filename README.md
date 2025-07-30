# infoSec documents
A database of regulatory documents in the field of Information security and engineering and technical security equipment, with the ability to export templated documents to PDF


## preInstall

```bash
sudo apt install sudo git curl g++ gcc libnss3 libasound2 libnspr4
```

Устанавливаем корневые  довенные сертивикаты сертификаты и CRL к ним (на всякий случай)

```bash
sudo mkdir /usr/local/share/ca-certificates/gsp.local && \
sudo wget -P /usr/local/share/ca-certificates/gsp.local \
http://cdp.gsp.local/pki/gsp-rca.crt \
http://cdp.gsp.local/pki/gsp-rca.crl \
http://cdp.gsp.local/pki/gsp-sca\(1\).crt \
http://cdp.gsp.local/pki/gsp-sca\(1\).crl \
http://cdp.gsp.local/pki/gsp-sca\(1\)\+.crl && \
openssl x509 -inform der -in /usr/local/share/ca-certificates/gsp.local/gsp-rca.crt -out /usr/local/share/ca-certificates/gsp.local/gsp-rca.pem && \
openssl x509 -inform der -in /usr/local/share/ca-certificates/gsp.local/gsp-sca\(1\).crt -out /usr/local/share/ca-certificates/gsp.local/gsp-sca_1.pem && \
sudo update-ca-certificates && \
git config --global http.sslCAinfo /usr/local/share/ca-certificates/gsp.local/gsp-rca.pem && \
rm -fR /usr/local/share/ca-certificates/gsp.local
```

Настраиваем в git доверие к корневому доменному сертификату 

```bash
git config --global http.sslCAinfo /usr/local/share/ca-certificates/gsp.local/gsp-rca.pem
```

## Getting started

Конируем репозоторий
```bash
git clone https://git.esu.gsp.local/cyberSecurity/docsite.git
```

Создаем виртуальное окружение в папке нашего проекта:
```bash
python3 -m venv .venv_mkdocs
```
Мы назвали его .venv_mkdocs (скрытая папка), чтобы не путать с venv от основного приложения.

Активируем его (для интерактивной работы):
```bash
source ./.venv_mkdocs/bin/activate
```

После этого в начале строки терминала появится (venv_mkdocs).

Устанавливаем пакеты уже в "чистое" окружение:

```bash
pip install poetry && poetry install && playwright install-deps && playwright install
```

для разработки (dev-сервер)
```bash
mkdocs serve -a 0.0.0.0:8000
```

для сборки сайта (prod)
```bash
mkdocs build --clean
```



Сборка образа Docker для CI/CD

docker build -t registry.esu.gsp.local/cybersecurity/docsite/mkdocs_bulder:1.0.1 .
docker push registry.esu.gsp.local/cybersecurity/docsite/mkdocs_bulder:1.0.1

openssl s_client -showcerts -connect registry.esu.gsp.local:443 -servername registry.esu.gsp.local < /dev/null 2>/dev/null | openssl x509 -outform PEM > /etc/docker/certs.d/registry.esu.gsp.local

==========================================
полезное:
верстка PDF
https://github.com/CourtBouillon/weasyprint-samples/blob/main/book/book-classical.css
============================================================================

#### Лентяйки:

```bash
cd existing_repo
git remote add origin https://git.esu.gsp.local/cyberSecurity/docsite.git
git branch -M dev
git push -uf origin dev
```

Добавление самоподписаного сертификата, если на него ругается IDE

```bash
openssl s_client -connect git.esu.gsp.local:443 -showcerts </dev/null 2>/dev/null | sed -n '/BEGIN CERTIFICATE/,/END CERTIFICATE/p' > git-esu-gsp-local.crt

sudo cp git-esu-gsp-local.crt /usr/local/share/ca-certificates/
sudo update-ca-certificates
```


git remote add gitlab http://git.netgroup.su/msp/docsite.git

отправка изменений в оба-два
git push origin main  # в GitHub
git push gitlab main  # в Gitlab

получение изменений
git pull origin main  # из GitHub
# или
git pull gitlab main  # из GitLab