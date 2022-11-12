# TP2-Openflow

### Ejecutando

Corriendo la topologia:
``` sh
sudo mn --custom ./topology.py --topo chain,number_of_switches=2
```

### Dependencias

Cliente de mininet
```sh
sudo apt install mininet
```

Biblioteca de Mininet para Python
``` sh
sudo pip install mininet
```


### Pruebas

Para correr las pruebas unitarias:
``` sh
python3 -m unittest topology_tests.py
```
