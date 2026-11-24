#ejercicio 6 · n3 · ¿existe x con 0 <= x <= b tal que g^x ≡ h (mod p)?
#clase: NP · algoritmo: búsqueda exhaustiva con exponenciación modular + verificador

#lectura: valida parámetros (primalidad por división, suficiente para datos didácticos)
def es_primo(p):
    if p < 2:
        return False
    d = 2
    while d * d <= p:
        if p % d == 0:
            return False
        d += 1
    return True

def validar(p, g, h, B):
    if not all(isinstance(v, int) for v in (p, g, h, B)):
        raise ValueError("todos los parámetros deben ser enteros")
    if not es_primo(p):
        raise ValueError(f"p = {p} no es primo")
    if not (0 < g < p and 0 <= h < p) or B < 0:
        raise ValueError("se requiere 0 < g < p, 0 <= h < p y B >= 0")

#búsqueda: recorre x = 0..b manteniendo g^x mod p con una multiplicación por paso
def buscar_exponente(p, g, h, B):
    validar(p, g, h, B)
    valor = 1                           #g^0 mod p
    for x in range(B + 1):
        if valor == h:
            return x                    #certificado
        valor = (valor * g) % p
    return None

#verificador: exponenciación rápida pow(g, x, p), o(log x) multiplicaciones
def verificar_exponente(p, g, h, B, x):
    return isinstance(x, int) and 0 <= x <= B and pow(g, x, p) == h

#versión de exponenciación rápida escrita a mano (cuadrado y multiplicación)
def pow_mod(base, exp, mod):
    resultado = 1
    base %= mod
    while exp > 0:
        if exp & 1:
            resultado = (resultado * base) % mod
        base = (base * base) % mod
        exp >>= 1
    return resultado

#presentación y pruebas
if __name__ == "__main__":
    p, g, h, B = 23, 5, 8, 10
    x = buscar_exponente(p, g, h, B)
    print(f"p={p}, g={g}, h={h}, B={B} -> x = {x}")
    print("verificación:", verificar_exponente(p, g, h, B, x), "| pow_mod:", pow_mod(g, x, p))
    #certificado falso
    print("certificado x = 3:", verificar_exponente(p, g, h, B, 3))
    #caso no: h = 7 aparece recién en x = 19, fuera del límite b = 10
    print("h = 7, B = 10:", buscar_exponente(p, g, 7, 10), "| con B = 22:", buscar_exponente(p, g, 7, 22))
    #caso límite: h = 1 se obtiene con x = 0
    print("h = 1:", buscar_exponente(p, g, 1, B))
    #caso inválido: p no primo
    try:
        buscar_exponente(21, 5, 8, 10)
    except ValueError as e:
        print("error controlado:", e)

    assert x == 6 and verificar_exponente(p, g, h, B, x) and pow_mod(g, x, p) == h
    assert buscar_exponente(p, g, 7, 10) is None and buscar_exponente(p, g, 7, 22) == 19
    print("todas las pruebas pasaron")
