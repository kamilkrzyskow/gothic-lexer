/*
    An example of a valid NPC Daedalus file + some misc content
*/

var int hry_hello_count;
const int hry_hello_threshold = 3;
const int hry_hello_exp = 100;
const string npc_name_hry = "HRY";

instance VLK_123456_HRY (Npc_Default)
{
    name = npc_name_hry;
    guild = GIL_NONE;
    id = 123456;
    voice = 9;
    flags = NPC_FLAG_IMMORTAL;
    npctype = NPCTYPE_MAIN;
    fight_tactic = FAI_HUMAN_STRONG;
    daily_routine = Rtn_Entry_123456;
    aivar[AIV_ToughGuy] = TRUE;

    B_SetAttributesToChapter(self, 4);

    CreateInvItems(self, ItMw_HRYSword, 1);
    CreateInvItems(self, ItMi_OldCoin, 1);

    EquipItem(self, ItMw_HRYSword);

    B_SetNpcVisual(self, MALE, "Hum_Head_Thief", Face_N_HRY, BodyTex_N, ITAR_Vlk_L);
    Mdl_SetModelFatness(self, 0);
    Mdl_ApplyOverlayMds(self, "Humans_Relaxed.mds");

    B_GiveNpcTalents(self);
    B_SetFightSkills(self, 99);
};

FUNC VOID Rtn_Entry_123456()
{
    TA_Stand_Guarding(08, 00, 20, 00, "HRY_WP");
    TA_Stand_Guarding(20, 00, 08, 00, "HRY_WP");
};

INSTANCE DIA_HRY_EXIT(C_INFO)
{
    npc = VLK_123456_HRY;
    nr = 999;
    condition = DIA_HRY_EXIT_Condition;
    information = DIA_HRY_EXIT_Info;
    permanent = TRUE;
    description = DIALOG_ENDE;
};

FUNC INT DIA_HRY_EXIT_Condition()
{
    return TRUE;
};

FUNC VOID DIA_HRY_EXIT_Info()
{
    AI_StopProcessInfos(self);
};

INSTANCE DIA_HRY_HELLO (C_INFO)
{
    npc = VLK_123456_HRY;
    nr = 1;
    condition = DIA_HRY_HELLO_Condition;
    information = DIA_HRY_HELLO_Info;
    permanent = TRUE;
    description = "Hi, do you know something about regular expressions?";
};

func int DIA_HRY_HELLO_Condition()
{
    return TRUE;
};

func void DIA_HRY_HELLO_Info()
{
    hry_hello_count = hry_hello_count + 1;

    AI_Output(other, self, "DIA_HRY_HELLO_15_00"); //Hi, do you know something about regular expressions?

    if (hry_hello_count < hry_hello_threshold) {
        if (hry_hello_count == 1) {
            AI_Output(self, other, "DIA_HRY_HELLO_09_01"); //Hello, I would rather not talk about them.
        } else {
            AI_Output(self, other, "DIA_HRY_HELLO_09_02"); //...
        };
    } else if (hry_hello_count == hry_hello_threshold) {
        AI_Output(self, other, "DIA_HRY_HELLO_09_03"); //Stop bothering me! Go ask someone else!
        B_GivePlayerXP(hry_hello_exp);
    } else {
        AI_Output(self, other, "DIA_HRY_HELLO_09_04"); //Enough!
    };

    AI_StopProcessInfos(self);

    if (hry_hello_count > hry_hello_threshold) {
        b_attack(self, other, AR_NONE, 0);
    };
};

namespace MiscExample
{
    func void add_exp_1000()
    {
        B_GivePlayerXP(1000);
    };
};

func void misc_example()
{
    MiscExample:add_exp_1000();
};

CLASS C_NPC
{
    VAR INT id;
    VAR STRING name[5];
    // ...
    VAR INT attribute[ATR_INDEX_MAX];
    var int HitChance[MAX_HITCHANCE];
    VAR INT protection[PROT_INDEX_MAX];
    VAR INT damage[DAM_INDEX_MAX];
    VAR INT damagetype;
    VAR INT guild, level;

    VAR FUNC mission [MAX_MISSIONS];
    var INT fight_tactic;
    VAR INT weapon;

    // ...

    VAR FUNC daily_routine;
    VAR FUNC start_aistate;

    VAR string spawnPoint;
    VAR int spawnDelay;
    // ...
};

INSTANCE self,other (C_NPC);

INSTANCE victim(C_NPC);

instance item (C_Item);