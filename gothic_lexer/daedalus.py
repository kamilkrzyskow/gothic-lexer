"""
Pygments lexer for the Daedalus scripting language used in Piranha Bytes Gothic series.
Run:
pygmentize -l daedalus.py:DaedalusLexer -x -f html -o result_dae.html -O full,debug_token_types <INPUT_FILE>
"""
import re

from pygments.lexer import RegexLexer, bygroups, include, words
from pygments.token import Comment, Keyword, Name, Number, Operator, Punctuation, String, Text

Declaration = Keyword.Declaration
Integer = Number.Integer
Member = Name.Variable.Instance
Namespace = Name.Namespace
Reserved = Keyword.Reserved
Whitespace = Text.Whitespace


class DaedalusLexer(RegexLexer):
    """Pygments lexer for the Daedalus scripting language used in Piranha Bytes Gothic series."""

    name: str = "Daedalus"
    aliases: list[str] = ["pbd", "dae"]
    filenames: list[str] = ["*.d", "*.D"]

    flags: int = re.IGNORECASE

    _global_constants = words({"TRUE", "FALSE"}, suffix=r"\b")
    _implicit_pseudo = words(
        {"SELF", "OTHER", "ITEM", "VICTIM", "HERO", "NULL", "INSTANCE_HELP"}, suffix=r"\b"
    )
    _keywords = words({"RETURN", "WHILE", "CONTINUE", "BREAK"}, suffix=r"\b")

    _basic_var: str = r"[\w_]+"
    _ext_var: str = r"[\w@_^]+"

    tokens = {
        "root": [
            (r"(META)(\s+)", bygroups(Declaration, Whitespace), "meta"),
            (r"(INSTANCE|PROTOTYPE)(\s+)", bygroups(Declaration, Whitespace), "instance-prototype"),
            (
                r"(CLASS)(\s+)(" + _ext_var + r")(\s*)({)",
                bygroups(Declaration, Whitespace, Name.Class, Whitespace, Punctuation),
                "class",
            ),
            (
                r"(NAMESPACE)(\s+)(" + _basic_var + r")(\s*)({)",
                bygroups(Declaration, Whitespace, Namespace, Whitespace, Punctuation),
                "namespace",
            ),
            (
                rf"(FUNC)(\s+)({_basic_var})(\s+)({_ext_var})",
                bygroups(Declaration, Whitespace, Keyword.Type, Whitespace, Name.Function),
                "function-declaration",
            ),
            include("general"),
        ],
        "general": [
            (r"\s+", Whitespace),
            (r"//.*", Comment),
            (r"/\*", Comment.Multiline, "comment-block"),
            (
                rf"(VAR|CONST)(\s+)({_basic_var})(\s+)({_ext_var})",
                bygroups(Declaration, Whitespace, Keyword.Type, Whitespace, Name),
                "var",
            ),
            (r"IF", Reserved, "if-block"),
            (_keywords, Reserved),
            (_global_constants, Keyword.Constant),
            (_implicit_pseudo, Name.Builtin.Pseudo),
            (r"\d+\.\d+", Number.Float),
            (r"\d+", Integer),
            (rf"({_ext_var})(\s*)(:)", bygroups(Name.Label, Whitespace, Punctuation)),
            (rf"({_ext_var})(\s*)(\()", bygroups(Name.Builtin.Other, Whitespace, Punctuation), "parenthesis"),
            (_ext_var, Name),
            (r"\(", Punctuation, "parenthesis"),
            (r"[,.:;{}\[\]]", Punctuation),
            (r"[-+=*/\|&<>!%~]", Operator),
            (r'".*?"', String),
        ],
        "class": [
            (r"}\s*;", Punctuation, "#pop"),
            include("general"),
        ],
        "comment-block": [
            (r"\*/", Comment.Multiline, "#pop"),
            (r"/\*", Comment.Multiline, "#push"),
            (r"[*/]", Comment.Multiline),
            (r"[^*/]+", Comment.Multiline),
        ],
        "function-declaration": [
            (r"\s+", Whitespace),
            (r"\(", Punctuation, "parenthesis"),
            (r"{", Punctuation, "function-inner"),
        ],
        "function-inner": [
            (r"}\s*;", Punctuation, "#pop:2"),
            include("general"),
        ],
        "if-block": [
            (r"}\s*;", Punctuation, "#pop"),
            (r"IF", Reserved, "#push"),
            (r"(ELSE)(\s+)(IF)", bygroups(Reserved, Whitespace, Reserved)),
            (r"ELSE", Reserved),
            include("general"),
        ],
        "instance-prototype": [
            (r"{", Punctuation, "instance-prototype-inner"),
            (r";", Punctuation, "#pop"),
            (_implicit_pseudo, Name.Builtin.Pseudo),
            (_ext_var, Name),
            (r",", Punctuation),
            (r"\s+", Whitespace),
            (
                rf"(\()(\s*)({_ext_var})(\s*)(\))",
                bygroups(Punctuation, Whitespace, Name.Class, Whitespace, Punctuation)
            ),
            include("general"),
        ],
        "instance-prototype-inner": [
            (r"}\s*;", Punctuation, "#pop:2"),
            (r"(\w+)(\s*)(=)", bygroups(Member, Whitespace, Operator)),
            (
                r"(\w+)(\s*)(\[)(\d+)(\])(\s*)(=)",
                bygroups(
                    Member, Whitespace, Punctuation, Integer, Punctuation, Whitespace, Operator
                ),
            ),
            (
                rf"(\w+)(\s*)(\[)({_ext_var})(\])(\s*)(=)",
                bygroups(Member, Whitespace, Punctuation, Name, Punctuation, Whitespace, Operator),
            ),
            include("general"),
        ],
        "meta": [
            (r"}\s*;", Punctuation, "#pop"),
            (r"(\w+)(\s*)(//.*)", bygroups(Member, Whitespace, Comment)),
            (r"(\w+)(\s*)(=)", bygroups(Member, Whitespace, Operator)),
            include("general"),
        ],
        "namespace": [
            (r"}\s*;", Punctuation, "#pop"),
            (
                rf"(NAMESPACE)(\s+)({_basic_var})",
                bygroups(Declaration, Whitespace, Namespace),
                "#push",
            ),
            include("root"),
        ],
        "parenthesis": [
            (r"\)", Punctuation, "#pop"),
            (r"\(", Punctuation, "#push"),
            (
                rf"(VAR|CONST)(\s+)({_basic_var})(\s+)({_ext_var})",
                bygroups(Declaration, Whitespace, Keyword.Type, Whitespace, Name),
                "var-inner",
            ),
            include("general"),
        ],
        "var": [
            (r";", Punctuation, "#pop"),
            (r"\s+", Whitespace),
            include("general"),
        ],
        "var-inner": [
            (r",", Punctuation, "#pop"),
            (r"\)", Punctuation, "#pop:2"),
            (r"\s+", Whitespace),
            (_ext_var, Text),
        ],
    }

    def get_tokens_unprocessed(self, text, stack=("root",)):
        for index, token, value in RegexLexer.get_tokens_unprocessed(self, text, stack):
            if token is Name.Builtin.Other and not value.startswith(self._OTHER):
                token = Name

            if token is Name and value.upper() in self._EXTERNALS:
                yield index, Name.Builtin.Externals, value
            elif token is Name and value.upper() in self._ZPARSEREXTENDER:
                yield index, Name.Builtin.ZParserExtender, value
            else:
                yield index, token, value

    _OTHER: tuple[str] = (
        "LeGo",
        "MEM",
        "CALL",
    )

    _EXTERNALS: set[str] = {
        "AI_AIMAT",
        "AI_ALIGNTOFP",
        "AI_ALIGNTOWP",
        "AI_ASK",
        "AI_ASKTEXT",
        "AI_ATTACK",
        "AI_CANSEENPC",
        "AI_COMBATREACTTODAMAGE",
        "AI_CONTINUEROUTINE",
        "AI_DEFEND",
        "AI_DODGE",
        "AI_DRAWWEAPON",
        "AI_DROPITEM",
        "AI_DROPMOB",
        "AI_EQUIPARMOR",
        "AI_EQUIPBESTARMOR",
        "AI_EQUIPBESTMELEEWEAPON",
        "AI_EQUIPBESTRANGEDWEAPON",
        "AI_FINISHINGMOVE",
        "AI_FLEE",
        "AI_GOTOFP",
        "AI_GOTOITEM",
        "AI_GOTONEXTFP",
        "AI_GOTONPC",
        "AI_GOTOSOUND",
        "AI_GOTOWP",
        "AI_LOOKAT",
        "AI_LOOKATNPC",
        "AI_LOOKFORITEM",
        "AI_OUTPUT",
        "AI_OUTPUTSVM",
        "AI_OUTPUTSVM_OVERLAY",
        "AI_PLAYANI",
        "AI_PLAYANIBS",
        "AI_PLAYCUTSCENE",
        "AI_PLAYFX",
        "AI_POINTAT",
        "AI_POINTATNPC",
        "AI_PRINTSCREEN",
        "AI_PROCESSINFOS",
        "AI_QUICKLOOK",
        "AI_READYMELEEWEAPON",
        "AI_READYRANGEDWEAPON",
        "AI_READYSPELL",
        "AI_REMOVEWEAPON",
        "AI_SETNPCSTOSTATE",
        "AI_SETWALKMODE",
        "AI_SHOOTAT",
        "AI_SND_PLAY",
        "AI_SND_PLAY3D",
        "AI_STANDUP",
        "AI_STANDUPQUICK",
        "AI_STARTSTATE",
        "AI_STOPAIM",
        "AI_STOPFX",
        "AI_STOPLOOKAT",
        "AI_STOPPOINTAT",
        "AI_STOPPROCESSINFOS",
        "AI_TAKEITEM",
        "AI_TAKEMOB",
        "AI_TELEPORT",
        "AI_TURNAWAY",
        "AI_TURNTONPC",
        "AI_TURNTOSOUND",
        "AI_UNEQUIPARMOR",
        "AI_UNEQUIPWEAPONS",
        "AI_UNREADYSPELL",
        "AI_USEITEM",
        "AI_USEITEMTOSTATE",
        "AI_USEMOB",
        "AI_WAIT",
        "AI_WAITFORQUESTION",
        "AI_WAITMS",
        "AI_WAITTILLEND",
        "AI_WHIRLAROUND",
        "AI_WHIRLAROUNDTOSOURCE",
        "APPLY_OPTIONS_AUDIO",
        "APPLY_OPTIONS_CONTROLS",
        "APPLY_OPTIONS_GAME",
        "APPLY_OPTIONS_PERFORMANCE",
        "APPLY_OPTIONS_VIDEO",
        "CONCATSTRINGS",
        "CREATEINVITEM",
        "CREATEINVITEMS",
        "DOC_CREATE",
        "DOC_CREATEMAP",
        "DOC_FONT",
        "DOC_MAPCOORDINATES",
        "DOC_OPEN",
        "DOC_PRINT",
        "DOC_PRINTLINE",
        "DOC_PRINTLINES",
        "DOC_SETFONT",
        "DOC_SETLEVEL",
        "DOC_SETLEVELCOORDS",
        "DOC_SETMARGINS",
        "DOC_SETPAGE",
        "DOC_SETPAGES",
        "DOC_SHOW",
        "EQUIPITEM",
        "EXITGAME",
        "EXITSESSION",
        "FLOATTOINT",
        "FLOATTOSTRING",
        "GAME_INITENGLISH",
        "GAME_INITGERMAN",
        "HLP_CUTSCENEPLAYED",
        "HLP_GETINSTANCEID",
        "HLP_GETNPC",
        "HLP_ISITEM",
        "HLP_ISVALIDITEM",
        "HLP_ISVALIDNPC",
        "HLP_RANDOM",
        "HLP_STRCMP",
        "INFOMANAGER_HASFINISHED",
        "INFO_ADDCHOICE",
        "INFO_CLEARCHOICES",
        "INTRODUCECHAPTER",
        "INTTOFLOAT",
        "INTTOSTRING",
        "LOG_ADDENTRY",
        "LOG_CREATETOPIC",
        "LOG_SETTOPICSTATUS",
        "MDL_APPLYOVERLAYMDS",
        "MDL_APPLYOVERLAYMDSTIMED",
        "MDL_APPLYRANDOMANI",
        "MDL_APPLYRANDOMANIFREQ",
        "MDL_APPLYRANDOMFACEANI",
        "MDL_REMOVEOVERLAYMDS",
        "MDL_SETMODELFATNESS",
        "MDL_SETMODELSCALE",
        "MDL_SETVISUAL",
        "MDL_SETVISUALBODY",
        "MDL_STARTFACEANI",
        "MIS_ADDMISSIONENTRY",
        "MIS_GETSTATUS",
        "MIS_ONTIME",
        "MIS_REMOVEMISSION",
        "MIS_SETSTATUS",
        "MOB_CREATEITEMS",
        "MOB_HASITEMS",
        "NPC_AREWESTRONGER",
        "NPC_CANSEEITEM",
        "NPC_CANSEENPC",
        "NPC_CANSEENPCFREELOS",
        "NPC_CANSEESOURCE",
        "NPC_CHANGEATTRIBUTE",
        "NPC_CHECKAVAILABLEMISSION",
        "NPC_CHECKINFO",
        "NPC_CHECKOFFERMISSION",
        "NPC_CHECKRUNNINGMISSION",
        "NPC_CLEARAIQUEUE",
        "NPC_CLEARINVENTORY",
        "NPC_CREATESPELL",
        "NPC_DELETENEWS",
        "NPC_EXCHANGEROUTINE",
        "NPC_GETACTIVESPELL",
        "NPC_GETACTIVESPELLCAT",
        "NPC_GETACTIVESPELLISSCROLL",
        "NPC_GETACTIVESPELLLEVEL",
        "NPC_GETATTITUDE",
        "NPC_GETBODYSTATE",
        "NPC_GETCOMRADES",
        "NPC_GETDETECTEDMOB",
        "NPC_GETDISTTOITEM",
        "NPC_GETDISTTONPC",
        "NPC_GETDISTTOPLAYER",
        "NPC_GETDISTTOWP",
        "NPC_GETEQUIPPEDARMOR",
        "NPC_GETEQUIPPEDMELEEWEAPON",
        "NPC_GETEQUIPPEDRANGEDWEAPON",
        "NPC_GETGUILDATTITUDE",
        "NPC_GETHEIGHTTOITEM",
        "NPC_GETHEIGHTTONPC",
        "NPC_GETINVITEM",
        "NPC_GETINVITEMBYSLOT",
        "NPC_GETLASTHITSPELLCAT",
        "NPC_GETLASTHITSPELLID",
        "NPC_GETLOOKATTARGET",
        "NPC_GETNEARESTWP",
        "NPC_GETNEWSOFFENDER",
        "NPC_GETNEWSVICTIM",
        "NPC_GETNEWSWITNESS",
        "NPC_GETNEXTTARGET",
        "NPC_GETNEXTWP",
        "NPC_GETPERMATTITUDE",
        "NPC_GETPORTALGUILD",
        "NPC_GETPORTALOWNER",
        "NPC_GETREADIEDWEAPON",
        "NPC_GETSTATETIME",
        "NPC_GETTALENTSKILL",
        "NPC_GETTALENTVALUE",
        "NPC_GETTARGET",
        "NPC_GETTRUEGUILD",
        "NPC_GIVEINFO",
        "NPC_GIVEITEM",
        "NPC_HASBODYFLAG",
        "NPC_HASDETECTEDNPC",
        "NPC_HASEQUIPPEDARMOR",
        "NPC_HASEQUIPPEDMELEEWEAPON",
        "NPC_HASEQUIPPEDRANGEDWEAPON",
        "NPC_HASEQUIPPEDWEAPON",
        "NPC_HASITEMS",
        "NPC_HASNEWS",
        "NPC_HASOFFERED",
        "NPC_HASRANGEDWEAPONWITHAMMO",
        "NPC_HASREADIEDMELEEWEAPON",
        "NPC_HASREADIEDRANGEDWEAPON",
        "NPC_HASREADIEDWEAPON",
        "NPC_HASSPELL",
        "NPC_ISAIMING",
        "NPC_ISDEAD",
        "NPC_ISDETECTEDMOBOWNEDBYGUILD",
        "NPC_ISDETECTEDMOBOWNEDBYNPC",
        "NPC_ISDRAWINGSPELL",
        "NPC_ISDRAWINGWEAPON",
        "NPC_ISINCUTSCENE",
        "NPC_ISINFIGHTMODE",
        "NPC_ISINPLAYERSROOM",
        "NPC_ISINROUTINE",
        "NPC_ISINSTATE",
        "NPC_ISNEAR",
        "NPC_ISNEWSGOSSIP",
        "NPC_ISNEXTTARGETAVAILABLE",
        "NPC_ISONFP",
        "NPC_ISPLAYER",
        "NPC_ISPLAYERINMYROOM",
        "NPC_ISVOICEACTIVE",
        "NPC_ISWAYBLOCKED",
        "NPC_KNOWSINFO",
        "NPC_KNOWSPLAYER",
        "NPC_LEARNSPELL",
        "NPC_MEMORYENTRY",
        "NPC_MEMORYENTRYGUILD",
        "NPC_OWNEDBYGUILD",
        "NPC_OWNEDBYNPC",
        "NPC_PERCDISABLE",
        "NPC_PERCEIVEALL",
        "NPC_PERCENABLE",
        "NPC_PLAYANI",
        "NPC_REFUSETALK",
        "NPC_REMOVEINVITEM",
        "NPC_REMOVEINVITEMS",
        "NPC_SENDPASSIVEPERC",
        "NPC_SENDSINGLEPERC",
        "NPC_SETACTIVESPELLINFO",
        "NPC_SETATTITUDE",
        "NPC_SETKNOWSPLAYER",
        "NPC_SETPERCTIME",
        "NPC_SETREFUSETALK",
        "NPC_SETSTATETIME",
        "NPC_SETTALENTSKILL",
        "NPC_SETTALENTVALUE",
        "NPC_SETTARGET",
        "NPC_SETTEMPATTITUDE",
        "NPC_SETTOFIGHTMODE",
        "NPC_SETTOFISTMODE",
        "NPC_SETTRUEGUILD",
        "NPC_STARTITEMREACTMODULES",
        "NPC_STOPANI",
        "NPC_WASINSTATE",
        "NPC_WASPLAYERINMYROOM",
        "PERC_SETRANGE",
        "PLAYVIDEO",
        "PLAYVIDEOEX",
        "PRINT",
        "PRINTDEBUG",
        "PRINTDEBUGCH",
        "PRINTDEBUGINST",
        "PRINTDEBUGINSTCH",
        "PRINTDIALOG",
        "PRINTMULTI",
        "PRINTSCREEN",
        "RTN_EXCHANGE",
        "SETPERCENTDONE",
        "SND_GETDISTTOSOURCE",
        "SND_ISSOURCEITEM",
        "SND_ISSOURCENPC",
        "SND_PLAY",
        "SND_PLAY3D",
        "TA",
        "TAL_CONFIGURE",
        "TA_BEGINOVERLAY",
        "TA_CS",
        "TA_ENDOVERLAY",
        "TA_MIN",
        "TA_REMOVEOVERLAY",
        "UPDATE_CHOICEBOX",
        "WLD_ASSIGNROOMTOGUILD",
        "WLD_ASSIGNROOMTONPC",
        "WLD_DETECTITEM",
        "WLD_DETECTNPC",
        "WLD_DETECTNPCEX",
        "WLD_DETECTNPCEXATT",
        "WLD_DETECTPLAYER",
        "WLD_EXCHANGEGUILDATTITUDES",
        "WLD_GETDAY",
        "WLD_GETFORMERPLAYERPORTALGUILD",
        "WLD_GETFORMERPLAYERPORTALOWNER",
        "WLD_GETGUILDATTITUDE",
        "WLD_GETMOBSTATE",
        "WLD_GETPLAYERPORTALGUILD",
        "WLD_GETPLAYERPORTALOWNER",
        "WLD_INSERTITEM",
        "WLD_INSERTNPC",
        "WLD_INSERTNPCANDRESPAWN",
        "WLD_INSERTOBJECT",
        "WLD_ISFPAVAILABLE",
        "WLD_ISMOBAVAILABLE",
        "WLD_ISNEXTFPAVAILABLE",
        "WLD_ISRAINING",
        "WLD_ISTIME",
        "WLD_PLAYEFFECT",
        "WLD_REMOVEITEM",
        "WLD_REMOVENPC",
        "WLD_SENDTRIGGER",
        "WLD_SENDUNTRIGGER",
        "WLD_SETGUILDATTITUDE",
        "WLD_SETMOBROUTINE",
        "WLD_SETOBJECTROUTINE",
        "WLD_SETTIME",
        "WLD_SPAWNNPCRANGE",
        "WLD_STOPEFFECT",
    }

    _ZPARSEREXTENDER: set[str] = {
        "AI_CALLSCRIPT",
        "AI_GETNEXTTRIGGERBYFUNC",
        "AI_GETNEXTTRIGGERBYFUNCNAME",
        "AI_GETNEXTTRIGGERBYNPCS",
        "AI_GETNEXTTRIGGERBYOTHER",
        "AI_GETNEXTTRIGGERBYSELF",
        "AI_GETNEXTTRIGGERBYVICTIM",
        "AI_GETTRIGGERBYID",
        "AI_GETTRIGGERFUNC",
        "AI_GETTRIGGERFUNCNAME",
        "AI_GETTRIGGERNPC",
        "AI_GETTRIGGERSNUM",
        "AI_STARTTRIGGERSCRIPT",
        "AI_STARTTRIGGERSCRIPTEX",
        "CAST_CHECKVOBCLASSID",
        "CAST_GETCLASSID",
        "CAST_GETINSTANCEINDEX",
        "CAST_GETVOBCLASSID",
        "CAST_INSTANCEISITEM",
        "CAST_INSTANCEISMOB",
        "CAST_INSTANCEISNPC",
        "CAST_INSTANCETOPOINTER",
        "CAST_POINTERTOINSTANCE",
        "CAST_POINTERTOITEM",
        "CAST_POINTERTONPC",
        "HLP_GAMEONPAUSE",
        "HLP_GETFOCUSVOB",
        "HLP_GETFOCUSVOBNAME",
        "HLP_GETSTEAMPERSONALNAME",
        "HLP_GETSTRINGLENGTH",
        "HLP_HASFOCUSVOB",
        "HLP_ISNULL",
        "HLP_KEYPRESSED",
        "HLP_KEYTOGGLED",
        "HLP_LOGICALKEYTOGGLED",
        "HLP_MESSAGEBOX",
        "HLP_OPTIONISEXISTS",
        "HLP_PRINTCONSOLE",
        "HLP_READOPTIONFLOAT",
        "HLP_READOPTIONINT",
        "HLP_READOPTIONSTRING",
        "HLP_WRITEOPTIONFLOAT",
        "HLP_WRITEOPTIONINT",
        "HLP_WRITEOPTIONSTRING",
        "ISNAN",
        "LOG_GETTOPICSECTION",
        "LOG_GETTOPICSTATUS",
        "MDL_ANIMATIONISACTIVE",
        "MDL_ANIMATIONISEXISTS",
        "MDL_APPLYOVERLAYMDS_ATFIRST",
        "MDL_GETANIMATIONINDEX",
        "MDL_GETANIMATIONNAME",
        "MDL_RESETALLANIMATIONSFPS",
        "MDL_RESETANIMATIONFPS",
        "MDL_RESETNPCSPEEDMULTIPLIER",
        "MDL_SETALLANIMATIONSFPS",
        "MDL_SETANIMATIONFPS",
        "MDL_SETNPCSPEEDMULTIPLIER",
        "MDL_SETVISIBLE",
        "MENU_SEARCHITEMS",
        "MOB_DESTROY",
        "MOB_GETKEYINSTANCE",
        "MOB_GETLOCKCOMBINATION",
        "MOB_INSERTITEM",
        "MOB_INSERTITEMS",
        "MOB_ISLOCKED",
        "MOB_REMOVEITEM",
        "MOB_REMOVEITEMS",
        "MOB_SETKEYINSTANCE",
        "MOB_SETLOCKCOMBINATION",
        "MOB_SETLOCKED",
        "NPC_GETLEFTHANDITEM",
        "NPC_GETRIGHTHANDITEM",
        "NPC_GETSLOTITEM",
        "NPC_OPENINVENTORY",
        "NPC_OPENINVENTORYSTEAL",
        "NPC_OPENINVENTORYTRADE",
        "NPC_PUTINSLOT",
        "NPC_REMOVEFROMSLOT",
        "NPC_SETASHERO",
        "PAR_GETPARSERID",
        "PAR_GETSYMBOLID",
        "PAR_GETSYMBOLLENGTH",
        "PAR_GETSYMBOLVALUEFLOAT",
        "PAR_GETSYMBOLVALUEFLOATARRAY",
        "PAR_GETSYMBOLVALUEINSTANCE",
        "PAR_GETSYMBOLVALUEINT",
        "PAR_GETSYMBOLVALUEINTARRAY",
        "PAR_GETSYMBOLVALUESTRING",
        "PAR_GETSYMBOLVALUESTRINGARRAY",
        "PAR_SETSYMBOLVALUEFLOAT",
        "PAR_SETSYMBOLVALUEFLOATARRAY",
        "PAR_SETSYMBOLVALUEINSTANCE",
        "PAR_SETSYMBOLVALUEINT",
        "PAR_SETSYMBOLVALUEINTARRAY",
        "PAR_SETSYMBOLVALUESTRING",
        "PAR_SETSYMBOLVALUESTRINGARRAY",
        "STR_FORMAT",
        "STR_GETCURRENTCP",
        "STR_GETLENGTH",
        "STR_GETLOCALIZEDSTRING",
        "STR_GETLOCALIZEDSTRINGEX",
        "STR_UTF8_TO_ANSI",
        "WLD_CHANGELEVEL",
        "WLD_FINDVOB",
        "WLD_GETWEATHERTYPE",
        "WLD_PLAYEFFECTAT",
        "WLD_PLAYEFFECTVOB",
        "WLD_SETWEATHERTYPE",
        "WLD_TOGGLERAIN",
    }


def main():
    import sys

    if len(sys.argv) == 1:
        sys.exit("No file provided")

    with open(sys.argv[1]) as file:
        source = file.read()

    tokens = DaedalusLexer().get_tokens(source)

    for token in tokens:
        print(token)


if __name__ == "__main__":
    main()
