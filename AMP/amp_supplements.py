import pywikibot
from pywikibot import Site
import re

# list of url patterns to skip
skip_url_patterns = [
    rf"^https?://(?:[\w.-]+\.)?{re.escape(domain)}(/.*)?$"
    for domain in [
        "wikipedia.org", 
        "amp.dev", "amp.org.br", "amp.pt",
        "larepublica-pe.cdn.ampproject.org",
        "acacamps.org", "asburyamp.org", "ampcapital.com"
        "angelscamp.gov", "amprofon.com", "amprofon.com.mx",
        "archive.is", "archive.ph", "archive.today",
        "astronomycamp.org", "astrocamp.org", "australianstamp.com",
        "bandcamp.com", "bamp.fr", "barrysbootcamp.com",
        "bengalscamp.com", "biancabeauchamp.com", "bitstamp.net",
        "boamp.fr", "breckelenkamp.nl", "bridgechamp.com",
        "caamp.org", "camptocamp.com", 
        "camp.pt.vu", "camp.tx", "camp.ucss.edu.pe",
        "camptocamp.org", "cclamp.radioandrecords.com", "chaclascamp.com",
        "champ.org.uk", "championscamp.pl", "danbeard.org",
        "datacamp.com", "debattencamp.spd.de", "duchamp.org",
        "dwebcamp.org", "eastercamp.org", "econtents.bc.unicamp.br",
        "edencamp.co.uk", "elpopular-pe.cdn.ampproject.org", "emmelkamp.de",
        "encamp.ad", "firetechcamp.com", "folkets-kamp.org",
        "freecodecamp.com", "futsalcamp.cz", "garagedoorchamp.com",
        "genoasamp.com", "ghostarchive.org", "grandchamp.fr",
        "hey-alex.com", "horschamp.qc.ca", "ilonahaberkamp.com",
        "koolskamp.be", "lastampa.it", "longlakecamp.com",
        "marinersbasecamp.com", "memocamp.com", "middlewoodcamp.org.uk",
        "monroemandolincamp.com", "msn.com", "nsobegamecamp.com",
        "oamp.fr", "oercamp.de", "onlamp.com",
        "onecamp.com.au", "oostkamp.be", "paysdeguingamp.com",
        "pincamp.de", "radio.com", "rockcamp.com",
        "ronchamp.fr", "saejongcamp.org", "sampi.net.br",
        "scoutcamp.org", "seecamp.com", "seedcamp.com",
        "skepticamp.org", "slayalive.com", "stamp.kiev.ua",
        "stlcamp.org", "suhrkamp.de", "swamp.lt",
        "tagesschau.de", "tifosamp.com", "tomkatcamp.ca",
        "ucr.edu", "unicamp.br", "unicamp.org",
        "vzwamp.com", "ville-guingamp.fr", "waltercamp.org",
        "wardsauto.com", "webamp.org", "webcitation.org",
        "winamp.com",
        "yardbarker.com", "zoutkamp.net", "delcamp.cat",
        "anthonyjcamp.com", "lamaimuaythaicamp.com", "wisebigmancamp.com",
        "pricecamp.org", "revolutioncamp.it", "sturdycamp.com",
        "larkcamp.com", "greencamp.com", "shumen-camp.info",
        "camp.lv", "railcamp.com", "thevalleycamp.com",
        "odette-camp.fr", "yurucamp.jp", "stlcamp.org",
        "uni-koeln.de", "altcamp.info", "eki-stamp.com",
        "lamp.ac.uk", "longcamp.com", "roaringcamp.com",
        "koreanculturecamp.net", "subwaystamp.com", "lankastamp.com",
        "ramp.com", "hipstamp.com", "rosekamp.dk",
        "numistamp.com", "vamp.org", "idolchamp.com",
        "mysticstamp.com", "pleinchamp.com", "sanskrit-lamp.org",
        "ghanamps.com", "tradjazzcamp.com",
    ]
]
           

# http://blog.yag-hamacamp.main.jp/?eid=341 
exact_skip_urls = [
    # exact matches for the URLs to skip (with or without www)
    r"^https?://(?:www\.)?wdwinfo\.com/news-stories/amp-suit-decorated-with-holiday-theming-at-disneys-animal-kingdom/$",
    r"^https?://(?:www\.)?swissinfo\.ch/spa/las--fake-news--amplifican-el-miedo-y-la-confusi%C3%B3n-en-hong-kong/45380788$",
    r"^https?://(?:www\.)?padua-access\.stuttgart\.de/Access\.xhtml\?.*$",
    r"^https?://(?:www\.)?adelaidenow\.com\.au/business/sa-business-journal/didier-elzingas-billion-dollar-tech-company-culture-amp-wants-to-make-work-better-for-all-of-us/news-story/265491a4c82d9aa9e4c5215b30320e13$",
]


# Set of words to check for skipping
skippable_words = {
    "amplio", "ampel", "ampersand",
    "ampproject", "amp-project", "webarchive",
    "amphan", "amphibian", "heitkamp",
}

archive_url_patterns = [
    # archive-url variations
    # covers de, en, es, fr, it, pl, pt, ar, nl, fi, eu, ast,
    r'(\|\s*(archive-url|مسار أرشيف|مسار الأرشيف|archiveurl|urlarchivo|archiwum|archiv-url|urlarchivio|urlarquivo|arquivourl|arquivo-url|archiefurl|valinnainen|artxibo-url|urlarchivu)\s*=\s*)(https?://[^\s|]+)',

    # Match {{Webarchive | url= ... }} templates with variations
    r'(\{\{\s*Webarchive\s*\|\s*url\s*=\s*)(https?://[^\s|]+)',
]

def get_wiki_sites():
    return {f"{code}wiki": Site(code, "wikipedia") for code in [
    "en", "de", "es", "fr", "it", "pl", "pt",
    "ab", "ace", "ady", "af", "am", "an", "ang", "ar", "arc", "arz", "as", "ast", "atj", "av", "avk", "awa", "ay", "az", "azb",
    "ca", "ce", "eu", "fa", "fi", "hu", "nl", "tt", "war", "zh-min-nan",
    "ceb", "hi",
]}

# temporaily removed: "ami", "id", ms, sv,  = not clear about global bot.

# dictionary of edit summaries for each wikipedia language
default_summary = "removed AMP tracking from URLs ([[:en:User:KiranBOT/AMP|details]]) ([[:en:User talk:Usernamekiran|report error]]) v2.2.5r"

edit_summaries = {
    "en": default_summary,
    "de": "Bot: AMP-Tracking aus URLs entfernt ([[:en:User:KiranBOT/AMP|details]]) ([[User talk:Usernamekiran|Fehler melden]]) v2.2.5r",
    "es": "eliminación del seguimiento AMP en URLs ([[:en:User:KiranBOT/AMP|detalles]]) ([[User talk:Usernamekiran|reportar error]]) v2.2.5r",
    "fr": "suppression du suivi AMP dans les URLs ([[:en:User:KiranBOT/AMP|détails]]) ([[User talk:Usernamekiran|signaler une erreur]]) v2.2.5r",
    "it": "rimosso il tracciamento AMP dagli URL ([[:en:User:KiranBOT/AMP|dettagli]]) ([[Discussioni utente:Usernamekiran|segnala errore]]) v2.2.5r",
    "pl": "Usunięto śledzenie AMP z adresów URL ([[:en:User:KiranBOT/AMP|szczegóły]]) ([[User talk:Usernamekiran|zgłoś błąd]]) v2.2.5r",
    "pt": "BOT: remoção do rastreamento AMP das URLs ([[:en:User:KiranBOT/AMP|detalhes]]) ([[User talk:Usernamekiran|reportar erro]]) v2.2.5r",
    "ab": "Ианыхуп AMP ашьҭаԥшра URL аҟынтәи ([[:en:User:KiranBOT/AMP|ахәҭаҷқәа]]) ([[User talk:Usernamekiran|aгха аҳасабырба]]). v2.2.5r",
    "ace": "Peulacak AMP ka geubôh nibak URL ([[:en:User:KiranBOT/AMP|detil]]) ([[User talk:Usernamekiran|lapor kasalahan]]) v2.2.5r",
    "ady": default_summary,
    "af": "het AMP-opsporing van URL'e verwyder ([[:en:User:KiranBOT/AMP|besonderhede]]) ([[User talk:Usernamekiran|rapporteer fout]]) v2.2.5r",
    "am": "የAMP ክትትልን ከዩአርኤሎች ተወግዷል ([[:en:User:KiranBOT/AMP|ዝርዝሮች]]) ([[User talk:Usernamekiran|ስህተት ሪፖርት አድርግ]]) v2.2.5r",
    "ami": default_summary,
    "an": default_summary,
    "ang": "afscerod AMP-tracking from URLs ([[:en:User:KiranBOT/AMP|dǣl]]) ([[User talk:Usernamekiran|forwyrd-an eor]]) v2.2.5r",
    "ar": "إزالة تتبع AMP من عناوين URL ([[:en:User:KiranBOT/AMP|التفاصيل]]) ([[نقاش المستخدم:Usernamekiran|خطأ في الإبلاغ]]) v2.2.5r",
    "arc": "AMP-Tracking ܡܢ URLs ܡܢܝܬ ([[:en:User:KiranBOT/AMP|ܐܢܬܐ]]) ([[User talk:Usernamekiran|ܐܙܠ ܕܠܝܠ]]) v2.2.5r",
    "arz": "AMP-Tracking mn URLs itfrrdu ([[:en:User:KiranBOT/AMP|tafaṣṣīl]]) ([[User talk:Usernamekiran|tārīkh ϻałʿūṭ]]) v2.2.5r",
    "as": "AMP-Tracking URLs ৰ পৰা আঁতৰোৱা হৈছে ([[:en:User:KiranBOT/AMP|বিশদ]]) ([[User talk:Usernamekiran|ভুল প'ৰিবেশ]]) v2.2.5r",
    "ast": "AMP-Tracking fuera de URLs retirado ([[:en:User:KiranBOT/AMP|detalles]]) ([[User talk:Usernamekiran|denunciar error]]) v2.2.5r",
    "atj": "AMP-Tracking URL hite eskeri ([[:en:User:KiranBOT/AMP|detaylar]]) ([[User talk:Usernamekiran|hata raporlama]]) v2.2.5r",
    "av": "AMP-Tracking URL-lär hanalhiy ([[:en:User:KiranBOT/AMP|tağlar]]) ([[User talk:Usernamekiran|hataları raporlama]]) v2.2.5r",
    "avk": "AMP-Tracking URLs dan girlemişti ([[:en:User:KiranBOT/AMP|detallar]]) ([[User talk:Usernamekiran|hatalar bildirin]]) v2.2.5r",
    "awa": "AMP-Tracking URLs se hatawā chiṭi ([[:en:User:KiranBOT/AMP|details]]) ([[User talk:Usernamekiran|bug report]]) v2.2.5r",
    "ay": "AMP-Tracking URLs qhanqʼa ([[:en:User:KiranBOT/AMP|detalles]]) ([[User talk:Usernamekiran|error reporte]]) v2.2.5r",
    "az": "AMP-Tracking URL-lərdən çıxarıldı ([[:en:User:KiranBOT/AMP|detallar]]) ([[User talk:Usernamekiran|xətanı bildirmək]]) v2.2.5r",
    "azb": "AMP-Tracking URL-lərdən qaldırıldı ([[:en:User:KiranBOT/AMP|detallar]]) ([[User talk:Usernamekiran|səhv bildirmək]]) v2.2.5r",
    "ca": "Eliminació del seguiment AMP de les URL ([[:en:User:KiranBOT/AMP|detalls]]) ([[User talk:Usernamekiran|informeu d'errors]]) v2.2.5r",
    "ce": default_summary,
    "eu": "AMP jarraipena URLetatik kendu da ([[:en:User:KiranBOT/AMP|xehetasunak]]) ([[User talk:Usernamekiran|errorea jakinarazi]]) v2.2.5r",
    "fa": "حذف ردیابی AMP از URLها ([[:en:User:KiranBOT/AMP|جزئیات]]) ([[User talk:Usernamekiran|گزارش خطا]]) v2.2.5r",
    "fi": "AMP-seuranta poistettu URL-osoitteista ([[:en:User:KiranBOT/AMP|yksityiskohdat]]) ([[User talk:Usernamekiran|ilmoita virheestä]]) v2.2.5r",
    "hu": "AMP-követés eltávolítva az URL-ekből ([[:en:User:KiranBOT/AMP|részletek]]) ([[User talk:Usernamekiran|hibabejelentés]]) v2.2.5r",
    "id": "Pelacakan AMP dihapus dari URL ([[:en:User:KiranBOT/AMP|rincian]]) ([[User talk:Usernamekiran|laporkan kesalahan]]) v2.2.5r",
    "ms": "Penjejakan AMP telah dialih keluar dari URL ([[:en:User:KiranBOT/AMP|butiran]]) ([[User talk:Usernamekiran|laporkan ralat]]) v2.2.5r",
    "sv": "AMP-spårning borttagen från URL:er ([[:en:User:KiranBOT/AMP|detaljer]]) ([[User talk:Usernamekiran|rapportera fel]]) v2.2.5r",
    "tl": "inalis ang pagsubaybay sa AMP sa mga URL ([[:en:User:KiranBOT/AMP|mga detalye]]) ([[User talk:Usernamekiran|mag-ulat ng error]]) v2.2.5r",
    "tt": default_summary,
    "war": default_summary,
    "zh-min-nan": default_summary,
    "nl": "AMP-tracking uit URL's verwijderd ([[:en:User:KiranBOT/AMP|details]]) ([[User talk:Usernamekiran|fout melden]]) v2.2.5r",
    "ceb": "Gitangtang ang AMP tracking gikan sa mga URL ([[:en:User:KiranBOT/AMP|detalye]]) ([[User talk:Usernamekiran|reporta ang sayop]]) v2.2.5r",
    "hi": "AMP-Tracking को URLs से हटाया गया ([[:en:User:KiranBOT/AMP|विवरण]]) ([[User talk:Usernamekiran|त्रुटि दर्ज करें]]) v2.2.5r",
}
