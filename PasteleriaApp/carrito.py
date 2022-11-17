class Carrito:
    def __init__(self, request):
        self.request = request
        self.session = request.session
        carrito = self.session.get("carrito")
        id = self.session.get('id')
        total = self.session.get('total')
        if not carrito:
            self.session["carrito"] = {}
            self.carrito = self.session["carrito"]
            self.session['total'] = 0
            self.session['id'] = 1
            self.id = self.session['id']
        else:
            # print(id)
            self.carrito = carrito
            self.id = id
            self.total = total

    def agregar(self, producto):
        # print(self.id)
        if self.id not in self.carrito.keys():
            self.carrito[str(self.id)] = {
                "tamaño": producto['tamaño'],
                "cobertura": producto['cobertura'],
                "relleno": producto['relleno'],
                "sabor": producto['sabor'],
                "aclaracion": producto['aclaracion'],
                'precio_pastel': producto['precio_pastel']
            }
            # print(self.carrito)
            # print(self.id)
            # print(self.session['total'])
            self.session['total'] = self.session['total'] + int(producto['precio_pastel'])
            self.session['id'] = self.id + 1
        # else:
        #     self.carrito[id]["cantidad"] += 1
        #     self.carrito[id]["acumulado"] += producto.precio
        self.guardar_carrito()

    def guardar_carrito(self):
        self.session["carrito"] = self.carrito
        self.session.modified = True

    def eliminar(self, producto_id):
        id = producto_id
        # print(type(id))
        if str(id) in self.carrito:
            # print('entro')
            self.session['total'] = self.session['total'] - self.carrito[str(id)]['precio_pastel']
            del self.carrito[str(id)]
        # print(len(self.carrito))
        # print(id)
        # print(type(id))
        for key in range(id, len(self.carrito)+1):
            # print('holas')
            # print(self.carrito)
            # print(self.carrito[str(key+1)])
            self.carrito[str(key)] = self.carrito.pop(str(key+1))
            # del self.carrito[str(key+1)]
        # print(self.carrito)
        # print(self.id)
        self.session['id'] = self.id - 1
        self.guardar_carrito()

    # def restar(self, producto):
    #     id = str(producto.id)
    #     if id in self.carrito.keys():
    #         self.carrito[id]["cantidad"] -= 1
    #         self.carrito[id]["acumulado"] -= producto.precio
    #         if self.carrito[id]["cantidad"] <= 0:
    #             self.eliminar(producto)
    #         self.guardar_carrito()

    def limpiar(self):
        self.session["carrito"] = {}
        self.session['id'] = 1
        self.session['total'] = 0
        self.session.modified = True
