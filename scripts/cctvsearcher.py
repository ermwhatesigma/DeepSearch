import os
import requests
import re
from colorama import init


black="\033[0;30m"
red="\033[0;31m"
green="\033[0;32m"
yellow="\033[0;33m"
blue="\033[0;34m"
purple="\033[0;35m"
cyan="\033[0;36m"
white="\033[0;37m"

def start():
    os.system('cls' if os.name == 'nt' else 'clear')
    print("\n-------------------------------------------------------------------------------------------------------------------------------")
    print("■■             ■■  ■■■■■■■  ■■         ■■■■■■    ■■■■■        ■■■   ■■■      ■■■■■■■")
    print(" ■■           ■■   ■■       ■■        ■■       ■■     ■■     ■■ ■■ ■■ ■■     ■■     ")
    print("  ■■   ■■■   ■■    ■■■■■■■  ■■       ■■        ■■     ■■    ■■   ■■■   ■■    ■■■■■■■")
    print("   ■■ ■■ ■■ ■■     ■■       ■■        ■■       ■■     ■■   ■■           ■■   ■■     ")
    print("    ■■■   ■■■      ■■■■■■■  ■■■■■■■    ■■■■■■    ■■■■■    ■■             ■■  ■■■■■■■")
    print("")
    print("■■■■■■■■    ■■■■■")
    print("   ■■     ■■     ■■")
    print("   ■■     ■■     ■■")
    print("   ■■     ■■     ■■")
    print("   ■■       ■■■■■")
    print("")
    print("■■■■■■     ■■■■■■■  ■■■■■■■  ■■■■■■  ")
    print("■■   ■■    ■■       ■■       ■■   ■■")
    print("■■    ■■   ■■■■■■■  ■■■■■■■  ■■■■■■  ")
    print("■■   ■■    ■■       ■■       ■■      ")
    print("■■■■■■     ■■■■■■■  ■■■■■■■  ■■      ")
    print("                                   ■■■■■   ■■■■■■■      ■■■■      ■■■■■■      ■■■■■■  ■■    ■■  ■■■■■■■  ■■■■■■")
    print("                                  ■■       ■■          ■■  ■■     ■■   ■■    ■■       ■■    ■■  ■■       ■■   ■■")
    print("                                   ■■■■■   ■■■■■■■    ■■■■■■■■    ■■■■■■    ■■        ■■■■■■■■  ■■■■■■■  ■■■■■■")
    print("                                       ■■  ■■        ■■      ■■   ■■   ■■    ■■       ■■    ■■  ■■       ■■   ■■")
    print("                                   ■■■■■   ■■■■■■■  ■■        ■■  ■■    ■■    ■■■■■■  ■■    ■■  ■■■■■■■  ■■    ■■")
    print("")
    print(green + "  ■■■■■■    ■■■■■■  ■■■■■■■■  ■■       ■■")
    print(" ■■        ■■          ■■      ■■     ■■")
    print("■■        ■■           ■■       ■■   ■■")
    print(" ■■        ■■          ■■        ■■ ■■")
    print("  ■■■■■■    ■■■■■■     ■■         ■■■" + white)
    print("\n-------------------------------------------------------------------------------------------------------------------------------")
    print(green + "Maker : Sigma")
    print("Github : https://github.com/ermwhatesigma")
    print(yellow + "This is the cctv searcher. It tries to find cctv from this list under")


def main_list():
    print('\n')
    print(green + f"    {'1) United States':35}47) Singapore")
    print(f"    {'2) Japan':35}48) Iceland")
    print(f"    {'3) Italy':35}49) Malaysia")
    print(f"    {'4) Korea':35}50) Colombia")
    print(f"    {'5) France':35}51) Tunisia")
    print(f"    {'6) Germany':35}52) Estonia")
    print(f"    {'7) Taiwan':35}53) Dominican Republic")
    print()
    print(cyan + f"    {'8) Russian Federation':35}54) Slovenia")
    print(f"    {'9) United Kingdom':35}55) Ecuador")
    print(f"    {'10) Netherlands':35}56) Lithuania")
    print(f"    {'11) Czech Republic':35}57) Palestinian")
    print(f"    {'12) Turkey':35}58) New Zealand")
    print(f"    {'13) Austria':35}59) Bangladesh")
    print(f"    {'14) Switzerland':35}60) Panama")
    print()
    print(red + f"    {'15) Spain':35}61) Moldova")
    print(f"    {'16) Canada':35}62) Nicaragua")
    print(f"    {'17) Sweden':35}63) Malta")
    print(f"    {'18) Israel':35}64) Trinidad And Tobago")
    print(f"    {'19) Iran':35}65) Saudi Arabia")
    print(f"    {'20) Poland':35}66) Croatia")
    print(f"    {'21) India':35}67) Cyprus")
    print(f"    {'22) Norway':35}69) United Arab Emirates")
    print(f"    {'23) Norway':35}70) Kazakhstan")
    print(f"    {'25) Belgium':35}71) Kuwait")
    print(f"    {'26) Brazil':35}72) Venezuela")
    print(f"    {'27) Bulgaria':35}73) Georgia")
    print(f"    {'28) Indonesia':35}74) Montenegro")
    print()
    print(yellow + f"    {'29) Denmark':35}75) El Salvador")
    print(f"    {'30) Argentina':35}76) Luxembourg")
    print(f"    {'31) Mexico':35}77) Curaçao")
    print(f"    {'32) Finland':35}78) Puerto Rico")
    print(f"    {'33) China':35}79) Costa Rica")
    print(f"    {'34) South Africa':35}80) Belarus")
    print(f"    {'35) South Africa':35}81) Albania")
    print(f"    {'36) Slovakia':35}82) Liechtenstein")
    print(f"    {'37) Hungary':35}83) Bosnia And Herzegovina")
    print()
    print(purple + f"    {'38) Ireland':35}84) Paraguay")
    print(f"    {'39) Egypt':35}85) Philippines")
    print(f"    {'40) Thailand':35}86) Faroe Islands")
    print(f"    {'41) Ukraine':35}87) Guatemala")
    print(f"    {'42) Serbia':35}88) Nepal")
    print(f"    {'43) Hong Kong':35}89) Peru")
    print(f"    {'44) Greece':35}90) Uruguay")
    print(f"    {'45) Portugal':35}91) Extra")
    print(f"    {'46) Latvia':35}92) Andorra")
    print()
    print(green + f"    {'93) Antigua And Barbuda':35}")
    print(f"    {'94) Armenia':35}120) Cayman Islands")
    print(f"    {'95) Angola':35}121) Laos")
    print(f"    {'96) Australia':35}122) Lebanon")
    print(f"    {'97) Aruba':35}123) Sri Lanka")
    print(f"    {'98) Azerbaijan':35}124) Morocco")
    print(f"    {'99) Barbados':35}125) Madagascar")
    print()
    print(blue + f"    {'100) Bonaire':35}126) North Macedonia")
    print(f"    {'101) Bahamas':35}127) Mongolia")
    print(f"    {'102) Botswana':35}128) Macau")
    print(f"    {'103) Congo':35}129) Martinique")
    print(f"    {'104) Ivory Coast':35}130) Mauritius")
    print(f"    {'105) Algeria':35}131) Namibia")
    print(f"    {'106) Fiji':35}132) New Caledonia")
    print()
    print(purple + f"    {'107) Gabon':35}133) Nigeria")
    print(f"    {'108) Guernsey':35}134) Qatar")
    print(f"    {'109) Greenland':35}135) Réunion")
    print(f"    {'110) Guadeloupe':35}136) Sudan")
    print(f"    {'111) Guam':35}137) Senegal")
    print(f"    {'112) Guyana':35}138) Suriname")
    print(f"    {'113) Honduras':35}139) São Tomé And Príncipe")
    print()
    print(red + f"    {'114) Jersey':35}140) Syria")
    print(f"    {'115) Jamaica':35}141) Tanzania")
    print(f"    {'116) Jordan':35}142) Uganda")
    print(f"    {'117) Kenya':35}143) Uzbekistan")
    print(f"    {'118) Cambodia':35}144) Saint Vincent")
    print(f"    {'119) Saint Kitts':35}145) Benin")

    countries = ["US", "JP", "IT", "KR", "FR", "DE", "TW", "RU", "GB", "NL", "CZ", "TR", "AT", "CH", "ES", "CA", "SE", "IL", "PL", "IR", "NO", "RO", "IN", "VN", "BE", "BR", "BG", "ID", "DK", "AR", "MX", "FI", "CN", "CL", "ZA", "SK", "HU", "IE", "EG", "TH", "UA", "RS", "HK", "GR", "PT", "LV", "SG", "IS", "MY", "CO", "TN", "EE", "DO", "SI", "EC", "LT", "PS", "NZ", "BD", "PA", "MD", "NI", "MT", "TT", "SA", "HR", "CY", "PK", "AE", "KZ", "KW", "VE", "GE", "ME", "SV", "LU", "CW", "PR", "CR", "BY", "AL", "LI", "BA", "PY", "PH", "FO", "GT", "NP", "PE", "UY", "-" , "AD", "AG", "AM", "AO", "AU", "AW", "AZ", "BB", "BQ", "BS", "BW", "CG", "CI", "DZ", "FJ", "GA", "GG", "GL", "GP", "GU", "GY", "HN", "JE", "JM", "JO", "KE", "KH", "KN", "KY", "LA", "LB", "LK", "MA", "MG", "MK", "MN", "MO", "MQ", "MU", "NA", "NC", "NG", "QA", "RE", "SD", "SN", "SR", "ST", "SY", "TZ", "UG", "UZ", "VC","BJ", ]
    headers = {"User-Agent": "Mozilla/5.0 (X11; Linux i686; rv:68.0) Gecko/20100101 Firefox/68.0"}
    num = int(input("\nOPTIONS : "))
    print('')

    if num not in range(1, 145+1):
        raise IndexError

    country = countries[num-1]
    res = requests.get(f"http://www.insecam.org/en/bycountry/{country}", headers=headers)
    last_page = re.findall(r'pagenavigator\("\?page=", (\d+)', res.text)[0]

    for page in range(int(last_page)):
        res = requests.get(f"http://www.insecam.org/en/bycountry/{country}/?page={page}", headers=headers)
        find_ip = re.findall(r"http://\d+.\d+.\d+.\d+:\d+", res.text)
        for ip in find_ip:
            print("\033[1;31m", ip)


while True:
    start()
    main_list()

    print("\033[1;37m")
    print('You can only close the script with ctrl + c')
    input(red + 'Press any key to reset...' + white)