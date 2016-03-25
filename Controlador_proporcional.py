#!/usr/bin/env python
# -*- coding:utf-8 -*- 

import rospy
from nav_msgs.msg import Odometry
from geometry_msgs.msg import Twist
from math import fabs
from sensor_msgs.msg import LaserScan


velocidade_objetivo = Twist();
pub = rospy.Publisher('/cmd_vel', Twist, queue_size=3)

def notificacao(data):
 
    global velocidade_objetivo

#Sair da função se a distancia do sensor ultrapassar seus limites, assim evitando o erro

    if data.ranges[5] < data.range_min:
        return

    elif data.ranges[5] > data.range_max:
        return

#Igual a velocidade para ser proporcional a distância lida pelo sensor

    velocidade = data.ranges[5]

#Quando a leitura do sensor for menor que 0.35 o robo para, pois já estara na parede

    if velocidade < 0.35:
        velocidade = 0


    velocidade_objetivo = Twist()

#a proporção de velocidade/5 foi feita pois se fosse simplesmente a velocidade, o robô vai muito rápido e não consegue parar a tempo

    velocidade_objetivo.linear.x = velocidade/5
    velocidade_objetivo.linear.y = 0
    velocidade_objetivo.linear.z = 0




def controle():

    rospy.init_node('Exemplo_Python')
    rospy.Subscriber("/stable_scan",LaserScan, notificacao)

    while not rospy.is_shutdown():
        pub.publish(velocidade_objetivo)
        rospy.sleep(0.2)

if __name__ == '__main__':
    try:
        controle()
    except rospy.ROSInterruptException:
        pass
