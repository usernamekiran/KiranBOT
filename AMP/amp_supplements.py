import pywikibot
from pywikibot import Site
import re

# list of url patterns to skip
skip_url_patterns = [
    rf"^https?://(?:[\w.-]+\.)?{re.escape(domain)}(/.*)?$"
    for domain in [
        "wikipedia.org",
        "books.google.com", "news.google.com",
        "legacy.com",
        "amp.dev", "amp.org.br", "amp.pt",
        "larepublica-pe.cdn.ampproject.org",
        "acacamps.org", "asburyamp.org", "ampcapital.com"
        "angelscamp.gov", "amprofon.com", "amprofon.com.mx",
        "archive.is", "archive.ph", "archive.today",
        "astronomycamp.org", "astrocamp.org", "australianstamp.com", "bandcamp.com", "bamp.fr",
        "barrysbootcamp.com", "bengalscamp.com", "biancabeauchamp.com", "bitstamp.net", "boamp.fr",
        "breckelenkamp.nl", "bridgechamp.com", "caamp.org", "camptocamp.com", "christerhamp.se",
        "camp.pt.vu", "camp.tx", "camp.ucss.edu.pe", "camptocamp.org", "cclamp.radioandrecords.com",
        "chaclascamp.com", "champ.org.uk", "championscamp.pl", "danbeard.org", "datacamp.com",
        "debattencamp.spd.de", "duchamp.org", "dwebcamp.org", "eastercamp.org", "econtents.bc.unicamp.br",
        "edencamp.co.uk", "elpopular-pe.cdn.ampproject.org", "emmelkamp.de", "encamp.ad", "firetechcamp.com",
        "folkets-kamp.org", "freecodecamp.com", "futsalcamp.cz", "garagedoorchamp.com", "genoasamp.com",
        "ghostarchive.org", "grandchamp.fr", "hey-alex.com", "horschamp.qc.ca", "ilonahaberkamp.com",
        "koolskamp.be", "lastampa.it", "longlakecamp.com", "marinersbasecamp.com", "memocamp.com",
        "middlewoodcamp.org.uk", "monroemandolincamp.com", "msn.com", "nsobegamecamp.com", "oamp.fr",
        "oercamp.de", "onlamp.com", "onecamp.com.au", "oostkamp.be", "paysdeguingamp.com",
        "pincamp.de", "radio.com", "rockcamp.com", "ronchamp.fr", "saejongcamp.org",
        "sampi.net.br", "scoutcamp.org", "seecamp.com", "seedcamp.com", "skepticamp.org",
        "slayalive.com", "stamp.kiev.ua", "stlcamp.org", "suhrkamp.de", "swamp.lt",
        "tagesschau.de", "tifosamp.com", "tomkatcamp.ca", "ucr.edu", "unicamp.br",
        "unicamp.org", "vzwamp.com", "ville-guingamp.fr", "waltercamp.org", "wardsauto.com",
        "webamp.org", "webcitation.org", "winamp.com", "wadehamptoncamp.org", "yardbarker.com",
        "zoutkamp.net", "delcamp.cat", "anthonyjcamp.com", "lamaimuaythaicamp.com", "wisebigmancamp.com",
        "pricecamp.org", "revolutioncamp.it", "sturdycamp.com", "larkcamp.com", "greencamp.com",
        "shumen-camp.info",
        "camp.lv", "railcamp.com", "thevalleycamp.com",
        "odette-camp.fr", "yurucamp.jp", "stlcamp.org",
        "uni-koeln.de", "altcamp.info", "eki-stamp.com",
        "lamp.ac.uk", "longcamp.com", "roaringcamp.com",
        "koreanculturecamp.net", "subwaystamp.com", "lankastamp.com",
        "ramp.com", "hipstamp.com", "rosekamp.dk",
        "numistamp.com", "vamp.org", "idolchamp.com",
        "mysticstamp.com", "pleinchamp.com", "sanskrit-lamp.org",
        "ghanamps.com", "tradjazzcamp.com", "mariekenijkamp.com",
        "cybercamp.es", "linecamp.com", "reebokabcdcamp.com",
        "lsamp.neu.edu", "andrew-reynolds-bootcamp.com",
        "rawramp.me", "skycamp.pl", "campaignlive.co.uk",
        "snowcamp.org", "voteforshamp.com", "facamp.com.br",
        "puccamp.br", "policamp.edu.br", "gavinstamp.co.uk",
        "ceciliastamp.com", "agnesstamp.com", "greatswamp.org",
        "supertramp.com", "apramp.org", "portofinoamp.it",
        "marinalystcamp.dk", "vestbirk.dk-camp.dk", "rduchamp.fr",
        "barcamp.org", "thomasroewekamp.de", "handstamp.com",
        "agemcamp.sp.gov.br", "openwebcamp.com", "grovedaycamp.com",
        "artsurfcamp.com", "rccamp.org", "jz-kamp.de",
        "nystamp.org", "aiamp.info", "usana-amp.com",
        "eaguingamp.com", "angelscamp.gov", "anthonycamp.com",
        "academystamp.com", "buddhiststamp.com", "metalcamp.com",
        "gnulamp.com", "mountainstamp.com", "freecodecamp.org",
        "horschamp.org", "bueschelskamp.de", "thorpecamp.org.uk",
        "droverscamp.com.au", "mainefiddlecamp.org", "a-camp.org",
        "greentourismcamp.com", "amp.acdh.oeaw.ac.at", "devbootcamp.com",
        "euro.dayfr.com", "amp.gov.al", "eaguingamp.com",
        "hamiltoncamp.com", "unicamp.academia.edu", "zachwamp.com",
        "maasaicamp.com", "profcamp.tripod.com", "muschamp.org.uk",
        "artistcamp.com", "museumparkharskamp.nl", "maamp.us",
        "pacamp.com", "davidkamp.com", "climbcamp.fr",
        "rentocamp.com", "conventioncamp.de", "chinesestamp.org",
        "laselvadelcamp.org", "bohemiamp.cz", "salsacamp.de",
        "kingswamp.com", "zamp.hr", "themusicswamp.com",
        "cripcamp.com", "caamp.info", "wanhuamp.com",
        "swamp.org", "nyscamp.org", "aberdaroncamp.com",
        "comparecamp.com", "knowyourrightscamp.com", "perlmancamp.org",
        "svjappenkamp.nl", "iamp.org", "swamp.osu.edu",
        "yag-hamacamp.main.jp", "midwestbanjocamp.com", "revolutioncamp.it",
        "wellcamp.com.au", "datamp.org", "balisurfingcamp.com",
        "wwe.com", "swissinfo.ch", "trueofvamp.dreamful.org",
        "spacamp.net", "klimacamp.fridaysforfuture.berlin", "attheamp.com",
        "ramonchamp.fr", "transvisionvamp.com", "eys-workcamp.de",
        "hipcamp.com", "mowjcamp.ws", "kitchenercamp.co.uk",
        "ecocamp.travel", "arthellcoalcamp.com", "longchamp.com",
        "vahrenkamp.org", "fineartscamp.org", "ggslangekamp.de",
        "kgs-meerkamp.de", "gs-amrosenkamp.de", "ggs-blumenkamp.de",
        "grundschule-heidkamp.de", "kgs-eikamp.de", "ggs-alten-kamp.bobi.net",
        "grundschule-kuhlerkamp.de", "gymnasium-rheinkamp.de", "beisenkamp.eu", "schule-am-buschkamp.de", "annehartkamp.de",
        "elettronicafacile.it", "indiewebcamp.com", "rutgermolenkamp.nl", "popsci.com", "isrsummercamp.org", # popsci usually redirects to 404 pages

    ]
]

exact_skip_urls = [
    # exact matches for the URLs to skip (with or without www)
    r"^https?://(?:www\.)?wdwinfo\.com/news-stories/amp-suit-decorated-with-holiday-theming-at-disneys-animal-kingdom/$",
    r"^https?://(?:www\.)?padua-access\.stuttgart\.de/Access\.xhtml\?.*$",
    r"^https?://(?:www\.)?adelaidenow\.com\.au/business/sa-business-journal/didier-elzingas-billion-dollar-tech-company-culture-amp-wants-to-make-work-better-for-all-of-us/news-story/265491a4c82d9aa9e4c5215b30320e13$",
    r"^https?://(?:www\.)?foreign\.go\.tz/resources/view/waziri-mahiga-ampokea-mjumbe-maalum-kutoka-sahrawi$",
    r"^https?://(?:www\.)?foreign\.go\.tz/index\.php/resources/view/waziri-mahiga-ampokea-mjumbe-maalum-kutoka-sahrawi$",

]

# Set of words to check for skipping
skippable_words = {
    "amplio", "ampel", "ampersand",
    "ampproject", "amp-project", "webarchive",
    "amphan", "amphibian", "heitkamp",
    "basecamp", "amphitheater", "obituaries",
}

archive_url_patterns = [
    # archive-url variations
    # covers de, en, es, fr, it, pl, pt, ar, nl, fi, eu, ast,
    r'(\|\s*(archive-url|مسار أرشيف|مسار الأرشيف|archiveurl|urlarchivo|archiwum|archiv-url|urlarchivio|urlarquivo|arquivourl|arquivo-url|archiefurl|valinnainen|artxibo-url|urlarchivu)\s*=\s*)(https?://[^\s|]+)',

    # match {{Webarchive | url= ... }} templates with variations
    #r'(\{\{\s*Webarchive\s*\|\s*url\s*=\s*)(https?://[^\s|]+)', # this is now covered in main script

    # urls that embed another URL after a slash
    r'(https?://[^\s|]*?/https?://[^\s|]+)',
]

def get_single_wiki():
    return {f"{code}wiki": Site(code, "wikipedia") for code in [
    "ta",
]}

def get_small_wikis():
    return {f"{code}wiki": Site(code, "wikipedia") for code in [
    "ady", "arc", "ang", "ab", "ace", "am", "an",
]}

def get_wiki_sites():
    return {f"{code}wiki": Site(code, "wikipedia") for code in [
    "en", "de", "es", "fr", "it", "pl", "pt", "id", "nn", "sl",
    "ab", "ace", "ady", "af", "als", "am", "ami", "ang", "anp", "an", "ar", "arc", "arz", "as", "ast", "atj", "av", "avk", "awa", "ay",
    "ba", "ban", "bar", "bbc", "bcl", "be", "be-tarask", "bg", "bh", "bi", "bjn", "blk", "bm", "bo", "bpy", "br", "bug", "bxr",
    "ca", "cdo", "ce", "ceb", "ch", "chr", "chy", "ckb", "co", "cr", "crh", "cs", "csb", "cu", "cv", "cy", "da", "dag", "dga", "din", "diq", "dsb", "dty", "dz",
    "ee", "el", "eml", "en", "eo", "et", "eu", "ext", "fa", "fat", "ff", "fi", "fj", "fo", "fon", "frp", "frr", "fur",
    "ga", "gag", "gan", "gcr", "gd", "glk", "gn", "gom", "gor", "got", "gpe", "gu", "guc", "gur", "guw", "gv", "ha", "hak", "haw", "he", "hi", "hif", "hr", "hsb", "ht", "hu", "hy", "hyw",
    "ia", "ie", "ig", "ik", "ilo", "inh", "io", "iu", "ja", "jam", "jbo", "jv",
    "ka", "kaa", "kab", "kbd", "kbp", "kcg", "kg", "ki", "kk", "kl", "km", "kn", "ko", "koi", "krc", "ks", "ku", "kv", "kw", "ky",
    "la", "lad", "lb", "lbe", "lez", "lfn", "lg", "li", "lij", "lld", "lmo", "ln", "lo", "lt", "ltg", "lv",
    "mad", "mai", "mdf", "mg", "mhr", "mi", "min", "mk", "ml", "mn", "mni", "mrj", "ms", "mwl", "my", "myv", "mzn",
    "nah", "nap", "ne", "new", "nia", "nl", "no", "nov", "nqo", "nrm", "nso", "nv", "ny", "oc", "olo", "om", "or", "os",
    "pa", "pag", "pam", "pap", "pcd", "pcm", "pdc", "pfl", "pi", "pms", "pnb", "pnt", "ps", "pwn", "qu", "rm", "rmy", "rn", "rue", "ru", "rw",
    "sa", "sah", "sat", "scn", "sc", "sco", "sd", "se", "sg", "sh", "shi", "shn", "si", "simple", "sk", "skr", "sm", "smn", "sn", "so", "sq", "srn", "ss", "st", "stq", "su", "sv", "sw", "szl", "szy",
    "ta", "tay", "tcy", "tet", "te", "tg", "th", "ti", "tk", "tl", "tly", "tn", "to", "tpi", "trv", "ts", "tt", "tum", "tw", "tyv", "ty",
    "udm", "ug", "uz", "vec", "vep", "ve", "vls", "vo", "wa", "war", "wo", "xal", "xh", "xmf", "yi", "yo", "za", "zea", "zgh", "zh", "zu",
]}

# exists, but not available in pywikibot: "ann", "bdr", "bew", "btm", "dtp", "iba", "igl", "kge", "knc", "kus", "mos", "nr", "nup", "rsk", "syl", "tdd", "tig",
# temporarily paused: "bs"
# temporarily halted: tr, az, azb

# dictionary of edit summaries for each wikipedia language
default_summary = "removed AMP tracking from URLs ([[:m:User:KiranBOT/AMP|details]]) ([[User talk:Usernamekiran|report error]]) v2.2.7r"

edit_summaries = {
    "en": default_summary,
    "de": "Bot: AMP-Tracking aus URLs entfernt ([[:m:User:KiranBOT/AMP|details]]) ([[User talk:Usernamekiran|Fehler melden]]) v2.2.7r",
    "es": "eliminación del seguimiento AMP en URLs ([[:m:User:KiranBOT/AMP|detalles]]) ([[User talk:Usernamekiran|reportar error]]) v2.2.7r",
    "fr": "suppression du suivi AMP dans les URLs ([[:m:User:KiranBOT/AMP|détails]]) ([[User talk:Usernamekiran|signaler une erreur]]) v2.2.7r",
    "it": "rimosso il tracciamento AMP dagli URL ([[:m:User:KiranBOT/AMP|dettagli]]) ([[Discussioni utente:Usernamekiran|segnala errore]]) v2.2.7r",
    "pl": "Usunięto śledzenie AMP z adresów URL ([[:m:User:KiranBOT/AMP|szczegóły]]) ([[User talk:Usernamekiran|zgłoś błąd]]) v2.2.7r",
    "pt": "BOT: remoção do rastreamento AMP das URLs ([[:m:User:KiranBOT/AMP|detalhes]]) ([[User talk:Usernamekiran|reportar erro]]) v2.2.7r",
    "ab": "Ианыхуп AMP ашьҭаԥшра URL аҟынтәи ([[:m:User:KiranBOT/AMP|ахәҭаҷқәа]]) ([[User talk:Usernamekiran|aгха аҳасабырба]]). v2.2.7r",
    "ace": "Peulacak AMP ka geubôh nibak URL ([[:m:User:KiranBOT/AMP|detil]]) ([[User talk:Usernamekiran|lapor kasalahan]]) v2.2.7r",
    "ady": default_summary,
    "af": "het AMP-opsporing van URL'e verwyder ([[:m:User:KiranBOT/AMP|besonderhede]]) ([[User talk:Usernamekiran|rapporteer fout]]) v2.2.7r",
    "am": "የAMP ክትትልን ከዩአርኤሎች ተወግዷል ([[:m:User:KiranBOT/AMP|ዝርዝሮች]]) ([[User talk:Usernamekiran|ስህተት ሪፖርት አድርግ]]) v2.2.7r",
    "ami": default_summary,
    "an": default_summary,
    "ang": "afscerod AMP-tracking from URLs ([[:m:User:KiranBOT/AMP|dǣl]]) ([[User talk:Usernamekiran|forwyrd-an eor]]) v2.2.7r",
    "ar": "إزالة تتبع AMP من عناوين URL ([[:m:User:KiranBOT/AMP|التفاصيل]]) ([[نقاش المستخدم:Usernamekiran|خطأ في الإبلاغ]]) v2.2.7r",
    "arc": "AMP-Tracking ܡܢ URLs ܡܢܝܬ ([[:m:User:KiranBOT/AMP|ܐܢܬܐ]]) ([[User talk:Usernamekiran|ܐܙܠ ܕܠܝܠ]]) v2.2.7r",
    "arz": "AMP-Tracking mn URLs itfrrdu ([[:m:User:KiranBOT/AMP|tafaṣṣīl]]) ([[User talk:Usernamekiran|tārīkh ϻałʿūṭ]]) v2.2.7r",
    "as": "AMP-Tracking URLs ৰ পৰা আঁতৰোৱা হৈছে ([[:m:User:KiranBOT/AMP|বিশদ]]) ([[User talk:Usernamekiran|ভুল প'ৰিবেশ]]) v2.2.7r",
    "ast": default_summary,
    "atj": "AMP-Tracking URL hite eskeri ([[:m:User:KiranBOT/AMP|detaylar]]) ([[User talk:Usernamekiran|hata raporlama]]) v2.2.7r",
    "av": "AMP-Tracking URL-lär hanalhiy ([[:m:User:KiranBOT/AMP|tağlar]]) ([[User talk:Usernamekiran|hataları raporlama]]) v2.2.7r",
    "avk": "AMP-Tracking URLs dan girlemişti ([[:m:User:KiranBOT/AMP|detallar]]) ([[User talk:Usernamekiran|hatalar bildirin]]) v2.2.7r",
    "awa": "AMP-Tracking URLs se hatawā chiṭi ([[:m:User:KiranBOT/AMP|details]]) ([[User talk:Usernamekiran|bug report]]) v2.2.7r",
    "ay": "AMP-Tracking URLs qhanqʼa ([[:m:User:KiranBOT/AMP|detalles]]) ([[User talk:Usernamekiran|error reporte]]) v2.2.7r",
    "az": "AMP-Tracking URL-lərdən çıxarıldı ([[:m:User:KiranBOT/AMP|detallar]]) ([[User talk:Usernamekiran|xətanı bildirmək]]) v2.2.7r",
    "azb": "AMP-Tracking URL-lərdən qaldırıldı ([[:m:User:KiranBOT/AMP|detallar]]) ([[User talk:Usernamekiran|səhv bildirmək]]) v2.2.7r",
    "ba": "URL-адрестарҙан AMP күҙәтеүен юйҙыҡ ([[:m:User:KiranBOT/AMP|тулыраҡ мәғлүмәт]]) ([[User talk:Usernamekiran|хата тураһында хәбәр]]) v2.2.7r",
    "be": "выдалена адсочванне AMP з URL-адрасоў ([[:m:User:KiranBOT/AMP|падрабязнасці]]) ([[User talk:Usernamekiran|паведаміць пра памылку]]) v2.2.7r",
    "be-tarask": "выдалена адсочванне AMP з URL-адрасоў ([[:m:User:KiranBOT/AMP|падрабязнасці]]) ([[User talk:Usernamekiran|паведаміць пра памылку]]) v2.2.7r",
    "bg": "премахнато е AMP проследяване от URL адреси ([[:m:User:KiranBOT/AMP|подробности]]) ([[User talk:Usernamekiran|докладвай грешка]]) v2.2.7r",
    "br": "tennet eo bet an heuliañ AMP diouzh an URLoù ([[:m:User:KiranBOT/AMP|munudoù]]) ([[User talk:Usernamekiran|kemenn ur fazi]]) v2.2.7r",
    "bs": "uklonjeno AMP praćenje iz URL-ova ([[:m:User:KiranBOT/AMP|detalji]]) ([[User talk:Usernamekiran|prijavi grešku]]) v2.2.7r",
    "ca": "Eliminació del seguiment AMP de les URL ([[:m:User:KiranBOT/AMP|detalls]]) ([[User talk:Usernamekiran|informeu d'errors]]) v2.2.7r",
    "ce": default_summary,
    "ceb": "gitangtang ang pagsubay sa AMP gikan sa mga URL ([[:m:User:KiranBOT/AMP|mga detalye]]) ([[User talk:Usernamekiran|pagtaho ug sayop]]) v2.2.7r",
    "ckb": "شوێنپێهەڵگرتنی AMP لە URLەکان لابرد ([[:m:User:KiranBOT/AMP|ووردەکاریەکان]]) ([[User talk:Usernamekiran|هەڵەیەک ڕاپۆرت بکە]]) v2.2.7r",
    "cs": "odstraněno sledování AMP z URL adres ([[:m:User:KiranBOT/AMP|podrobnosti]]) ([[User talk:Usernamekiran|nahlásit chybu]]) v2.2.7r",
    "cv": "URL-сенчен AMP сӑнаса тӑрассине кӑларса пӑрахнӑ ([[:m:User:KiranBOT/AMP|даннӑйсем]]) ([[User talk:Usernamekiran|йӑнӑш ҫинчен пӗлтер]]) v2.2.7r",
    "cy": "wedi tynnu olrhain AMP o URLau ([[:m:User:KiranBOT/AMP|manylion]]) ([[User talk:Usernamekiran|adrodd am wall]]) v2.2.7r",
    "da": "fjernede AMP-sporing fra URL'er ([[:m:User:KiranBOT/AMP|detaljer]]) ([[User talk:Usernamekiran|rapporter en fejl]]) v2.2.7r",
    "el": "κατάργησε την παρακολούθηση AMP από τις διευθύνσεις URL ([[:m:User:KiranBOT/AMP|καθέκαστα]]) ([[User talk:Usernamekiran|αναφορά σφάλματος]]) v2.2.7r",
    "eo": "forigis AMP-spuradon de URL-oj  ([[:m:User:KiranBOT/AMP|detaloj]]) ([[User talk:Usernamekiran|raporti eraron]]) v2.2.7r",
    "et": "eemaldas URL-idelt AMP jälgimise  ([[:m:User:KiranBOT/AMP|detailid]]) ([[User talk:Usernamekiran|teata veast]]) v2.2.7r",
    "eu": "AMP jarraipena URLetatik kendu da ([[:m:User:KiranBOT/AMP|xehetasunak]]) ([[User talk:Usernamekiran|errorea jakinarazi]]) v2.2.7r",
    "fa": "حذف ردیابی AMP از URLها ([[:m:User:KiranBOT/AMP|جزئیات]]) ([[User talk:Usernamekiran|گزارش خطا]]) v2.2.7r",
    "fi": "AMP-seuranta poistettu URL-osoitteista ([[:m:User:KiranBOT/AMP|lisätietoja]]) ([[User talk:Usernamekiran|ilmoita virheestä]]) v2.2.7r",
    "ga": "baineadh rianú AMP de URLanna ([[:m:User:KiranBOT/AMP|sonraí]]) ([[User talk:Usernamekiran|tuairiscigh earráid]]) v2.2.7r",
    "glk": default_summary,
    "ha": "cire bin AMP daga URLs ([[:m:User:KiranBOT/AMP|cikakkun bayanai]]) ([[User talk:Usernamekiran|rahoton kuskure]]) v2.2.7r",
    "he": "הסרת מעקב AMP מכתובות URL ([[:m:User:KiranBOT/AMP|פרטים]]) ([[User talk:Usernamekiran|דווח על שגיאה]]) v2.2.7r",
    "hi": "AMP-Tracking को URLs से हटाया ([[:m:User:KiranBOT/AMP|विवरण]]) ([[User talk:Usernamekiran|त्रुटि दर्ज करें]]) v2.2.7r",
    "hr": "uklonjeno je AMP praćenje iz URL-ova ([[:m:User:KiranBOT/AMP|detalji]]) ([[User talk:Usernamekiran|prijavi grešku]]) v2.2.7r",
    "hu": "AMP-követés eltávolítva az URL-ekből ([[:m:User:KiranBOT/AMP|részletek]]) ([[User talk:Usernamekiran|hibabejelentés]]) v2.2.7r",
    "hy": "հեռացվել է AMP հետևումը URL-ներից ([[:m:User:KiranBOT/AMP|մանրամասներf]]) ([[User talk:Usernamekiran|հաղորդել սխալի մասին]]) v2.2.7r",
    "ht": "retire swivi AMP nan URL yo ([[:m:User:KiranBOT/AMP|detay]]) ([[User talk:Usernamekiran|rapòte yon erè]]) v2.2.7r",
    "id": "Pelacakan AMP dihapus dari URL ([[:m:User:KiranBOT/AMP|rincian]]) ([[User talk:Usernamekiran|laporkan kesalahan]]) v2.2.7r",
    "io": default_summary,
    "ja": "URLからアプリトラッキングを削除 ([[:m:User:KiranBOT/AMP|詳細]]) ([[User talk:Usernamekiran|エラーを報告]]) v2.2.7r",
    "jv": "mbusak pelacakan AMP saka URL ([[:m:User:KiranBOT/AMP|rincian]]) ([[User talk:Usernamekiran|laporan kesalahan]]) v2.2.7r",
    "ka": "URL-ებიდან AMP თვალთვალი წაიშალა ([[:m:User:KiranBOT/AMP|დეტალები]]) ([[User talk:Usernamekiran|შეცდომის შესახებ შეტყობინება]]) v2.2.7r",
    "ko": "URL에서 AMP 추적을 제거했습니다 ([[:m:User:KiranBOT/AMP|세부]]) ([[User talk:Usernamekiran|오류 보고]]) v2.2.7r",
    "ku": "şopandina AMP ji URLan hate rakirin ([[:m:User:KiranBOT/AMP|hûrgulî]]) ([[User talk:Usernamekiran|çewtiyek rapor bike]]) v2.2.7r",
    "ky": "URL'дерден AMP көз салуу алынып салынды ([[:m:User:KiranBOT/AMP|майда-чүйдөсүнө чейин]]) ([[User talk:Usernamekiran|ката жөнүндө кабарлоо]]) v2.2.7r",
    "la": "vestigationem AMP ex URL remotam ([[:m:User:KiranBOT/AMP|singularia]]) ([[User talk:Usernamekiran|errorem nuntia]]) v2.2.7r",
    "lb": "AMP-Tracking vun URLen ewechgeholl ([[:m:User:KiranBOT/AMP|detailer]]) ([[User talk:Usernamekiran|feeler mellen]]) v2.2.7r",
    "lld": default_summary,
    "lmo": "eliminà el tracciament AMP di URL ([[:m:User:KiranBOT/AMP|detali]]) ([[User talk:Usernamekiran|segnalà un errur]]) v2.2.7r",
    "lt": "pašalintas AMP stebėjimas iš URL ([[:m:User:KiranBOT/AMP|detalės]]) ([[User talk:Usernamekiran|pranešti apie klaidą]]) v2.2.7r",
    "lv": "noņemta AMP izsekošana no URL ([[:m:User:KiranBOT/AMP|sīkāka informācija]]) ([[User talk:Usernamekiran|ziņot par kļūdu]]) v2.2.7r",
    "mg": "nesorina ny fanaraha-maso AMP tamin'ny URL ([[:m:User:KiranBOT/AMP|tsipiriany]]) ([[User talk:Usernamekiran|mitatitra lesoka]]) v2.2.7r",
    "min": "dihapuih palacakan AMP dari URL ([[:m:User:KiranBOT/AMP|detail]]) ([[User talk:Usernamekiran|malaporkan kasalahan]]) v2.2.7r",
    "ml": "URL-കളിൽ നിന്ന് AMP ട്രാക്കിംഗ് നീക്കം ചെയ്തു  ([[:m:User:KiranBOT/AMP|വിശദാംശങ്ങൾ]]) ([[User talk:Usernamekiran|പിശക് റിപ്പോർട്ട് ചെയ്യുക]]) v2.2.7r",
    "ms": "Penjejakan AMP telah dialih keluar dari URL ([[:m:User:KiranBOT/AMP|butiran]]) ([[User talk:Usernamekiran|laporkan ralat]]) v2.2.7r",
    "my": "AMP ခြေရာခံခြင်းကို URL မှ ဖယ်ရှားခဲ့သည်။ ([[:m:User:KiranBOT/AMP|အသေးစိတ်]]) ([[User talk:Usernamekiran|အမှားအယွင်းတစ်ခုကို သတင်းပို့ပါ။]]) v2.2.7r",
    "mzn": default_summary,
    "new": "यूआरएलपाखें एएमपि ट्राकिङ्ग लिकयाबिल ([[:m:User:KiranBOT/AMP|विवरण]]) ([[User talk:Usernamekiran|छगू द्वंगु रिपोर्ट]]) v2.2.7r",
    "nl": "AMP-tracking uit URL's verwijderd ([[:m:User:KiranBOT/AMP|details]]) ([[User talk:Usernamekiran|fout melden]]) v2.2.7r",
    "nn": "fjernet AMP-sporing fra URL-er ([[:m:User:KiranBOT/AMP|detaljer]]) ([[User talk:Usernamekiran|rapporter en feil]]) v2.2.7r",
    "no": "fjernet AMP-sporing fra URL-er ([[:m:User:KiranBOT/AMP|detaljer]]) ([[User talk:Usernamekiran|rapporter en feil]]) v2.2.7r",
    "oc": "suprimit lo seguiment AMP de las URL ([[:m:User:KiranBOT/AMP|detalhs]]) ([[User talk:Usernamekiran|senhalar una error]]) v2.2.7r",
    "pa": "URL ਤੋਂ AMP ਟਰੈਕਿੰਗ ਹਟਾਈ ਗਈ ([[:m:User:KiranBOT/AMP|ਵੇਰਵੇ]]) ([[User talk:Usernamekiran|ਗਲਤੀ ਦੀ ਰਿਪੋਰਟ ਕਰੋ]]) v2.2.7r",
    "pms": "gjavât vie il monitoraç AMP dai URL ([[:m:User:KiranBOT/AMP|detais]]) ([[User talk:Usernamekiran|segnalâ un erôr]]) v2.2.7r",
    "ru": "удалено отслеживание AMP из URL-адресов ([[:m:User:KiranBOT/AMP|подробности]]) ([[User talk:Usernamekiran|сообщить об ошибке]]) v2.2.7r",
    "sh": default_summary,
    "si": "URL වලින් AMP ලුහුබැඳීම ඉවත් කරන ලදී ([[:m:User:KiranBOT/AMP|විස්තර]]) ([[User talk:Usernamekiran|දෝෂයක් වාර්තා කරන්න]]) v2.2.7r",
    "simple": default_summary,
    "sk": "odstránené sledovanie AMP z URL adries ([[:m:User:KiranBOT/AMP|detaily]]) ([[User talk:Usernamekiran|nahlásiť chybu]]) v2.2.7r",
    "sl": "odstranjeno sledenje AMP iz URL-jev ([[:m:User:KiranBOT/AMP|podrobnosti]]) ([[User talk:Usernamekiran|prijavi napako]]) v2.2.7r",
    "sq": "gjurmimi i AMP u hoq nga URL-të ([[:m:User:KiranBOT/AMP|detajet]]) ([[User talk:Usernamekiran|raporto një gabim]]) v2.2.7r",
    "su": "dipiceun tracking AMP tina URL ([[:m:User:KiranBOT/AMP|rinci]]) ([[User talk:Usernamekiran|kasalahan laporan]]) v2.2.7r",
    "sv": "AMP-spårning borttagen från URL:er ([[:m:User:KiranBOT/AMP|detaljer]]) ([[User talk:Usernamekiran|rapportera fel]]) v2.2.7r",
    "sw": "iliondoa ufuatiliaji wa AMP kutoka kwa URL ([[:m:User:KiranBOT/AMP|maelezo]]) ([[User talk:Usernamekiran|ripoti hitilafu]]) v2.2.7r",
    "szl": "usuniynto śledzynie AMP z URL-ōw ([[:m:User:KiranBOT/AMP|detale]]) ([[User talk:Usernamekiran|zgłosić błōnd]]) v2.2.7r",
    "ta": "URL களில் இருந்து AMP கண்காணிப்பை அகற்றியது ([[:m:User:KiranBOT/AMP|விவரங்கள்]]) ([[User talk:Usernamekiran|பிழையைப் புகாரளிக்கவும்]]) v2.2.7r",
    "te": "URL నుండి AMP ట్రాకింగ్ తీసివేయబడింది ([[:m:User:KiranBOT/AMP|వివరాలు]]) ([[User talk:Usernamekiran|లోపాన్ని నివేదించండి]]) v2.2.7r",
    "tg": "пайгирии AMP аз URL хориҷ карда шуд ([[:m:User:KiranBOT/AMP|тафсилот]]) ([[User talk:Usernamekiran|дар бораи хато хабар диҳед]]) v2.2.7r",
    "th": "ลบการติดตาม AMP ออกจาก URL ([[:m:User:KiranBOT/AMP|รายละเอียด]]) ([[User talk:Usernamekiran|รายงานข้อผิดพลาด]]) v2.2.7r",
    "tl": "inalis ang pagsubaybay sa AMP sa mga URL ([[:m:User:KiranBOT/AMP|mga detalye]]) ([[User talk:Usernamekiran|mag-ulat ng error]]) v2.2.7r",
    "tr": "URL'lerden AMP izlemesi kaldırıldı ([[:m:User:KiranBOT/AMP|detaylar]]) ([[User talk:Usernamekiran|hata bildir]]) v2.2.7r",
    "tt": default_summary,
    "uk": "видалено відстеження AMP з URL-адрес ([[:m:User:KiranBOT/AMP|деталі]]) ([[User talk:Usernamekiran|повідомити про помилку]]) v2.2.7r",
    "uz": "URL manzillardan AMP kuzatuvi olib tashlandi ([[:m:User:KiranBOT/AMP|tafsilotlar]]) ([[User talk:Usernamekiran|xato haqida xabar bering]]) v2.2.7r",
    "vec": "cavà el tracciamento AMP dai URL ([[:m:User:KiranBOT/AMP|detaji]]) ([[User talk:Usernamekiran|segnałar un eror]]) v2.2.7r",
    "war": default_summary,
    "zh-min-nan": default_summary,
}
