import json
from datetime import datetime  
 
ruta_json = "clientes.json"
 
# Listas en memoria
ordenes = []
 
menu = [
    {
        "nombre": "Pizza",
        "descripcion": "Pizza artesanal con ingredientes frescos",
        "tamaños y precios": {
            "Personal": 20000,
            "Mediana": 35000,
            "Familiar": 50000
        }
    },
    {
        "nombre": "Hamburguesa",
        "descripcion": "Callejera",
        "tamaños y precios": {
            "Sencilla": 18000,
            "Doble": 25000
        }
    },
    {
        "nombre": "Alitas",
        "descripcion": "BBQ",
        "tamaños y precios": {
            "Pequeña": 12000,
            "Familiar": 20000
        }
    }
]
 
formas_pago = ["Tarjeta Débito", "Tarjeta Crédito", "Efectivo", "Bono"]
 
 
def pedir_numeros(mensaje, longitud_min=None, longitud_max=None):
    while True:
        valor = input(mensaje).strip()
        if valor.isdigit():
            if (longitud_min and len(valor) < longitud_min) or (longitud_max and len(valor) > longitud_max):
                print(f"Debe tener entre {longitud_min} y {longitud_max} dígitos.")
            else:
                return valor
        else:
            print("Solo se permiten números.")
 
 
def pedir_letras(mensaje):
    while True:
        valor = input(mensaje).strip()
        if valor.replace(" ", "").isalpha():  
            return valor
        else:
            print("Solo se permiten letras.")
 
 
def pedir_opcion(mensaje, opciones):
    while True:
        try:
            valor = int(input(mensaje))
            if 1 <= valor <= opciones:
                return valor
            else:
                print(f"Debe ser un número entre 1 y {opciones}.")
        except ValueError:
            print("Entrada inválida, ingrese un número.")
 
 
def cargar_clientes():
    try:
        with open(ruta_json, "r", encoding="utf-8") as f:
            return json.load(f)
    except FileNotFoundError:
        return []
 
 
def guardar_clientes(clientes):
    with open(ruta_json, "w", encoding="utf-8") as f:
        json.dump(clientes, f, indent=4, ensure_ascii=False)
 
 
def registrar_cliente():
    clientes = cargar_clientes()
 
    cliente = {
        "cedula": pedir_numeros("Ingrese su cédula: ", longitud_min=3, longitud_max=5),
        "nombre": pedir_letras("Ingrese su nombre: "),
        "email": input("Ingrese su correo: "),
        "telefono": pedir_numeros("Ingrese su teléfono: ", longitud_min=3, longitud_max=5)
    }
 
    if any(c["cedula"] == cliente["cedula"] for c in clientes):
        print("Cliente ya registrado.\n")
        return
 
    clientes.append(cliente)
    guardar_clientes(clientes)
    print("\nCliente registrado con éxito.\n")
 
 
def consultar_cliente():
    clientes = cargar_clientes()
    cedula_buscar = pedir_numeros("Ingrese la cédula del cliente: ")
 
    cliente = next((c for c in clientes if c["cedula"] == cedula_buscar), None)
 
    if cliente:
        print("\n--- DATOS CLIENTE ---")
        for k, v in cliente.items():
            print(f"{k}: {v}")
 
        historial = [o for o in ordenes if o.get("cliente") == cliente["nombre"]]
        if historial:
            print("\n--- HISTORIAL DE ÓRDENES ---")
            for o in historial:
                print(f"Orden #{o['numero']} | {o['plato']} ({o['tamaño']}) x{o['cantidad']} = ${o['precio_total']} | Pago: {o['pago']} | Fecha: {o['fecha']}")
        else:
            print("\n(No tiene órdenes registradas)")
        print()
    else:
        print("Cliente no encontrado.\n")
 
 
def mostrar_menu():
    print("\n=== MENÚ ===")
    for i, plato in enumerate(menu, start=1):
        # Ahora mostramos el nombre y descripción del plato
        print(f"{i}. {plato['nombre']} - {plato['descripcion']}")
        for j, (tam, precio) in enumerate(plato["tamaños y precios"].items(), start=1):
            print(f"   {j}) {tam}: ${precio}")
    print()
   
def hacer_orden():
    clientes = cargar_clientes()
 
    if not clientes:
        print("No hay clientes registrados.\n")
        return
 
    cedula_cliente = pedir_numeros("Ingrese cédula del cliente: ")
    cliente = next((c for c in clientes if c["cedula"] == cedula_cliente), None)
 
    if not cliente:
        print("Cliente no encontrado.\n")
        return
 
    mostrar_menu()
    plato_idx = pedir_opcion("Seleccione número del plato: ", len(menu)) - 1
    plato = menu[plato_idx]
 
    tamaños = list(plato["tamaños y precios"].keys())
    precios = list(plato["tamaños y precios"].values())
 
    tam_idx = pedir_opcion("Seleccione tamaño del plato: ", len(tamaños)) - 1
    cantidad = int(pedir_numeros("Ingrese cantidad: "))
 
    nombre_plato = plato["nombre"]
    tamaño_elegido = tamaños[tam_idx]
    precio_unitario = precios[tam_idx]
    precio_total = precio_unitario * cantidad
 
    print("\nFormas de pago:")
    for i, fp in enumerate(formas_pago, start=1):
        print(f"{i}. {fp}")
    opcion_pago = pedir_opcion("Seleccione forma de pago: ", len(formas_pago)) - 1
    pago = formas_pago[opcion_pago]
 
    cuotas = 1
    valor_cuota = precio_total
 
    if pago == "Tarjeta Crédito":
        cuotas = int(pedir_numeros("¿A cuántas cuotas desea pagar? (1-12): "))
        if cuotas < 1:
            cuotas = 1
        elif cuotas > 12:
            cuotas = 12
        valor_cuota = round(precio_total / cuotas)
 
    # 👇 aquí añadimos la fecha actual
    fecha = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
 
    orden = {
        "numero": len(ordenes) + 1,
        "cliente": cliente["nombre"],
        "plato": nombre_plato,
        "tamaño": tamaño_elegido,
        "cantidad": cantidad,
        "precio_total": precio_total,
        "pago": pago,
        "cuotas": cuotas,
        "valor_cuota": valor_cuota,
        "fecha": fecha   # 👈 agregamos la fecha
    }
    ordenes.append(orden)
    print("\nOrden registrada.")
    imprimir_orden(orden)
 
 
def imprimir_orden(orden):
    print("\n  ORDEN  ")
    print(f"Número: {orden['numero']}")
    print(f"Cliente: {orden['cliente']}")
    print(f"Plato: {orden['plato']} ({orden['tamaño']})")
    print(f"Cantidad: {orden['cantidad']}")
    print(f"Precio total: ${orden['precio_total']}")
    print(f"Pago: {orden['pago']}")
    print(f"Fecha: {orden['fecha']}")  
   
    if orden["pago"] == "Tarjeta Crédito":
        print(f"Pago en {orden['cuotas']} cuotas de ${orden['valor_cuota']} cada una")
   
    print()
 
 
def consultar_orden():
    if not ordenes:
        print("No hay órdenes registradas.\n")
        return
    num = pedir_numeros("Ingrese número de orden: ")
    num = int(num)
    for o in ordenes:
        if o["numero"] == num:
            imprimir_orden(o)
            return
    print("Orden no encontrada.\n")
 
 
def menu_inicio():
    while True:
        print("\n   SISTEMA RESTAURANTE   \n")
        print("1. Registrar Cliente")
        print("2. Mostrar Menú")
        print("3. Hacer Orden")
        print("4. Consultar Cliente")
        print("5. Consultar Orden")
        print("6. Salir\n")
        opcion = input("Seleccione una opción: \n")
 
        if opcion == "1":
            registrar_cliente()
        elif opcion == "2":
            mostrar_menu()
        elif opcion == "3":
            hacer_orden()
        elif opcion == "4":
            consultar_cliente()
        elif opcion == "5":
            consultar_orden()
        elif opcion == "6":
            print("Chau, Que vuelvas muy pronto.")
            break
        else:
            print("Opción inválida.\n")
 
 
menu_inicio()


# tema de validaciones

# Expresiones regulares regex
