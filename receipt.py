from fpdf import FPDF 
import string
import random
from datetime import datetime 
import qrcode
class Product:
    def __init__(self, name, price, quantity):
        self.name = name
        self.price = price
        self.quantity = quantity
def generateReceipt(name,number,direction,pay,products,descuento):

    leters=(''.join(random.SystemRandom().choice(string.ascii_letters) for _ in range(3)))
    numbers=(''.join(random.SystemRandom().choice(string.digits) for _ in range(2)))
    key=f"{leters}{numbers}"
    pdf = FPDF() 
    total=0
    pdf.add_page() 
    now = datetime.now()


    cordenatey=140 
    # create a cell
    pdf.image("img.jpg",x = 0, y=0 , w = 210, h = 297)
    pdf.image("thea.jpg",x = 18, y=20 , w = 49.6, h = 21.15)

    pdf.set_font("Arial", size = 12) 

    pdf.text(x=160, y=20, txt = f"{now.day}/{now.month}/{now.year}",)
    precios=[]
    pdf.set_font("Arial", size = 30) 

    pdf.text(x=85, y=50, txt = "Factura",)
    pdf.set_font("Arial", size = 20) 
    pdf.text(x=93, y=57, txt = key) 
    pdf.text(x=30, y=75, txt = "Nombre:",)
    pdf.text(x=120, y=75, txt = "Numero:",)
    pdf.text(x=30, y=100, txt = "Direcion:",)
    pdf.text(x=120, y=100, txt = "Metodo de pago:",)

    pdf.image("box.jpg",x = 30, y=76 , w = 77, h = 15)
    pdf.image("box.jpg",x = 30, y=101 , w = 77, h = 15)
    pdf.image("box.jpg",x = 120, y=76 , w = 70, h = 15)
    pdf.image("box.jpg",x = 120, y=102 , w = 70, h = 15)

    pdf.set_font("Arial", size = 13) 

    pdf.text(x=33, y=84, txt = name,)
    pdf.text(x=33, y=109, txt = direction,)
    pdf.text(x=125, y=84, txt = number,)
    pdf.text(x=125, y=110, txt = pay.upper(),)

    pdf.set_font("Arial", size = 17) 
    pdf.text(x=33, y=130, txt = "Producto",)
    pdf.text(x=110, y=130, txt = "cantidad",)
    pdf.text(x=150, y=130, txt = "valor",)
    pdf.line(30, 133, 165, 133)

    pdf.set_font("Arial", size = 15) 
    for product in products:
        precios.append(int(product["price"])*int(product['quantity']))
        pdf.text(x=30, y=cordenatey, txt = f"> {product['name']}")
        pdf.text(x=112, y=cordenatey, txt = f"x{product['quantity']}")
        pdf.text(x=150, y=cordenatey, txt = "${:,.0f}".format(int(product["price"])*int(product['quantity'])))
        cordenatey+=7
    for i in precios:
        total+=i
    pdf.line(30, cordenatey+3, 165, cordenatey+3)
    pdf.text(x=112, y=cordenatey+9, txt = f"envio :",)
    pdf.text(x=150, y=cordenatey+9, txt = "$5.000")
    pdf.text(x=112, y=cordenatey+15, txt = f"descuento :",)
    pdf.text(x=150, y=cordenatey+15, txt = f"{descuento}%")
    total=((total+5000)/100)*(100-int(descuento))
    print(total)
    pdf.text(x=112, y=cordenatey+21, txt = f"Total :",)
    pdf.text(x=150, y=cordenatey+21, txt = "${:,.0f}".format(total)
        
        )

    img = qrcode.make("thestyle.co")
    f = open("output.png", "wb")
    img.save(f)
    f.close()

    pdf.image("output.png",x = 43,y=cordenatey+9 , w = 50, h = 50)
    #pdf.output("da.pdf")
    pdf.output(f"{key}-{now.day}#{now.month}#{now.year}.pdf")
    print(f"factura creada exitosamente \n {key}-{now.day}#{now.month}#{now.year}.pdf")
    
   