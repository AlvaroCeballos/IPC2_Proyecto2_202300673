class Carro ():
    def __init__(self, idTipoAuto, Marca, Modelo, Descripcion, Precio_unitario, Cantidad, Imagen):
        self.idTipoAuto = idTipoAuto
        self.Marca = Marca
        self.Modelo = Modelo
        self.Descripcion = Descripcion
        self.Precio_unitario = Precio_unitario
        self.Cantidad = Cantidad
        self.Imagen = Imagen


    def __str__(self):
        return f'{self.idTipoAuto} {self.Marca} {self.Modelo} {self.Descripcion} {self.Precio_unitario} {self.Cantidad} {self.Imagen}'