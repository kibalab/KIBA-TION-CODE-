import random
import urllib.request 
import shutil 
import sys 
import imp 
from bs4 import BeautifulSoup
a_oper = [
["슬레지","M590A1","L85A2",["P226 MK 25","SMG-11"]]
,["대처","AR33","L85A2","M590A1",["P226 MK 25"]]
,["애쉬","G36C","R4-C",["M45 MEUSOC","5.7 USG"]]
,["서마이트","M1014","556XI",["M45 MEUSOC","5.7 USG"]]
,["트위치","F2","417","SG-CQB",["P9","LFP586"]]
,["몽타뉴","확장형 방패",["P9","LFP586"]]
,["글라즈","OTs-03",["GSH-18","PMM"]]
,["퓨즈","사격 방패","6P41","AK-12",["GSH-18","PMM"]]
,["블리츠","특수 섬광 방패",["P12"]]
,["아이큐","AUG A2","552 COMMANDO","G8A1",["P12"]]
,["벅","C8-SFW","CAMRS",["MK1 9mm"]]
,["블랙비어드","MK17 CQB","SR-25",["D-50"]]
,["카피탕","PARA-308","M249",["PRB92"]]
,["히바나","SUPERNOVA","TYPE-89",["P229","BEARING 9"]]
,["자칼","C7E","PDW9","ITA12L",["USP40","ITA12S"]]
,["잉","T-95 LSW","SIX12",["Q-929"]]
,["조피아","LMG-E","M762",["RG15"]]
,["도깨비","Mk.14 EBR","BOSG. 12. 2",["C75 Auto","SMG-12 MP"]]
,["라이온","V308","417","SG-CQB",["P9","LFP586"]]
,["핀카","SPEAR .308","SASG-12","6P41",["PMM","GSH-18"]]]

a_oper_en = ["sledge","thatcher","ash","thermite","twitch","montagne","glaz","fuze","blitz","iq","buck","blackbeard","capitao","hibana","jackal","ying","zofla","dokkaebl","lion","finka"]

d_oper = [
["스모크","FMG-9","M590A1",["P226 MK 25","SMG-11"]]
,["뮤트","MP5K","M590A1",["P226 MK 25"]]
,["캐슬","M1014","UMP45",["M45 MEUSOC","5.7 USG"]]
,["펄스","M1014","UMP45",["M45 MEUSOC","5.7 USG"]]
,["닥","MP5","P90","SG-CQB",["P9","LFP586"]]
,["룩","MP5","P90","SG-CQB",["P9","LFP586"]]
,["캅칸","SASG-12","9x19 VSN",["GSH-18","PMM"]]
,["타찬카","SASG-12","9x19 VSN",["GSH-18","PMM"]]
,["예거","416-C CARBINE","M870",["P12"]]
,["밴딧","MP7","M870",["P12"]]
,["프로스트","9mm C1","SUPER 90",["MK1 9mm"]]
,["발키리","MPX","SPAS-12",["D-50"]]
,["카베이라","M12","SPAS-12",["LUISON"]]
,["에코","SUPERNOVA","MP5SD",["P229","BEARING 9"]]
,["미라","Vector .45 ACP","ITA12L",["USP40","ITA12S"]]
,["리전","SIX12 SD","T-5 SMG",["Q-929"]]
,["엘라","SCORPION EVO 3 A1","FO-12",["RG15"]]
,["비질","K1A","BOSG. 12. 2",["C75 Auto","SMG-12 MP"]]
,["마에스트로","ALDA 5.56","ACS12",["KERATOS .357","Bailiff 410"]]
,["알리바이","Mx4 Storm","ACS12",["KERATOS .357","Bailiff 410"]]
]

d_oper_en = ["smoke","mute","castle","pulse","doc","rook","kapkan","tachanka","jager","bandit","frost","valkyrie","caveira","echo","mira","lesion","ela","vigil", "maestro", "alibi"]

def image(oper):
    req = urllib.request.Request("https://rainbow6.ubisoft.com/siege/en-us/game-info/operators/"+oper+"/index.aspx")
    data = urllib.request.urlopen(req).read()
    bs = BeautifulSoup(data, 'html.parser')
    span = bs.find_all('span')
    for ele in span:
        val = ele.get('class')
        if val != None and val[0] == "ico":
            print(ele.img.get('src'))
            return ele.img.get('src')
    return "https://pbs.twimg.com/profile_images/945079417109385216/l0FfXDZg_400x400.jpg"

def defence():
    d_choice_oper = random.randrange(0,20)
    print(d_oper[d_choice_oper][0])
    d_selec_oper = d_oper[d_choice_oper][0]
    d_choice_am_j = random.randrange(1,len(d_oper[d_choice_oper])-1)
    print(d_oper[d_choice_oper][d_choice_am_j])
    d_selec_am_j = d_oper[d_choice_oper][d_choice_am_j]
    d_choice_am_b = random.randrange(0,len(d_oper[d_choice_oper][-1]))
    print(d_oper[d_choice_oper][-1][d_choice_am_b-1])
    d_selec_am_b = d_oper[d_choice_oper][-1][d_choice_am_b-1]
	
    img = image(d_oper_en[d_choice_oper])

    return d_selec_oper, d_selec_am_j, d_selec_am_b, img
def attack():
    a_choice_oper = random.randrange(0,20)
    print(a_oper[a_choice_oper][0])
    a_selec_oper = a_oper[a_choice_oper][0]
    a_choice_am_j = random.randrange(1,len(a_oper[a_choice_oper])-1)
    print(a_oper[a_choice_oper][a_choice_am_j])
    a_selec_am_j = a_oper[a_choice_oper][a_choice_am_j]
    a_choice_am_b = random.randrange(0,len(a_oper[a_choice_oper][-1]))
    print(a_oper[a_choice_oper][-1][a_choice_am_b-1])
    a_selec_am_b = a_oper[a_choice_oper][-1][a_choice_am_b-1]

    img = image(a_oper_en[a_choice_oper])

    return a_selec_oper, a_selec_am_j, a_selec_am_b, img