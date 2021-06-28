from Crypto.Util.number import bytes_to_long

coeff = [6484546390062521637317439294277882416678715709573542399510825949010244923470820534128395775792698001803897492814775093578709258771641505585967366699015059, 13277902340441197246567725778100204509280776661999209227896094428327622723039583714726166276314276370591264817761656106482364825932600618099436868012246542, 5569691405670980897828722326587617598774769523521099186281100255117574427398911341368942458388688332548519800875420529830908747106276869276436164595500337, 8406294415712389214320953233788256642887491830781641468433430158514377860135904870393127152291801658743566164516286411055548603233912506125472492384840356, 13355881396510163694364715177716073817296741511856371213169373799254507139997307059210783369340455319373052167868752902051097779964937772728882008097585569, 3648151137121977286112718952274983356658558660279750209939861301832619693753209610765803989080997802395920945017336608704436570181169399997986963848784405, 12172247866967866174498014978375860550450347110905636929410629208626394056487463588986230586032160820823810395595579288955820875178503787597567496157243178, 4395044193758142711266168230151726401437550389966508417775440778004258692883137786272642875326945881997533098728645473360740290133827767452908699379611948, 12010413061855321385147400369230766707687884965867638985184558713248574329822759205942219764164801994819359410755817106287261696022404106665890964297490315, 3473308757282001157351523458239675017364514597483100180807243200217136102882113210014752828594028365245409561302876134913436637561609880919747770379993467]

flag = b'greyhats{??????????????????????????????}'

assert len(flag) == 40

mod = 1 << 512

def hash(msg, coeff):
    result = 0
    for i in range(0, len(msg), 4):
        a = bytes_to_long(flag[i:i+4])
        b = coeff[(i//4) % len(coeff)]
        result = (result + a * b) % mod
    return result


f = open('output.txt', 'w')

f.write(hex(hash(flag, coeff)))
