valor = int(input("Que numero quer descobrir o inverso modular multiplicativo? "))
for i in range(1000):
    if ((valor*i)%1000 == 1):
        print(valor, "x", i, "mod 1000 =", (valor*i)%1000)
