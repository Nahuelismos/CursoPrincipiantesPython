import turtle

window = turtle.Screen()
flecha = turtle.Turtle()

def triangulo():
  for i in range(3):
    flecha.forward(100)
    flecha.left(120)

def cuadrado():
  flecha.color("red")
  for i in range(4):
    flecha.forward(100)
    flecha.left(90)

def pentagono():
  flecha.color("blue")
  for i in range(5):
    flecha.forward(100)
    flecha.left(72)

triangulo()
cuadrado()
pentagono()