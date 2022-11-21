# TP2-Openflow

### Dependencias

* Python 3.8+

* Cliente de mininet
```sh
sudo apt install mininet
```

* Biblioteca de Mininet para Python
``` sh
sudo pip install mininet
```

* OpenvSwitch
```sh
sudo apt install openvswitch-switch
systemctl start openvswitch
```

* Herramientas de prueba
```
sudo apt install xterm

```

### Cómo ejecutar el proyecto:
1. Asegurarse de haber instalado las dependencias necesarias.
2. Clonar el proyecto mediante `git clone` y hacer `cd` dentro del mismo.
3. Ejecutar el controlador en un terminal emulator mediante:

``` sh
python3 pox.py log.level --DEBUG openflow.of_01 forwarding.l2_learning controller
```
  No cerrar esta ventana, y proceder con los siguientes pasos en otra terminal

4. Corriendo la topologia:
``` sh
sudo mn --custom ./topology.py --topo chain,number_of_switches=2 --mac --arp -x --switch ovsk --controller remote
```
  Esto configurará la red creada por mininet con la topología de cadena del enunciado, insertando en el medio la cantidad de switches especificada en la línea del comando. La misma utilizará como controlador la topología `chain` definida en `topology.py`. Adicionalmente, veremos que se abre una terminal `xterm` para cada uno de nuestros hosts virtuales, permitiendonos realizar pruebas

### Pruebas
* Pruebas con `iperf` (ver informe .pdf para más detalle):
Ahora testearemos que nuestro controlador está efectivamente imponiendo las reglas de firewall declaradas en el archivo `rules.json`. Para esto, podemos usar el comando `iperf`, levantando clientes y servidores como sea necesario.
  1. Probando regla 1 (Bloquear toda comunicación por puerto 80):
```sh
     iperf -s -p 80 #en la terminal del host4, para que actue como servidor escuchando en el puerto 80.
     iperf -c 10.0.0.4 -p 80 #en la terminal del host1, para que actue como cliente e intente hacer la request.
```
     Veremos que la regla se aplica exitosamente. Podemos probar además con UDP agregando el flag `-u` para demostrar que la regla aplica para ambos protocolos de transporte.

  2. Probando regla 2 (Bloquear paquetes UDP provenientes del host1 con puerto destino 5001):
```sh
    iperf -u -s -p 5001 #en la terminal del host3, para que actue como servidor UDP en el puerto 5001.
    iperf -u -c 10.0.0.3 -p 5001 #en la terminal del host1, para que actue como cliente e intente hacer la request.
```
    Nuevamente podemos observar que al intentar enviar paquetes que cumplen con losclientes filtros de la regla, estos nunca llegan a destino y somos advertidos del timeout ocurrido.

  3. Probando regla 3 (Bloquear completamente la comunicación entre dos host en específico, en este caso host2 y host3):
 ```sh
     ìperf -s -p 8080 en la terminal del host2, para que actúe como servidor en el puerto 8080.
     iperf -c 10.0.0.2 -p 8080 en la terminal del host3, para que actue como cliente e intente hacer la request.
 ```
    Al utilizar iperf para configurar la situación descripta, vemos que nunca se logra establecer la conexión TCP entre el host2 y el host3, verificando de esta forma que nuestra regla de firewall está en funcionamiento.


* Pruebas unitarias:
``` sh
python3 -m unittest topology_tests.py
```
