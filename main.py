import os
import cv2
import graphviz
from os.path import isfile, join

index = 0
dfa = graphviz.Digraph(directory="poze", format="png")

f = open("date.in", "r")

automatDFA = {}


def creeazaAutomat(nod):  # imi creez automat cu toate lambda tranzitiile
    global stareInitiala, stariFinale, automat
    for listeMici in automat[nod]:
        multimeStari.add(nod)
        if listeMici[1] == '#':
            multimeStari.add(listeMici[0])
            creeazaAutomat(listeMici[0])


def convertireSir(tranzitiePrimita):  # In functia asta iau o lista si o transform intr-un sir de caractere
    lista = sorted(tranzitiePrimita)  # Exemplu [0, 1, 2, 3] devine "0123"
    tranzitieFinala = ""
    for x in lista:
        tranzitieFinala = tranzitieFinala + x
    return tranzitieFinala


stareFost = []  # fac o lista pentru a memora starile prin care am trecut deja
automatFinal = {}
stariFinaleDFA = set()


def dictLambda(lambdaInchidere):  # dictionarul are ca parametru o stare pe care am creat-o
    for tranzitie in tranzitii:  # fac for pe lista in care am toate tranzitiile din automat mai putin lambda
        multimeTranzitie = set()
        for element in lambdaInchidere:  # iau fiecare element din starea mea : ex q023456, iau 0, 2, 3 si asa mai departe
            if element in automat:  # verific daca elementul meu se afla in automat
                for tranzElem in automat[element]:  # parcurg tranzitiile elementului din automatul mare
                    if tranzElem[
                        1] == tranzitie:  # daca tranzitia elementului din automatul mare este egala cu tranzitia din for, adaug starea in care pot ajunge
                        multimeTranzitie.add(tranzElem[0])
        multimeLambdaFinal = set()
        for inchidere in multimeTranzitie:
            if inchidere in automatDFA:
                multimeLambdaFinal = multimeLambdaFinal.union(automatDFA[
                                                                  inchidere])  # aici fac o reuniune dintre lambda inchidere de care am nevoie (pe care le am in multimeTranzitie)
        stareNoua = multimeLambdaFinal  # starea mea noua va fi multimeLambdaFinal adica reuniunea de mai sus
        lambdaSir = sorted(lambdaInchidere)
        for x in lambdaSir:
            if x in stariFinale:
                lambdaSir = convertireSir(
                    lambdaSir)  # verific daca am vreo stare finala in lambdaSir-ul meu si daca da o adaug in starile finale ale DFA-ului
                stariFinaleDFA.add(lambdaSir)
        lambdaSir = convertireSir(lambdaSir)
        if lambdaSir in automatFinal:  # verific daca starea mea se afla in automatul final
            stareNoua = convertireSir(stareNoua)
            automatFinal[lambdaSir].append((stareNoua, tranzitie))
        else:
            stareNoua = convertireSir(stareNoua)
            automatFinal[lambdaSir] = [(stareNoua, tranzitie)]
        if stareNoua not in stareFost:  # daca nu am mai trecut prin starea pe care o am acum, o introduc in lista starilor prin care am mai trecut
            stareFost.append(stareNoua)  # pentru a nu mai trece prin ea inca odata atunci cand apelez functia din nou
            dictLambda(stareNoua)  # apelez functia pentru starea mea noua daca nu am mai trecut prin ea


fisier = f.readlines()
nrNod = int(fisier[0].split()[0])  # Memorez numarul de stari
nrTranz = int(fisier[0].split()[1])  # Memorez numarul de tranzitii

i = 1
automat = {}
while i <= nrTranz:
    if fisier[i].split()[0] in automat:
        automat[fisier[i].split()[0]].append([fisier[i].split()[1], fisier[i].split()[2]])
    else:
        automat[fisier[i].split()[0]] = [[fisier[i].split()[1], fisier[i].split()[2]]]
    i += 1

# Construiesc automatul ca un dictionar avand ca chei starile si la fiecare stare am facut o lista
# care sa contina mai multe liste mici unde memorez starile in care pot ajunge si prin ce tranzitii
# {'0': [['0', 'a'], ['1', 'a'], ['2', 'b'], ['2', '#'], ['3', '#']], '1': [['2', '#']], '2': [['3', 'a'], ['4', '#']],
# '3': [['3', 'b'], ['5', '#'], ['6', 'a'], ['6', 'b']], '4': [['5', 'b'], ['6', 'a'], ['6', '#']],
# '5': [['6', 'a'], ['2', 'b'], ['2', '#'], ['6', '#']], '6': [['6', 'b']]}


stareInitiala = fisier[i].split()[0]  # Memorez starea initiala
i += 1

nrStariFinale = int(fisier[i].split()[0])  # Memorez numarul de stari finale
j = 1
stariFinale = []
while j <= nrStariFinale:
    stariFinale.append(fisier[i].split()[j])  # Fac o lista unde memorez starile finale
    j += 1

tranzitii = []
for i in range(len(automat)):  # Verific ce tranzitii am un automatul lambda - NFA
    for tranzitie in automat[str(i)]:
        if tranzitie[1] not in tranzitii and tranzitie[1] != '#':
            tranzitii.append(tranzitie[1])

stareInitiala = str(stareInitiala)  # Creez automat pentru lambda inchideri
stareCurenta = stareInitiala
for stareCurenta in automat:
    multimeStari = set()
    creeazaAutomat(stareCurenta)
    automatDFA[stareCurenta] = multimeStari

# {'0': {'2', '3', '6', '0', '4', '5'}, '1': {'1', '2', '4', '6'}, '2': {'2', '4', '6'}, '3': {'2', '6', '3', '4', '5'}, '4': {'4', '6'}, '5': {'5', '2', '4', '6'}, '6': {'6'}}

dictLambda(automatDFA[stareInitiala])  # apelez functia care o sa-mi construiasca automatul DFA final
print("Stare intiala:", convertireSir(automatDFA[stareInitiala]))
if len(stariFinaleDFA) < 2:
    print("Stare finala", stariFinaleDFA)
else:
    print("Stari finale:", *stariFinaleDFA)
print("Automat DFA:", automatFinal)

dfa.attr(rankdir='LR', size='8,5')

dfa.attr('node', shape='none')
dfa.node('')

if convertireSir(automatDFA[stareInitiala]) not in stariFinaleDFA:
    dfa.attr('node', shape='circle')
    dfa.edge('', convertireSir(automatDFA[stareInitiala]))
    dfa.render(filename=f'{index}')
    index += 1
else:
    dfa.attr('node', shape='doublecircle')
    dfa.edge('', convertireSir(automatDFA[stareInitiala]))
    dfa.render(filename=f'{index}')
    index += 1
stareVizitata = []

imagini = [f for f in os.listdir('./poze') if f.endswith('.png')]
imagini.sort(key=lambda x: int(x.split('.')[0]))
imagine = cv2.imread('./poze/' + str(len(imagini) - 1) + '.png')
dimMax = imagine.shape[1], imagine.shape[0]


def creareImagine(starePrimita):
    global index
    stareVizitata.append(starePrimita)
    if starePrimita != convertireSir(automatDFA[stareInitiala]):
        if starePrimita in stariFinaleDFA:
            dfa.attr('node', shape='doublecircle')
            dfa.node(starePrimita)
        else:
            dfa.attr('node', shape='circle')
            dfa.node(starePrimita)
    for stareC in automatFinal[starePrimita]:
        dfa.edge(starePrimita, stareC[0], label=stareC[1])
        dfa.render(filename=f'{index}')
        index += 1
        if stareC[0] not in stareVizitata:
            creareImagine(stareC[0])


creareImagine(convertireSir(automatDFA[stareInitiala]))


def automatVizual(pathIn, pathOut, fps, timp):
    listaImagini = []
    resurse = [f for f in os.listdir(pathIn) if isfile(join(pathIn, f)) and f.endswith('.png')]
    for i in range(len(resurse)):
        numeFisier = pathIn + resurse[i]
        img = cv2.imread(numeFisier)
        img = cv2.resize(img, dimMax)

        for k in range(timp):
            listaImagini.append(img)
    out = cv2.VideoWriter(pathOut, cv2.VideoWriter_fourcc(*'mp4v'), fps, dimMax)
    for i in range(len(listaImagini)):
        out.write(listaImagini[i])
    out.release()


folder = './poze'
pathIn = folder + '/'
pathOut = pathIn + 'automatVizual.avi'
fps = 1
timp = 1
automatVizual(pathIn, pathOut, fps, timp)
