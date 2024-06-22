# Лабораторная работа №1 по компьютерным сетям

1) Топология собрана:
Ее можно увидеть на фото topology.png

2) Клиенты VPC1 и VPC2 находятся во VLAN 10 и 20.

_______
1. **Настроим S0, коммутатор доступа для левого клиента**:
```bash
enable
configure terminal
vlan 10
exit
vlan 20
exit
interface gi 0/2
switchport mode access
switchport access vlan 10
exit
interface range gi 0/0-1
switchport trunk encapsulation dot1q
switchport mode trunk
switchport trunk allowed vlan 10,20
exit
exit
write memory
```

2. **Настроим S1, коммутатор доступа для правого клиента**:
```bash
enable
configure terminal
vlan 10
exit
vlan 20
exit
interface gi 0/2
switchport mode access
switchport access vlan 20
exit
interface range gi 0/0-1
switchport trunk encapsulation dot1q
switchport mode trunk
switchport trunk allowed vlan 10,20
exit
exit
write memory
```

3. **Настроим S2, коммутатор для маршрутизатора**:

```bash
enable
configure terminal
vlan 10
exit
vlan 20
exit
interface range gi 0/0-2
switchport trunk encapsulation dot1q
switchport mode trunk
switchport trunk allowed vlan 10,20
exit
exit
write memory
```

4. **Настроим Клиента 1**:
```bash
ip 10.0.10.2/24 10.0.10.1
```
5. **Настроим Клиента 2**:
```bash
ip 10.0.20.2/24 10.0.20.1
```
6. **Настроим маршрутизатор**:
```bash
enable
configure terminal
interface gi 0/1
no shutdown
```
Здесь не до конца смог понять, как сделать корнем для vlan

______


Работа выполнена в EVE-NG.

Клиенты пингуются успешно, это можно посмотреть на скринах images/ping1.png и images/pin2.png

Сеть отказоустойчива - отключим случайный линк и все также будет работать, пинги доходят.

Конфигурации устройств лежат в configs.

ZIP-файл с лабораторной приложен.