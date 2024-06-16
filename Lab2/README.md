# How to use:

1) Собираем контейнер:
```bash
docker build -t mtu .
```
2) Запускаем с флагами:

examples:
```bash
docker run mtu -s google.com
```

```bash
docker run mtu -p 2 -s vk.com
```

```bash
docker run mtu -p 5 -U 1800 yandex.ru
```