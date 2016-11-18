import re

"""
cambiarFecha(texto)
Recibe el texto, el cual se recorre dentro de la funcion para encontrar el patron
creado a partir de expresiones regulares, y asi cambiar dicha fecha encontrada.

Retorna el texto con las fechas modificadas al formato dd/mm/aaaa
"""
def cambiarFecha(texto):
	patron = re.compile(r"^\d{2}[^\w|^\d|^\s|^/]\d{2}[^\w|^\d|^\s|^/]\d{4}[\s|\.|}]|[\s|{|(]\d{2}[^\w|^\d|^\s|^/]\d{2}[^\w|^\d|^\s|^/]\d{4}[\s|\.|}]")
	marca=0
	for linea in texto:
		while re.search(patron,linea)!=None:
			matcher = re.search(patron,linea)
			grupo = matcher.group()
			if len(grupo)==12:
				linea = re.sub(patron, grupo[0:3]+'/'+grupo[4:6]+'/'+grupo[7:12], linea, 1)
				texto[marca]=linea
			else:
				linea = re.sub(patron, grupo[0:2]+'/'+grupo[3:5]+'/'+grupo[6:11], linea, 1)
				texto[marca]=linea
		marca+=1
	return texto

"""
separaMiles(texto)
Recibe el texto, el cual se recorre en la funcion para encontrar la expresion regular que 
representa los numeros que requieren la separacion de miles
Se utiliza modulos para analizar donde tiene que ir el separa miles.

Retorna el texto con los numeros separados en miles(los permitidos).
"""
def separarMiles(texto):
	patron = re.compile(r"^[0-9]{4,}(?=([\)\}\.\,][\W]|\s))|(?<=[\s\{\(])[0-9]{4,}(?=([\)\}\.\,][\W]|\s))")
	marca=0
	for linea in texto:
		while re.search(patron,linea)!=None:
			i=1
			matcher = re.search(patron,linea)
			grupo= matcher.group()
			while i<=len(grupo):
				if i==1:
					cambio = str(grupo[-i])
				elif i%3==1 and i!=1:
					cambio = str(grupo[-i])+"."+cambio
				else:
					cambio = str(grupo[-i])+cambio
				i+=1
			linea = re.sub(patron, cambio, linea, 1)
			texto[marca]=linea
		marca+=1
	return texto

"""
negrita(linea,fn)
Recibe la linea que se recorre, y la expresion regular de la funcion fn
Aplica la etiqueta <strong> a la palabra o frase que se pide ennegrecer

Retorna la linea con la palabra o frase en negrita
"""
def negrita(linea,fn):
	if re.search(fn,linea)!=None:
		negrita=re.search(fn,linea)
		ctext=negrita.group()[4:-1]
		textcur="<strong>"+ctext+"</strong>"
		linea=re.sub(fn,textcur,linea,1)
	return linea
"""
cursiva(linea,fc)
Recibe la linea que se recorre, y la expresion regular de la funcion fc
Aplica la etiqueta <em> para colocar en cursiva la palabra o frase

Retorna la linea con la palabra o frase en cursiva
"""
def cursiva(linea,fc):
	if re.search(fc,linea)!=None:
		cursiva=re.search(fc,linea)
		ctext=cursiva.group()[4:-1]
		textcur="<em>"+ctext+"</em>"
		linea=re.sub(fc,textcur,linea,1)
	return linea

"""
parentesis(data)
Recibe el texto, el cual se recorre para analizar el uso correctos de los parentes "{}"
para esto se utiliza una pila, la cual al momento de encontrar un corchete abierto se agrega
a la pila , si encuentra un corchete cerrado se saca, asi comprobando que existe la misma
cantidad de corchetes de abertura que de cierre. Tambien se verifica que exista la misma cantidad de "backslash"
con respecto a los corchetes, comandos y funciones que se encuentran en la linea.

Retorna False en caso de que no se respete el uso de parentesis, de "backslash", de comandos y funciones (error)
"""
def parentesis(data):
	stack=[]
	count2 = 0
	i = 0
	comando = re.compile(r"\\(separamiles|ofecha|fc|fn|nproy|titulo|inicio|fin|item)")
	for p in data:
		if p == '{':
			stack.append(p)
			count2 += 1
		elif p == '}':
			if len(stack) == 0:
				return False
			stack.pop(-1)
		elif p == '\\':
			i+=1
	if i != count2:
		return False
	totales= comando.findall(data)
	if len(totales)!=i:
		return False
	return len(stack) == 0

"""
inicioFin(texto,inicio,fin,item)
Recibe el texto y las expresiones regualres de inicio, fin y item.
En esta funcion se verifica gran parte de la sintaxis de inicio y fin.
- Que exista un inicio y un fin , solo items entre ellos,
- Que corresponda a lista_enumerada o lista_punteada
- Sintaxis en general

Retorna False en caso de no respetar la sintaxis (error)
"""
def inicioFin(texto,inicio, fin,item):
	pila=[]
	i=0
	marca=0
	while i<len(texto):
		buscar=re.search(inicio,texto[i])
		if buscar:
			if len(pila)==1:
				return False
			marca=i+1
			if buscar.group()[8:-1] == "lista_enumerada":
				pila.append("1")
			elif buscar.group()[8:-1] =="lista_punteada":
				pila.append("2")

		res=re.search(fin,texto[i])
		if res:
			if len(pila)==0:
				return False
			if i==marca:
				print "Error, no tiene items entre \\inicio y \\fin"
				return False
			while i > marca:
				if re.search(item,texto[marca])==None:
					return False
				marca+=1
			if res.group()[5:-1] == "lista_enumerada":
				if pila[0]=="1":
					pila.pop(-1)
				else:
					return False				
			if res.group()[5:-1] == "lista_punteada":
				if pila[0]=="2":
					pila.pop(-1)
				else:
					return False
		i+=1

	return len(pila)== 0

"""
textoAfuera(value)
funcion que crea un contador para verificar que no haya texto afuera de los comandos
Especialmente se utiliza para el comando Item.
Retorna False en caso de haber texto afuera (error)
True si no hay texto afuera
"""
def textoAfuera(value):
	contar=0
	abierto=0
	cerrado=0
	while contar < len(value):
		if value[contar] == '{':
			abierto+=1
		elif value[contar] == '}':
			cerrado+=1
		contar+=1
		if cerrado == abierto and len(value)!=contar and cerrado!=0:
			return False
	return True

"""
Expresiones Regulares de los comandosy algunas necesarias 
para la verificacion de sintaxis
"""
titulo= re.compile(r"\\titulo{.*}")
inicio= re.compile(r"\\inicio{(lista_punteada|lista_enumerada)}")
fin= re.compile(r"\\fin{(lista_punteada|lista_enumerada)}")
InicioFinPrueba = re.compile(r"\\(inicio|fin){?[^}]+}")
IniFinAbierto = re.compile(r"\\(inicio|fin){.*")
item= re.compile(r"\\item{.*}")
fn=re.compile(r"\\fn{[^}|^{]+}") 
fc=re.compile(r"\\fc{[^}|^{]+}") 
nproy=re.compile(r"\\nproy{[^}|^{|^\\]+}")
nproyAbierto=re.compile(r"\\nproy{.*}")
separamiles=re.compile(r"\\separamiles{}")
separaAbierto=re.compile(r"\\separamiles{.*")
ofecha=re.compile(r"\\ofecha{}")
ofechaAbierto=re.compile(r"\\ofecha{.*")

""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""""
#Abrimos el archivo, y traspasamos las lineas a una lista para poderlas manejar
arch= open("suertex.txt")
lista=[]
for linea in arch:
	lista.append(linea)

i=0
contador=0
marca=0
if inicioFin(lista,inicio,fin,item) == False: #Verificamos sintaxis inicio y fin
	print " Error de sintaxis (inicio-fin)" 
	exit()

while i<len(lista):
	if parentesis(lista[i])== False: #Verificamos los parentesis
		print "Error en sintaxis"
		exit()

	#Se verifica la existencia de las funciones y que esten en los lugares permitidos
	#Separamiles y ofecha
	if re.search(separamiles, lista[i]) or re.search(ofecha, lista[i]):
		contador+=1
		if i!= 0 and i!=1:
			print "Error, funciones mal."
			exit()

		# Verificamos texto afuera de la funcion separamiles
		elif re.search(separamiles,lista[i]):
			separar=re.search(separamiles,lista[i])
			verificar_sep=re.search(separaAbierto,lista[i])
			sep= verificar_sep.group()
			sep = sep.strip()
			if sep[-1]!= "}" or lista[i][0]!="\\" or len(separar.group())!=len(sep):
				print "Error , texto afuera de separamiles"
				exit()
			separarMiles(lista) #Se llama funcion para separar miles

		# Verificamos texto afuera de la funcion ofecha
		elif re.search(ofecha,lista[i]):
			ofech=re.search(ofecha,lista[i])
			verificar_fecha=re.search(ofechaAbierto,lista[i])
			fech= verificar_fecha.group()
			fech= fech.strip()
			if fech[-1]!= "}" or lista[i][0]!="\\" or len(ofech.group())!= len(fech):
				print "Error , texto afuera de ofecha"
				exit()
			cambiarFecha(lista) #Se llama funcion para ajustar fecha al formato
	# Nproy
	#Se verifica la sintaxis del comando nproy
	if re.search(nproy,lista[i]):
		proy= re.search(nproy,lista[i])
		verificar_nproy=re.search(nproyAbierto,lista[i])
		np= verificar_nproy.group()
		np = np.strip()
		if np[-1]!= "}" or lista[i][0]!="\\" or len(proy.group())!= len(np): #texto fuera del nproy
			print "Error , texto afuera de nproy"
			exit()
		if contador!=i:
			marca+=1         #se aumenta el valor de marca, dado que hay error en nproy
		marca+=1             #no hay error en nproy ssi marca=1, es decir, si no entra al if anterior

	#Inicio y fin 
	if re.search(InicioFinPrueba,lista[i]):
		if re.search(inicio,lista[i]) or re.search(fin,lista[i]):
			partida=re.search(InicioFinPrueba,lista[i])
			verificar_ini=re.search(IniFinAbierto,lista[i])
			ini= verificar_ini.group()
			ini = ini.strip()
			#Verificamos texto afuera del comando inicio o fin
			if ini[-1]!= "}" or lista[i][0]!="\\" or len(ini) != len(partida.group()):
				print "Error , texto afuera de un comando"
				exit()
			i+=1
			continue
		else:
			print "Error el inicio/fecha"
			exit()

	#Item
	if re.search(item,lista[i]):
		itemAB=re.search(item,lista[i])
		value= itemAB.group()
		value = value.strip()
		#Se verifica la existencia de texto afuera del comando item
		if value[-1]!= "}" or lista[i][0]!="\\":
			print "Error , texto afuera del item"
			exit()
		if textoAfuera(value)==False:         #se llama a la funcion textoAfuera para comprobar sintaxis
			print "Error, texto fuera de item"
			exit()
	
	#Titulo
	if re.search(titulo,lista[i]):
		verificar_tit=re.search(titulo,lista[i])
		titu=verificar_tit.group()
		titu = titu.strip()
		if titu[-1]!= "}" or lista[i][0]!="\\":
			print len(tit.group()), len(titu)
			print "Error , texto afuera del titulo"
			exit()
		if textoAfuera(titu)==False:         #se llama a la funcion texto afuera para comprobar sintaxis
			print "Error, texto fuera del titulo"
			exit()
	i+=1
#se verifica la marca para ver que nproy se encuentre solo una vez en el texto
if marca!=1:
	print "Error en nproy"
	exit()


#Despues de verificar la sintaxis se crea el archivo html y se recorre la lista
html=open("output.html","w")
html.write("<!DOCTYPE HTML>\n") #Iniciamos documento html
html.write("<head>\n")

for linea in lista:
	title=re.search(nproy,linea)
	start= re.search(inicio,linea)
	end=re.search(fin,linea)
	li=re.search(item,linea)
	encabezado=re.search(titulo,linea)
	separa=re.search(separamiles,linea)
	fechita=re.search(ofecha,linea)
	#Si se encuentra el comando del titulo agregamos titulo
	if title:
		name=title.group()[7:-1]
		html.write("<title>"+name+"</title>\n")
		html.write("</head>\n")
		html.write("<body>\n")
	#Encabezado
	elif encabezado:
		h1=encabezado.group()[8:-1]
		while re.search(fc,h1)!=None:
			h1=cursiva(h1,fc)
		html.write("<h1>"+h1+"</h1>\n")	
	#Inicio
	elif start:
		if start.group()[8:-1] =="lista_enumerada":
			html.write("<ol>\n")
		else:
			html.write("<ul>\n")
	#Fin
	elif end:
		if end.group()[5:-1] =="lista_enumerada":
			html.write("</ol>\n")
		else:
			html.write("</ul>\n")
	#Item
	elif li:
		contenido= li.group()[6:-1]
		#Se verifica la existencia de comandos fn y fc
		while (re.search(fn,contenido)!=None or re.search(fc,contenido)!=None):
			contenido=cursiva(contenido,fc)
			contenido=negrita(contenido,fn)
		html.write("<li>"+contenido+"</li>\n")

	#Si encuentra la funcion separamiles o ofecha
	elif separa or fechita:
		continue
	#Si no se encuentra ningun comando en la linea , se escribe parrafo
	else:
		#Se verifica la existencia de comandos fn y fc
		while (re.search(fn,linea)!=None or re.search(fc,linea)!=None):
			linea=negrita(linea,fn)
			linea=cursiva(linea,fc)
		html.write("<p>"+linea+"</p>\n")
html.write("</body>") #cerramos cuerpo html
#cerramos los archivos trabajados
arch.close()
html.close()