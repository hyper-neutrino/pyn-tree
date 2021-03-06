import sys

code_page  = """¡¢£¤¥¦©¬®µ½¿€ÆÇÐÑ×ØŒÞßæçðıȷñ÷øœþ !"#$%&'()*+,-./0123456789:;<=>?"""
code_page += """@ABCDEFGHIJKLMNOPQRSTUVWXYZ[\]^_`abcdefghijklmnopqrstuvwxyz{|}~¶"""
code_page += """°¹²³⁴⁵⁶⁷⁸⁹⁺⁻⁼⁽⁾ƁƇƊƑƓƘⱮƝƤƬƲȤɓƈɗƒɠɦƙɱɲƥʠɼʂƭʋȥẠḄḌẸḤỊḲḶṂṆỌṚṢṬỤṾẈỴẒȦḂ"""
code_page += """ĊḊĖḞĠḢİĿṀṄȮṖṘṠṪẆẊẎŻạḅḍẹḥịḳḷṃṇọṛṣṭ§Äẉỵẓȧḃċḋėḟġḣŀṁṅȯṗṙṡṫẇẋẏż«»‘’“”"""

getters = {}

def Getter(name):
	def wrapper(function):
		getters[name] = function
		return function
	return wrapper

def getstr(code):
	if not code: return "tryinput()"
	c = code.pop(0)
	if c not in getters:
		return ""
	return getters[c](code)

def transpile(code):
	output = """# Python code transpiled from %d bytes of PynTree code

global_register = {}

def assign(name, val):
	global_register[name] = val
	return val

current = None

def stash(val):
	global current
	current = val
	return val

def cache():
	return current

import sys, builtins, ast, functools, regex

def getval(name):
	if name in global_register: return global_register[name]
	if name in globals(): return globals()[name]
	if name in dir(builtins): return getattr(builtins, name)
	return 0

def tryinput():
	val = input()
	try: return ast.literal_eval(val)
	except: return val

def deduplicate(array):
	output = []
	seen = {}
	for obj in array:
		if obj not in seen:
			output.append(obj)
			seen.add(obj)
	return output

def listassign(array, index, item):
	ensuresize(array, index)
	array[index] = item
	return item

def ensuresize(array, index, value = 0):
	if -len(array) > index < 0:
		array[:] = [value for _ in range(len(array) - index)] + array
	elif len(array) <= index > 0:
		array[:] = array + [value for _ in range(index - len(array) + 1)]
	elif 0 == index == len(array):
		array.append(value)

def getintable(obj):
	if type(obj) == str:
		return obj
	else:
		try:
			return "".join("0123456789abcdefghijklmnopqrstuvwxyz"[y] for y in obj)
		except:
			return "0"

def concat(left, right):
	if hasattr(left, "__iter__"): left = list(left)
	else: left = [left]
	if hasattr(right, "__iter__"): right = list(right)
	else: right = [right]
	return left + right

def wloop(cond, iter):
	output = 0
	while cond():
		output = iter()
	return output

def numerify(obj):
	try:
		return int(obj)
	except:
		try:
			return float(obj)
		except:
			try:
				return complex(obj)
			except:
				return obj

def fallthrough(a, **k):
	return print(a, **k) or a

""" % len(code)
	code = list(code)
	while code:
		output += getstr(code) + "\n"
	return output

@Getter("C")
def oneArgFuncCall(code):
	return "(%s)(%s)" % (getstr(code), getstr(code))

@Getter("Ċ")
def readchar(code):
	return "sys.stdin.read(1)"

@Getter("ċ")
def readchars(code):
	return "sys.stdin.read(%s)"

@Getter("E")
def evalinput(code):
	return "eval(input())"

@Getter("D")
def declare(code):
	return "assign('%s', %s)" % (code.pop(0), getstr(code))

@Getter("€")
def listcompx(code):
	return "[[assign('x', x)] and %s for x in %s]" % (getstr(code), getstr(code))

@Getter("F")
def repeatloop(code):
	times = getstr(code)
	return "[%s for _ in range(%s)]" % (getstr(code), times)

@Getter("Ḟ")
def listcomp(code):
	return "[[assign('%s', x)] and %s for x in %s]" % (code.pop(0), getstr(code), getstr(code))

@Getter("G")
def getvarname(code):
	return "getval(%s)" % getstr(code)

@Getter("I")
def getint(code):
	return "int(input())"

@Getter("J")
def joiner(code):
	return "''.join(map(str, %s))" % getstr(code)

@Getter("L")
def getlength(code):
	return "len(%s)" % getstr(code)

@Getter("Ŀ")
def getlist(code):
	return "list(input())"

@Getter("Ḷ")
def lowerrange(code):
	return "list(range(int(%s)))" % getstr(code)

@Getter("Ṁ")
def maxgetter(code):
	return "max(%s)" % getstr(code)

@Getter("Ṃ")
def mingetter(code):
	return "min(%s)" % getstr(code)

@Getter("N")
def getnumber(code):
	return "numerify(input())"

@Getter("O")
def getord(code):
	return "ord(%s)" % getstr(code)

@Getter("Ȯ")
def getchr(code):
	return "chr(int(%s))" % getstr(code)

@Getter("P")
def pythonprint(code):
	return "fallthrough(%s)" % getstr(code)

@Getter("Ƥ")
def pythonoutput(code):
	return "fallthrough(%s, end = '')" % getstr(code)

@Getter("Q")
def deduplicate(code):
	return "deduplicate(%s)" % getstr(code)

@Getter("R")
def upperrange(code):
	return "list(range(1, 1 + int(%s)))" % getstr(code)

@Getter("S")
def getstring(code):
	return "input()"

@Getter("Ṡ")
def sorter(code):
	return "sorted(%s)" % getstr(code)

@Getter("Ṣ")
def rsorter(code):
	return "sorted(%s, reverse = True)" % getstr(code)

@Getter("a")
def pythonand(code):
	return "(%s and %s)" % (getstr(code), getstr(code))

@Getter("c")
def splatFuncCall(code):
	return "(%s)(*%s)" % (getstr(code), getstr(code))

@Getter("ċ")
def multiFuncCall(code):
	func = getstr(code)
	arglist = []
	while code and code[0] != "}":
		arglist.append(getstr(code))
	if code: code.pop(0)
	return "(%s)(%s)" % (func, ", ".join(arglist))

@Getter("d")
def setlongvar(code):
	return "assign(%s, %s)" % (getstr(code), getstr(code))

@Getter("e")
def evaler(code):
	return "eval(%s)" % getstr(code)

@Getter("f")
def listcompxcond(code):
	return "[%s for x in %s if [assign('x', x)] and %s]" % (getstr(code), getstr(code), getstr(code))

@Getter("ḟ")
def listcompcond(code):
	varname = code.pop(0)
	return "[%s for x in %s if [assign('%s', x)] and %s]" % (getstr(code), getstr(code), varname, getstr(code))

@Getter("g")
def getlongvar(code):
	output = ""
	while code and code[0].isidentifier():
		output += code.pop(0)
	if code: code.pop(0)
	return "getval('%s')" % output

@Getter("i")
def toint(code):
	return "int(%s)" % getstr(code)

@Getter("ị")
def tointbase(code):
	return "int(getintable(%s), %s)" % (getstr(code), getstr(code))

@Getter("j")
def customjoiner(code):
	return "(%s).join(map(str, %s))" % (getstr(code), getstr(code))

@Getter("l")
def tolist(code):
	return "list(%s)" % getstr(code)

@Getter("ḷ")
def toset(code):
	return "set(%s)" % getstr(code)

@Getter("ṁ")
def maxkey(code):
	return "max(%s, key = lambda x: %s)" % (getstr(code), getstr(code))

@Getter("ṃ")
def minkey(code):
	return "min(%s, key = lambda x: %s)" % (getstr(code), getstr(code))

@Getter("n")
def tonumber(code):
	return "numerify(%s)" % getstr(code)

@Getter("o")
def pythonor(code):
	return "(%s or %s)"

@Getter("s")
def tostring(code):
	return "str(%s)" % getstr(code)

@Getter("ṡ")
def keysorter(code):
	return "sorted(%s, key = lambda x: [assign('x', x)] and %s)" % (getstr(code), getstr(code))

@Getter("ṣ")
def rkeysorter(code):
	return "sorted(%s, reverse = True, key = lambda x: [assign('x', x)] and %s)" % (getstr(code), getstr(code))

@Getter("w")
def varW(code):
	return "getval('w')"

@Getter("x")
def varX(code):
	return "getval('x')"

@Getter("y")
def varY(code):
	return "getval('y')"

@Getter("z")
def varZ(code):
	return "getval('z')"

@Getter("1")
def num1(code):
	return "1" + consumeNum(code)

@Getter("2")
def num2(code):
	return "2" + consumeNum(code)

@Getter("3")
def num2(code):
	return "3" + consumeNum(code)

@Getter("4")
def num2(code):
	return "4" + consumeNum(code)

@Getter("5")
def num2(code):
	return "5" + consumeNum(code)

@Getter("6")
def num2(code):
	return "6" + consumeNum(code)

@Getter("7")
def num2(code):
	return "7" + consumeNum(code)

@Getter("8")
def num2(code):
	return "8" + consumeNum(code)

@Getter("9")
def num2(code):
	return "9" + consumeNum(code)

@Getter("0")
def num2(code):
	return "0" + consumeNum(code)

@Getter("-")
def negnum(code):
	return "-" + consumeNum(code, neg = False)

@Getter(".")
def decnum(code):
	return "." + consumeNum(code, decimal = False)

@Getter("'")
def schar(code):
	return "'%s'" % code.pop(0) if code[0] != "\\" else "'%s'" % (code.pop(0) + code.pop(0))

@Getter('"')
def gstr(code):
	output = '"'
	while code:
		c = code.pop(0)
		if c == '"':
			break
		elif c == "\\":
			output += "\\" + code.pop(0)
		else:
			output += c
	return output + '"'

@Getter("\n")
@Getter(" ")
def empty(code):
	return getstr(code)

@Getter("ø")
def subgetraw(code):
	attrname = ""
	while code and code[0].isidentifier():
		attrname += code.pop(0)
	if code: code.pop(0)
	return "getattr(%s, %r)" % (getstr(code), attrname)

binfunc = {
	"Ø": "getattr({L}, {R})",
	"+": "({L} + {R})",
	"_": "({L} - {R})",
	"×": "({L} * {R})",
	"%": "({L} % {R})",
	":": "({L} // {R})",
	"÷": "({L} / {R})",
	"*": "({L} ** {R})",
	"&": "({L} & {R})",
	"|": "({L} | {R})",
	"^": "({L} ^ {R})",
	">": "({L} > {R})",
	"<": "({L} < {R})",
	";": "concat({L}, {R})",
	"=": "({L} == {R})",
	"⁻": "({L} != {R})",
	"ė": "({L} in {R})",
	"ẹ": "({L} not in {R})"
}

for key in binfunc:
	Getter(key)((lambda t: lambda code: t.format(L = getstr(code), R = getstr(code)))(binfunc[key]))

@Getter("¬")
def logical_not(code):
	return "(not %s)" % getstr(code)

@Getter("?")
def condif(code):
	condition = getstr(code)
	return "(%s if %s else None)" % (getstr(code), condition)

@Getter("¿")
def condifelse(code):
	condition = getstr(code)
	return "(%s if %s else %s)" % (getstr(code), condition, getstr(code))

@Getter("¤")
def block(code):
	output = []
	while code and code[0] != "}":
		output.append(getstr(code))
	if code: code.pop(0)
	return "(" + " and ".join("[%s]" % k for k in output) + ")[0]" if output else "0"

@Getter("⁺")
def selfie(code):
	return ("(lambda a: %s)(%s)" % (binfunc[code.pop(0)], getstr(code))).format(L = "a", R = "a")

@Getter("¡")
def whileloop(code):
	return "wloop(lambda: (%s), lambda: (%s))" % (getstr(code), getstr(code))

@Getter("#")
def arrayaccess(code):
	return "(%s)[%s]" % (getstr(code), getstr(code))

@Getter("/")
def reducer(code):
	return ("functools.reduce(lambda a, b: %s, %s)" % (binfunc[code.pop(0)], getstr(code))).format(L = "a", R = "b")

@Getter("\\")
def insertraw(code):
	return code.pop(0)

@Getter("`")
def slicer(code):
	if code[0] == "`":
		code.pop(0)
		return "%s:%s:%s" % (getstr(code), getstr(code), getstr(code))
	else:
		return "%s:%s" % (getstr(code), getstr(code))

@Getter("¦")
def dictentry(code):
	return "%s: %s" % (getstr(code), getstr(code))

@Getter("þ")
def switcher(code):
	cases = {}
	while code and code[0] != "}":
		key = getstr(code)
		cases[key] = "lambda: " + getstr(code)
	if code: code.pop(0)
	return "{%s}.get(%s, lambda:0)()" % (", ".join("(%s): (%s)" % (key, cases[key]) for key in cases), getstr(code))

@Getter("Þ")
def switcherdefault(code):
	cases = {}
	while code and code[0] != "}":
		key = getstr(code)
		cases[key] = "lambda: " + getstr(code)
	if code: code.pop(0)
	default_case = getstr(code)
	return "{%s}.get(%s, lambda: %s)()" % (", ".join("(%s): (%s)" % (key, cases[key]) for key in cases), getstr(code), default_case)

@Getter("Ƭ")
def translate(code):
	translation = {}
	while code and code[0] != "}":
		key = code.pop(0)
		translation[ord(key)] = getstr(code)
	if code: code.pop(0)
	return "str(%s).translate({%s})" % (getstr(code), ", ".join("%d: %s" % (key, translation[key]) for key in translation))

@Getter("§")
def funcdef(code):
	args = []
	splat = code[0] == "*"
	if splat: code.pop(0)
	while code and code[0] != ":":
		args.append(code.pop(0))
	if code: code.pop(0)
	return "lambda " + "*" * splat + ", ".join(args) + ": " + "[0, " + ", ".join("assign('%s', %s)" % (name, name) for name in args) + "] and " + getstr(code)

@Getter("[")
def formlist(code):
	output = []
	while code and code[0] != "]":
		output.append(getstr(code))
	if code: code.pop(0)
	return "[" + ", ".join(output) + "]"

@Getter("{")
def formlist(code):
	output = []
	while code and code[0] != "}":
		output.append(getstr(code))
	if code: code.pop(0)
	return "{" + ", ".join(output) + "}" if output else "set()"

@Getter("ß")
def reassign(code):
	func = binfunc[code.pop(0)]
	varname = code.pop(0)
	return "assign('%s', %s)" % (varname, func.format(L = "getval('%s')" % varname, R = getstr(code)))

@Getter("æ")
def specials(code):
	if code[0] in special_format: format = special_format[code.pop(0)]
	else: return getstr(code)
	return format % tuple(getstr(code) for _ in range(format.count("%s") + format.count("%r") + format.count("%d")))

@Getter("Æ")
def specialcalls(code):
	if code[0] in special_format: format = special_format[code.pop(0)] + "(%s)"
	else: return getstr(code)
	return format % tuple(getstr(code) for _ in range(format.count("%s") + format.count("%r") + format.count("%d")))

special_format = {
	"a": "(%s).append",
	"c": "(%s).count",
	"e": "(%s).extend",
	"ė": "eval",
	"ẹ": "exec",
	"f": "(%s).find",
	"I": "(%s).insert(%s, %s)",
	"i": "(%s).index",
	"p": "pyntree_eval",
	"r": "(%s).replace",
	"S": "ensuresize(%s, %s)",
	"s": "ensuresize(%s, %s, %s)",
	"T": "transpile",
	"=": "%s = %s",
	"#": "listassign(%s, %s, %s)",
}

@Getter("ɼ")
def regex_specials(code):
	if code[0] in regex_format: format = regex_format[code.pop(0)]
	else: format = "regex.find(%s, %s)"
	return format % tuple(getstr(code) for _ in range(format.count("%s") + format.count("%r") + format.count("%d")))

regex_format = {
	"f": "(stash(regex.search(%s, %s)) and cache().group(0))",
	"s": "regex.search(%s, %s)",
	"g": "(%s).group(%s)",
	"G": "(%s).group(0)",
	"p": "(%s).groups()",
	"b": "(stash(regex.match(%s, %s)) and cache().group(0))",
	"m": "regex.match(%s, %s)",
	"a": "regex.findall(%s, %s)",
	"r": "regex.sub(%s, %s, %s)",
}

def consumeNum(code, digits = "0123456789", neg = True, decimal = True):
	output = ""
	while code and (code[0] in digits or code[0] == "-" and neg or code[0] == "." and decimal):
		if code[0] == "-": neg = False
		if code[0] == ".": decimal = False
		output += code.pop(0)
	return output

def pyntree_eval(code):
	exec(transpile(code))

flag_file = "f" in sys.argv[1]
flag_utf8 = "u" in sys.argv[1]

if flag_file:
	with open(sys.argv[2], "rb") as f:
		code = f.read()
	if flag_utf8:
		code = "".join(char for char in code.decode("utf-8") if char in code_page)
	else:
		code = "".join(code_page[i] for i in code)
else:
	code = sys.argv[2]
	if flag_utf8:
		code = "".join(char for char in code if char in code_page)
	else:
		code = "".join(code_page[ord(i)] for i in code)

trans = transpile(code)

if "--transpile" in sys.argv:
	print(trans)
else:
	exec(trans)
