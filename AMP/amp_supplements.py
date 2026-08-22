import pywikibot
from pywikibot import Site
import re
from urllib.parse import urlparse, urlunparse

def normalise_url(url):
    # normalise a URL by removing redundant slashes in the path

    try:
        parsed_url = urlparse(url)
        # Remove duplicate slashes in the path
        normalised_path = re.sub(r'\/+', '/', parsed_url.path)
        # Rebuild the URL with the normalised path
        normalised_url = urlunparse(parsed_url._replace(path=normalised_path))
        return normalised_url
    except Exception as e:
        print(f"Error normalizing URL {url}: {e}")
        return url  # Return the original URL if normalisation fails

def is_skippable_url(url: str) -> bool:
    if is_exact_skip_url(url):
        return True
    if any(re.match(pattern, url) for pattern in skip_url_patterns):
        return True
    if any(word in url.lower() for word in skippable_words):
        return True
    return False

def is_exact_skip_url(url: str) -> bool:
    return normalise_url(url) in exact_skip_urls_set

# define AMP keywords and path patterns
AMP_KEYWORDS = [
    "/amp", "amp/", ".amp", "amp.", "?amp", "amp?", "=amp", "amp=",
    "&amp", "amp&", "%amp", "amp%", "_amp", "amp_", "-amp", "amp-",
    "/amp-", "-amp/", "amphtml", "_amphtml", "-amphtml", "/amphtml",
    "amphtml/", "?amphtml", "amphtml=", "amphtml?", "amp_version",
    "outputType=amp", "renderMode=amp", "amp_js_v",
]

PATH_PATTERNS = [
    r'/amp/', r'-amp/', r'/amp-', r'-amp', r'/amphtml/', r'-amphtml',
    r'amp_articleshow', r'-amp(\.html|\.php|\.asp|\.htm|_section)?$',
    r'_amp(\.html|\.php)?$', r'amp_articleshow', r'/ampRFA$',
    r'/amp-page/?$', r'\.amp\.html$', r'/amp\.[a-z]+$', r'/amp_js_v[0-9]+',
    r'/ampredir/', r'/amp-view/', r'/amp_embed/',
]

exact_skip_urls_set = {
    normalise_url("https://wdwinfo.com/news-stories/amp-suit-decorated-with-holiday-theming-at-disneys-animal-kingdom/"),
    normalise_url("https://padua-access.stuttgart.de/Access.xhtml"),
    normalise_url("https://adelaidenow.com.au/business/sa-business-journal/didier-elzingas-billion-dollar-tech-company-culture-amp-wants-to-make-work-better-for-all-of-us/news-story/265491a4c82d9aa9e4c5215b30320e13"),
    normalise_url("https://foreign.go.tz/resources/view/waziri-mahiga-ampokea-mjumbe-maalum-kutoka-sahrawi"),
    normalise_url("https://foreign.go.tz/index.php/resources/view/waziri-mahiga-ampokea-mjumbe-maalum-kutoka-sahrawi"),
    normalise_url("https://albertonews.com/principales/ultima-hora-venezuela-amplia-hasta-2050-el-periodo-establecido-para-operaciones-de-empresa-mixta-petrolera-con-chevron-detalles/"),
    normalise_url("https://bitlyanews.com/principales/ultima-hora-venezuela-amplia-hasta-2050-el-periodo-establecido-para-operaciones-de-empresa-mixta-petrolera-con-chevron-detalles/"),
    normalise_url("https://cio.com/article/2992634/google-takes-on-apple-news-facebook-instant-articles-with-amp.html"),
    normalise_url("https://www.elnacional.com/2018/05/fallecio-paciente-amparada-por-medidas-cautelares-cidh_235127/"),
    normalise_url("https://bitlysdowssl-aws.com/2018/05/fallecio-paciente-amparada-por-medidas-cautelares-cidh_235127/"),
    normalise_url("https://www.elnacional.com/2021/11/quien-es-adolfo-superlano-el-dirigente-que-interpuso-el-amparo-que-impide-proclamacion-del-gobernador-de-barinas/"),
    normalise_url("https://bitlysdowssl-aws.com/2021/11/quien-es-adolfo-superlano-el-dirigente-que-interpuso-el-amparo-que-impide-proclamacion-del-gobernador-de-barinas/"),
}

# skip the URLs containing following words anywhere
skippable_words = {
    "amplio", "ampel", "ampersand", "ampproject", "amp-project",
    "webarchive", "amphan", "amphibian", "heitkamp", "basecamp",
    "amphitheater", "obituaries",
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

# list of url patterns to skip
skip_url_patterns = [
    rf"^https?://(?:[\w.-]+\.)?{re.escape(domain)}(/.*)?$"
    for domain in [
        "wikipedia.org",
        "books.google.com", "news.google.com", "maps.google.com",
        "legacy.com",
        "amp.dev", "amp.org.br", "amp.pt",
        "larepublica-pe.cdn.ampproject.org",
        "archive.is", "archive.ph", "archive.today", "archive.org", "campaign-archive.com",
        "amp.gov.al", "agemcamp.sp.gov.br", "angelscamp.gov", "whccamp.hhs.gov", "techcamp.america.gov",
        "climate.nasa.gov",
        "acacamps.org", "asburyamp.org", "ampcapital.com", "astronomycamp.org", "astrocamp.org",
        "australianstamp.com", "bandcamp.com", "bamp.fr", "hamiltoncamp.com", "unicamp.academia.edu",
        "barrysbootcamp.com", "bengalscamp.com", "biancabeauchamp.com", "bitstamp.net", "boamp.fr",
        "breckelenkamp.nl", "barcamp.com.ar",
        "bridgechamp.com", "caamp.org", "camptocamp.com", "christerhamp.se",
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
        "slayalive.com", "stamp.kiev.ua", "suhrkamp.de", "swamp.lt", "zachwamp.com",
        "tagesschau.de", "tifosamp.com", "tomkatcamp.ca", "ucr.edu", "unicamp.br",
        "unicamp.org", "vzwamp.com", "ville-guingamp.fr", "waltercamp.org", "wardsauto.com",
        "webamp.org", "webcitation.org", "winamp.com", "wadehamptoncamp.org", "yardbarker.com",
        "zoutkamp.net", "delcamp.cat", "anthonyjcamp.com", "lamaimuaythaicamp.com", "wisebigmancamp.com",
        "pricecamp.org", "revolutioncamp.it", "sturdycamp.com", "larkcamp.com", "greencamp.com",
        "shumen-camp.info", "camp.lv", "railcamp.com", "thevalleycamp.com", "odette-camp.fr",
        "yurucamp.jp", "stlcamp.org", "uni-koeln.de", "altcamp.info", "eki-stamp.com",
        "lamp.ac.uk", "longcamp.com", "roaringcamp.com", "koreanculturecamp.net", "subwaystamp.com",
        "lankastamp.com", "ramp.com", "hipstamp.com", "rosekamp.dk", "numistamp.com",
        "vamp.org", "idolchamp.com", "mysticstamp.com", "pleinchamp.com", "sanskrit-lamp.org",
        "ghanamps.com", "tradjazzcamp.com", "mariekenijkamp.com", "cybercamp.es", "linecamp.com",
        "reebokabcdcamp.com", "lsamp.neu.edu", "andrew-reynolds-bootcamp.com", "rawramp.me", "skycamp.pl",
        "campaignlive.co.uk", "snowcamp.org", "voteforshamp.com", "facamp.com.br", "puccamp.br",
        "policamp.edu.br", "gavinstamp.co.uk", "ceciliastamp.com", "agnesstamp.com", "greatswamp.org",
        "supertramp.com", "apramp.org", "portofinoamp.it", "marinalystcamp.dk", "vestbirk.dk-camp.dk",
        "rduchamp.fr", "barcamp.org", "thomasroewekamp.de", "handstamp.com", "maasaicamp.com",
        "openwebcamp.com", "grovedaycamp.com", "artsurfcamp.com", "rccamp.org", "jz-kamp.de",
        "nystamp.org", "aiamp.info", "usana-amp.com", "eaguingamp.com", "devbootcamp.com",
        "anthonycamp.com", "academystamp.com", "buddhiststamp.com", "metalcamp.com", "gnulamp.com",
        "mountainstamp.com", "freecodecamp.org", "horschamp.org", "bueschelskamp.de", "thorpecamp.org.uk",
        "droverscamp.com.au", "mainefiddlecamp.org", "a-camp.org", "greentourismcamp.com", "amp.acdh.oeaw.ac.at",
        "profcamp.tripod.com", "muschamp.org.uk", "artistcamp.com", "museumparkharskamp.nl", "maamp.us",
        "pacamp.com", "davidkamp.com", "climbcamp.fr", "rentocamp.com", "conventioncamp.de",
        "chinesestamp.org", "laselvadelcamp.org", "bohemiamp.cz", "salsacamp.de", "kingswamp.com",
        "zamp.hr", "themusicswamp.com", "cripcamp.com", "caamp.info", "wanhuamp.com",
        "swamp.org", "nyscamp.org", "aberdaroncamp.com", "comparecamp.com", "knowyourrightscamp.com",
        "perlmancamp.org", "svjappenkamp.nl", "iamp.org", "swamp.osu.edu", "yag-hamacamp.main.jp",
        "midwestbanjocamp.com", "wellcamp.com.au", "datamp.org", "balisurfingcamp.com", "wwe.com",
        "swissinfo.ch", "trueofvamp.dreamful.org", "spacamp.net", "klimacamp.fridaysforfuture.berlin", "attheamp.com",
        "ramonchamp.fr", "transvisionvamp.com", "eys-workcamp.de", "hipcamp.com", "mowjcamp.ws",
        "kitchenercamp.co.uk", "ecocamp.travel", "arthellcoalcamp.com", "longchamp.com", "vahrenkamp.org",
        "fineartscamp.org", "ggslangekamp.de", "kgs-meerkamp.de", "gs-amrosenkamp.de", "ggs-blumenkamp.de",
        "grundschule-heidkamp.de", "kgs-eikamp.de", "ggs-alten-kamp.bobi.net", "isrsummercamp.org", "nativecamp.net",
        "grundschule-kuhlerkamp.de", "gymnasium-rheinkamp.de", "beisenkamp.eu", "schule-am-buschkamp.de", "annehartkamp.de",
        "elettronicafacile.it", "indiewebcamp.com", "rutgermolenkamp.nl", "backtothesugarcamp.com", "bonestamp.com",
        "popsci.com", "popsci.com.au", "dell.com", "itworld.com",  # popsci usually redirects to 404 pages
        "nieuwsblad.be", # requested on talkpage, fetched urls are from another domain
        "amp-lessons.com", "championat.com", "rockcamp.es", "memorial-chiry-ourscamp.fr", "editoraunicamp.com.br",
        "eurocamp.co.uk", "toocamp.com", "orangecamp.dk", "thedailycampus.com", "adunicamp.org.br",
        "mellencamp.com", "coltscamp.com", "bonsallcamp.co.uk", "tuttocalciocampano.it", "forestcamp.info",
        "jeremycamp.com", "shawncamp.com", "co.camp.tx.us", "macamp.com.br", "thesyriacampaign.org",
        "jimcalhouncamp.com", "pinecrestswimcamp.com", "live2camp.com.au", "fitnesscamp.co.uk",  "tech-camp.in",
        "everythingsummercamp.com", "mowjcamp.com", "emucamp.com", "worldcupfancamp.com",
        "azurebootcamp.com", "laselvadelcamp.cat", "santpaudelcamp.info", "navylacrossecamp.com", "joinfightcamp.com",
        "camp.gob.mx", "my3camp.pl", "copycamp.pl", "microcamp.com.br", "blogdopresidentemicrocamp.com.br",
        "makeachamp.com", "blueridgecamp.com", "billieswamp.com", "wandcamp.com", "dpcamp.de",
        "spacecamp.com", "pctechbootcamp.com", "fukudajudocamp.org", "ville-fecamp.fr", "locmariagrandchamp.fr",
        "loulansverchamp.fr", "neuvy-grandchamp.com", "saint-genest-lachamp.fr", "vercel-villedieu-le-camp.fr", "kettenkamp.de",
        "cordclamp.com", "highcamp.tripod.com", "texastornadobootcamp.com", "highcamp.web.id", "baungcamp.com",
        "wellspringcamp.co.uk", "amprofon.com", "amprofon.com.mx", "ampers.org", "makeachamp.com",
        "steampowered.com", "ourcampaigns.com", "ourcampaigns.com", "whosampled.com", "soypampeano.com",
        "archiviolastampa.it", "footchampion.com", "campionicalcio.com", "thesportscampus.com", "swampland.time.com", "tampabay.com",
        "nottinghampost.com", "bramptonguardian.com", "ncresearchcampus.net", "en.unpacampaign.org", "camp-fire.jp",
        "championshiprugby.co.uk", "namport.com.na", "hampshirechronicle.co.uk", "panampost.com", "wokinghampaper.co.uk",
        "bramptonwest.conservativeeda.ca", "easthamptonstar.com", "postalmuseum.si.edu", "canadianstampnews.com", "tampabaytimesforum.com",
        "hamptonschool.org.uk", "tampabayprotocol.com", "tuttocampo.it", "campaignindia.in", "campiflegrei.it",
        "opencampania.it", "bundescamp.de", "codecamp.jp", "ael-stamp.jp", "okefenokeeswamp.com",
        "servamp.jp", "ffamp.com", "bundescamp.de", "heavenstamp.net", "stopstamp.ru",
        "bohnenkamp.de", "maiamp.gov.my", "joachimstamp.de", "nicolestamp.com", "ampalestine.org",
        "kenmorestamp.com", "samp.pt", "mathcamp.org", "acacamp.org", "jewishcamp.org",
        "henristeenkamp.org", "jeffkottkamp.com", "panstamp.com", "my-camp.org", "letabarestcamp.com",
        "skatecamp.co.uk", "armenstamp.com", "galiscamp.gr", "altcamp.cat", "soccercamp.com",
        "reagrupamentbaixcamp.cat", "warburg.chaa-unicamp.com.br", "yarmoukcamp.net", "campos24horas.com.br", "grammarcamp.com",
        "ticketcamp.net", "baycamp.net", "gamercamp.ca", "urbancamp.net", "comuencamp.ad",
        "bootcamp.com", "camperchamp.com.au", "matomocamp.org", "mtccamp.org", "brokenamp.com",
        "adelaidenow.com", "foreign.go.tz", "padua-access.stuttgart.de", "wdwinfo.com", # from exact_skip_urls
        "powcamp.fsnet.co.uk", "altcamp.altanet.org", "maesaelephantcamp.com", "fanamp.com", "nifs.no",
        "silberkamp.de", "hikamp.com", "echosonicamp.com", "tannensmagiccamp.com", "bundespolizeibiker-camp.de",
        "goshiki-camp.com", "infocamp.cat", "psicamp.it", "galescreekcamp.org", "understandingduchamp.com",
        "wordcamp.org", "stamp.umd.edu", "heavenstamp.com", "elementsmusiccamp.com.ph", "springlakedaycamp.com",
        "frihetskamp.net", "frihetskamp.no", "bigstamp.uk", "phootcamp.com", "fortfun-abenteuercamp.de",
        "ifch.unicamp.br", "icc-camp.info", "secustamp.com", "adacamp.org", "mibumpirecamp.com",
        "ciwangunindahcamp.com", "requiemchevaliervamp.free.fr", "amp.org.ph", "polarcamp.com", "cocacamp.nl",
        "motutapucamp.org.nz", "ot-guingamp.org", "nalbandstamp.com", "erikaskicamp.com", "trolltamp.com",
        "climatecamp.tv", "climatecamp.org.uk", "danielheidkamp.com", "rapchamp.com", "howdycamp.tamu.edu",
        "t-camp.tamu.edu", "garrettcamp.com", "heswallcamp.org.uk", "witchcamp.org", "spacecamp.no",
        "objcamp.com", "procamps.com", "pbacamp.org", "samusicmag.co.za", "swedensocialwebcamp.com",
        "bloodybloodybiblecamp.com", "nationalradiochamp.com", "supercamp.com", "miznerparkamp.com", "thijsbroekkamp.com",
        "cio.com", "camp.kg", "adventure-camp.com", "centralfriendscamp.org", "camp.kg",
        "urcamp.edu.br", "cciamp.com", "sturtevantcamp.org", "nextgenchamp.com", "vamp.ee",
        "workramp.com",

    ]
]

skip_url_patterns.append(
    r"^https?://(?:[\w.-]+\.)?books\.google\.[\w.-]+(/.*)?$"
)

def get_wiki_sites_a():
    return {f"{code}wiki": Site(code, "wikipedia") for code in [
        "en", "fr", "es", "pl", "ja", "ar", "fa", "ko", "no", "cs", "ro", "ms", "hy", "bg", "el", "et", "ur", "lt", "ka", "bn", "hi",
        "lv", "te", "sq", "mr", "be-tarask", "nds", "ky", "ha", "pms", "mzn", "su", "pa", "tl", "ig", "sco", "gu", "crh", "scn", "qu",
        "os", "ps", "sd", "cdo", "yi", "li", "shn", "fo", "ie", "ff", "sa", "km", "bjn", "shi", "hak", "tly", "rw", "co", "mi", "sc",
        "kw", "gv", "smn", "gn", "udm", "lo", "fur", "tw", "lg", "stq", "lad", "gom", "fon", "gag", "bxr", "szy", "awa", "atj", "om",
        "nov", "fat", "dtp", "fj", "st", "guw", "tpi", "gur", "mos", "sm", "srn", "rki", "chr", "igl", "rmy", "guc", "ch", "tdd", "iu",
]}

def get_wiki_sites_b():
    return {f"{code}wiki": Site(code, "wikipedia") for code in [
        "ceb", "sv", "ru", "arz", "uk", "war", "ca", "sr", "tr", "tt", "eu", "he", "uz", "cy", "be", "azb", "hr", "az", "lld", "th", "mk",
        "ast", "tg", "sw", "ku", "br", "lmo", "pnb", "new", "vec", "ba", "io", "cv", "glk", "yo", "kn", "ia", "bar", "bpy", "skr", "bcl",
        "frr", "tum", "gd", "am", "nap", "mai", "sat", "dag", "ace", "hif", "zu", "mhr", "mni", "rue", "so", "bh", "ks", "se", "mdf", "vep",
        "kab", "ab", "frp", "csb", "nrm", "ln", "lfn", "mwl", "ext", "rm", "koi", "za", "blk", "krc", "inh", "pdc", "ki", "iba", "wo",
        "anp", "xal", "kg", "pcm", "tet", "bbc", "ee", "lbe", "ltg", "gcr", "got", "bm", "chy", "ik", "nup", "sg", "dz",
]}
# tok not available in pywikibot
def get_wiki_sites_c():
    return {f"{code}wiki": Site(code, "wikipedia") for code in [
        "de", "nl", "it", "zh", "vi", "pt", "id", "ce", "fi", "hu", "sh", "eo", "da", "simple", "sk", "kk", "gl", "sl", "ta", "nn",
        "la", "af", "my", "mg", "oc", "ml", "ckb", "jv", "ht", "lb", "ga", "szl", "an", "vo", "ban", "als", "avk", "mn", "si", "nv",
        "as", "or", "sah", "bug", "ilo", "gor", "hsb", "eml", "hyw", "wa", "zgh", "sn", "kaa", "mrj", "pam", "ug", "nso", "vls", "myv",
        "bo", "tk", "gan", "pcd", "kv", "ay", "pap", "olo", "lez", "gpe", "tyv", "tn", "dsb", "bew", "haw", "pfl", "pag", "xh", "mad",
        "arc", "nia", "jam", "kbd", "nqo", "knc", "bi", "jbo", "cu", "syl", "ss", "ny", "rsk", "ts", "ve", "rn", "ady", "pnt", "ann",
]}

def get_wiki_sites_1():
    return {f"{code}wiki": Site(code, "wikipedia") for code in [
        "en", "de", "sv", "es", "it", "arz", "ja", "vi", "war", "fa", "id", "sr", "no", "fi", "tt", "ro", "sh", "zh-min-nan", "eo", "uz",
        "bg", "simple", "be", "et", "kk", "hr", "lt", "lld", "ta", "th", "hi", "la", "ast", "te", "my", "sw", "mr", "ku", "be-tarask", "ml",
        "lmo", "ky", "jv", "new", "pms", "lb", "io", "pa", "cv", "tl", "glk", "ig", "sco", "kn", "gu", "avk", "crh", "scn", "si", "qu",
        "os", "as", "or", "tum", "bat-smg", "gd", "yi", "ilo", "nap", "shn", "fo", "map-bms", "ie", "hyw", "ace", "sa", "km", "sn", "mhr", "shi",
        "mrj", "rue", "tly", "ug", "rw", "nso", "ks", "mi", "myv", "mt", "bo", "vep", "gv", "gan", "ab", "gn", "kv", "ay", "nrm", "fur",
        "olo", "lfn", "lg", "stq", "tyv", "rm", "gom", "dsb", "bew", "gag", "haw", "blk", "szy", "pag", "inh", "atj", "mad", "om", "arc",
        "iba", "fat", "jam", "anp", "fj", "nqo", "kg", "guw", "bi", "roa-rup", "jbo", "bbc", "mos", "syl", "lbe", "ss", "alt", "ny", "gcr", "chr",
        "ts", "bm", "rmy", "rn", "ik", "ch", "pnt", "sg", "iu",
]}

def get_wiki_sites_2():
    return {f"{code}wiki": Site(code, "wikipedia") for code in [
        "ceb", "fr", "nl", "pl", "zh", "uk", "ar", "pt", "ca", "ko", "ce", "tr", "hu", "cs", "eu", "ms", "he", "hy",
        "da", "cy", "el", "sk", "azb", "ur", "gl", "sl", "ka", "bn", "nn", "mk", "lv", "af", "tg", "sq", "mg", "bs", "oc", "br",
        "nds", "ckb", "pnb", "ha", "vec", "ht", "ba", "ga", "su", "szl", "fy", "an", "wuu", "vo", "yo", "ban", "als", "ia",
        "bar", "mn", "bpy", "ps", "frr", "sd", "sah", "cdo", "bug", "am", "li", "gor", "sat", "eml", "dag", "ff", "wa", "hif", "zgh",
        "zu", "bjn", "kaa", "mni", "hak", "pam", "so", "roa-tara", "bh", "co", "vls", "se", "sc", "mdf", "kw", "tk", "kab", "smn",
        "pcd", "frp", "udm", "csb", "lo", "pap", "lez", "tw", "ln", "mwl", "gpe", "ext", "lad", "tn", "koi", "fon", "cbk-zam", "dv", "ksh", "za",
        "bxr", "pfl", "krc", "awa", "xh", "pdc", "mnw", "ki", "nov", "nia", "wo", "dtp", "kbd", "xal", "st", "knc", "pcm", "tpi", "tet", "gur",
        "cu", "ee", "sm", "ami", "srn", "ltg", "rki", "rsk", "got", "igl", "ve", "chy", "guc", "ady", "nup", "tdd", "ann", "dz", "mzn", "skr",
        "bcl", "hsb", "ru", "nv",
    ]}

def get_wiki_sites():
    return {f"{code}wiki": Site(code, "wikipedia") for code in [
    "en", "de", "es", "fr", "it", "pl", "pt", "id", "mr", "nn", "sl",
    "ab", "ace", "ady", "af", "als", "am", "ami", "ang", "an", "anp", "ar", "arc", "arz", "as", "ast", "atj", "av", "avk", "awa", "ay",
    "ba", "ban", "bar", "bbc", "bcl", "be", "be-tarask", "bg", "bh", "bi", "bjn", "blk", "bm", "bn", "bo", "bpy", "br", "bug", "bxr",
    "ca", "cdo", "ce", "ceb", "ch", "chr", "chy", "ckb", "co", "cr", "crh", "cs", "csb", "cu", "cv", "cy", "da", "dag", "dga", "din", "diq", "dsb", "dty", "dz",
    "ee", "el", "eml", "eo", "et", "eu", "ext", "fa", "fat", "ff", "fi", "fj", "fo", "fon", "frp", "frr", "fur",
    "ga", "gag", "gan", "gcr", "gd", "glk", "gn", "gom", "gor", "got", "gpe", "gu", "guc", "gur", "guw", "gv", "ha", "hak", "haw", "he", "hi", "hif", "hr", "hsb", "ht", "hu", "hy", "hyw",
    "ia", "ie", "ig", "ik", "ilo", "inh", "io", "iu", "ja", "jam", "jbo", "jv",
    "ka", "kaa", "kab", "kbd", "kbp", "kcg", "kg", "ki", "kk", "kl", "km", "kn", "ko", "koi", "krc", "ks", "ku", "kv", "kw", "ky",
    "la", "lad", "lb", "lbe", "lez", "lfn", "lg", "li", "lij", "lld", "lmo", "ln", "lo", "lt", "ltg", "lv",
    "mad", "mai", "mdf", "mg", "mhr", "mi", "min", "mk", "ml", "mn", "mni", "mrj", "ms", "mwl", "my", "myv", "mzn",
    "nah", "nap", "ne", "new", "nia", "nl", "no", "nov", "nqo", "nrm", "nso", "nv", "ny", "oc", "olo", "om", "or", "os",
    "pa", "pag", "pam", "pap", "pcd", "pcm", "pdc", "pfl", "pi", "pms", "pnb", "pnt", "ps", "pwn", "qu", "rm", "rmy", "rn", "ro", "rue", "ru", "rw",
    "sa", "sah", "sat", "scn", "sc", "sco", "sd", "se", "sg", "sh", "shi", "shn", "si", "simple", "sk", "skr", "sm", "smn", "sn", "so", "sq", "srn", "ss", "st", "stq", "su", "sv", "sw", "szl", "szy",
    "ta", "tay", "tcy", "tet", "te", "tg", "th", "ti", "tk", "tl", "tly", "tn", "to", "tpi", "trv", "ts", "tt", "tum", "tw", "tyv", "ty",
    "udm", "ug", "uk", "uz", "vec", "vep", "ve", "vls", "vo", "wa", "war", "wo", "xal", "xh", "xmf", "yi", "yo", "za", "zea", "zh", "zgh", "zu",
]}

def get_wikinews_sites():
    return {f"{code}wiki": Site(code, "wikinews") for code in [
    "ar", "bg", "bs", "ca", "cs", "el", "en", "eo", "fa", "fi", "guw", "he", "hu", "ja", "ko", "li",
    "nl", "no", "pl", "pt", "ro", "sd", "sq", "sr", "sv", "ta", "th", "tr", "uk", "zh",
]}

# exists, but not available in pywikibot: "ann", "bdr", "bew", "btm", "dtp", "iba", "igl", "kge", "knc", "kus", "mos", "nr", "nup", "rsk", "syl", "tdd", "tig",
# wikinews: shn,

# dictionary of edit summaries for each wikipedia language
default_summary = "removed AMP tracking from URLs ([[:m:User:KiranBOT/AMP|details]]) ([[User talk:Usernamekiran|report error]]) v3.1.1s"

edit_summaries = {
    "en": default_summary,
    "de": "Bot: AMP-Tracking aus URLs entfernt ([[:m:User:KiranBOT/AMP|details]]) ([[User talk:Usernamekiran|Fehler melden]]) v3.1.1s",
    "es": "eliminación del seguimiento AMP en URLs ([[:m:User:KiranBOT/AMP|detalles]]) ([[User talk:Usernamekiran|reportar error]]) v3.1.1s",
    "fr": "suppression du suivi AMP dans les URLs ([[:m:User:KiranBOT/AMP|détails]]) ([[User talk:Usernamekiran|signaler une erreur]]) v3.1.1s",
    "it": "rimosso il tracciamento AMP dagli URL ([[:m:User:KiranBOT/AMP|dettagli]]) ([[Discussioni utente:Usernamekiran|segnala errore]]) v3.1.1s",
    "pl": "Usunięto śledzenie AMP z adresów URL ([[:m:User:KiranBOT/AMP|szczegóły]]) ([[User talk:Usernamekiran|zgłoś błąd]]) v3.1.1s",
    "pt": "BOT: remoção do rastreamento AMP das URLs ([[:m:User:KiranBOT/AMP|detalhes]]) ([[User talk:Usernamekiran|reportar erro]]) v3.1.1s",
    "ab": "Ианыхуп AMP ашьҭаԥшра URL аҟынтәи ([[:m:User:KiranBOT/AMP|ахәҭаҷқәа]]) ([[User talk:Usernamekiran|aгха аҳасабырба]]). v3.1.1s",
    "ace": "Peulacak AMP ka geubôh nibak URL ([[:m:User:KiranBOT/AMP|detil]]) ([[User talk:Usernamekiran|lapor kasalahan]]) v3.1.1s",
    "af": "het AMP-opsporing van URL'e verwyder ([[:m:User:KiranBOT/AMP|besonderhede]]) ([[User talk:Usernamekiran|rapporteer fout]]) v3.1.1s",
    "am": "የAMP ክትትልን ከዩአርኤሎች ተወግዷል ([[:m:User:KiranBOT/AMP|ዝርዝሮች]]) ([[User talk:Usernamekiran|ስህተት ሪፖርት አድርግ]]) v3.1.1s",
    "ang": "afscerod AMP-tracking from URLs ([[:m:User:KiranBOT/AMP|dǣl]]) ([[User talk:Usernamekiran|forwyrd-an eor]]) v3.1.1s",
    "ar": "إزالة تتبع AMP من عناوين URL ([[:m:User:KiranBOT/AMP|التفاصيل]]) ([[نقاش المستخدم:Usernamekiran|خطأ في الإبلاغ]]) v3.1.1s",
    "arc": "AMP-Tracking ܡܢ URLs ܡܢܝܬ ([[:m:User:KiranBOT/AMP|ܐܢܬܐ]]) ([[User talk:Usernamekiran|ܐܙܠ ܕܠܝܠ]]) v3.1.1s",
    "arz": "AMP-Tracking mn URLs itfrrdu ([[:m:User:KiranBOT/AMP|tafaṣṣīl]]) ([[User talk:Usernamekiran|tārīkh ϻałʿūṭ]]) v3.1.1s",
    "as": "AMP-Tracking URLs ৰ পৰা আঁতৰোৱা হৈছে ([[:m:User:KiranBOT/AMP|বিশদ]]) ([[User talk:Usernamekiran|ভুল প'ৰিবেশ]]) v3.1.1s",
    "ast": "Desaniciaos los parámetros de rastrexu AMP de les URL ([[:m:User:KiranBOT/AMP|detalles]]) ([[User talk:Usernamekiran|informar d'un error]]) v3.1.1s",
    "atj": "AMP-Tracking URL hite eskeri ([[:m:User:KiranBOT/AMP|detaylar]]) ([[User talk:Usernamekiran|hata raporlama]]) v3.1.1s",
    "av": "AMP-Tracking URL-lär hanalhiy ([[:m:User:KiranBOT/AMP|tağlar]]) ([[User talk:Usernamekiran|hataları raporlama]]) v3.1.1s",
    "avk": "AMP-Tracking URLs dan girlemişti ([[:m:User:KiranBOT/AMP|detallar]]) ([[User talk:Usernamekiran|hatalar bildirin]]) v3.1.1s",
    "awa": "AMP-Tracking URLs se hatawā chiṭi ([[:m:User:KiranBOT/AMP|details]]) ([[User talk:Usernamekiran|bug report]]) v3.1.1s",
    "ay": "AMP-Tracking URLs qhanqʼa ([[:m:User:KiranBOT/AMP|detalles]]) ([[User talk:Usernamekiran|error reporte]]) v3.1.1s",
    "az": "AMP-Tracking URL-lərdən çıxarıldı ([[:m:User:KiranBOT/AMP|detallar]]) ([[User talk:Usernamekiran|xətanı bildirmək]]) v3.1.1s",
    "azb": "AMP-Tracking URL-lərdən qaldırıldı ([[:m:User:KiranBOT/AMP|detallar]]) ([[User talk:Usernamekiran|səhv bildirmək]]) v3.1.1s",
    "ba": "URL-адрестарҙан AMP күҙәтеүен юйҙыҡ ([[:m:User:KiranBOT/AMP|тулыраҡ мәғлүмәт]]) ([[User talk:Usernamekiran|хата тураһында хәбәр]]) v3.1.1s",
    "be": "выдалена адсочванне AMP з URL-адрасоў ([[:m:User:KiranBOT/AMP|падрабязнасці]]) ([[User talk:Usernamekiran|паведаміць пра памылку]]) v3.1.1s",
    "be-tarask": "выдалена адсочванне AMP з URL-адрасоў ([[:m:User:KiranBOT/AMP|падрабязнасці]]) ([[User talk:Usernamekiran|паведаміць пра памылку]]) v3.1.1s",
    "bg": "премахнато е AMP проследяване от URL адреси ([[:m:User:KiranBOT/AMP|подробности]]) ([[User talk:Usernamekiran|докладвай грешка]]) v3.1.1s",
    "bn": "URL থেকে AMP ট্র্যাকিং সরানো হয়েছে ([[:m:User:KiranBOT/AMP|বিস্তারিত]]) ([[User talk:Usernamekiran|ত্রুটি রিপোর্ট করুন]]) v3.1.1s",
    "br": "tennet eo bet an heuliañ AMP diouzh an URLoù ([[:m:User:KiranBOT/AMP|munudoù]]) ([[User talk:Usernamekiran|kemenn ur fazi]]) v3.1.1s",
    "bs": "uklonjeno AMP praćenje iz URL-ova ([[:m:User:KiranBOT/AMP|detalji]]) ([[User talk:Usernamekiran|prijavi grešku]]) v3.1.1s",
    "ca": "Eliminació del seguiment AMP de les URL ([[:m:User:KiranBOT/AMP|detalls]]) ([[User talk:Usernamekiran|informeu d'errors]]) v3.1.1s",
    "ceb": "gitangtang ang pagsubay sa AMP gikan sa mga URL ([[:m:User:KiranBOT/AMP|mga detalye]]) ([[User talk:Usernamekiran|pagtaho ug sayop]]) v3.1.1s",
    "ckb": "شوێنپێهەڵگرتنی AMP لە URLەکان لابرد ([[:m:User:KiranBOT/AMP|ووردەکاریەکان]]) ([[User talk:Usernamekiran|هەڵەیەک ڕاپۆرت بکە]]) v3.1.1s",
    "cs": "odstraněno sledování AMP z URL adres ([[:m:User:KiranBOT/AMP|podrobnosti]]) ([[User talk:Usernamekiran|nahlásit chybu]]) v3.1.1s",
    "cv": "URL-сенчен AMP сӑнаса тӑрассине кӑларса пӑрахнӑ ([[:m:User:KiranBOT/AMP|даннӑйсем]]) ([[User talk:Usernamekiran|йӑнӑш ҫинчен пӗлтер]]) v3.1.1s",
    "cy": "wedi tynnu olrhain AMP o URLau ([[:m:User:KiranBOT/AMP|manylion]]) ([[User talk:Usernamekiran|adrodd am wall]]) v3.1.1s",
    "da": "fjernede AMP-sporing fra URL'er ([[:m:User:KiranBOT/AMP|detaljer]]) ([[User talk:Usernamekiran|rapporter en fejl]]) v3.1.1s",
    "el": "κατάργησε την παρακολούθηση AMP από τις διευθύνσεις URL ([[:m:User:KiranBOT/AMP|καθέκαστα]]) ([[User talk:Usernamekiran|αναφορά σφάλματος]]) v3.1.1s",
    "eo": "forigis AMP-spuradon de URL-oj  ([[:m:User:KiranBOT/AMP|detaloj]]) ([[User talk:Usernamekiran|raporti eraron]]) v3.1.1s",
    "et": "eemaldas URL-idelt AMP jälgimise  ([[:m:User:KiranBOT/AMP|detailid]]) ([[User talk:Usernamekiran|teata veast]]) v3.1.1s",
    "eu": "AMP jarraipena URLetatik kendu da ([[:m:User:KiranBOT/AMP|xehetasunak]]) ([[User talk:Usernamekiran|errorea jakinarazi]]) v3.1.1s",
    "fa": "حذف ردیابی AMP از URLها ([[:m:User:KiranBOT/AMP|جزئیات]]) ([[User talk:Usernamekiran|گزارش خطا]]) v3.1.1s",
    "fi": "AMP-seuranta poistettu URL-osoitteista ([[:m:User:KiranBOT/AMP|lisätietoja]]) ([[User talk:Usernamekiran|ilmoita virheestä]]) v3.1.1s",
    "ga": "baineadh rianú AMP de URLanna ([[:m:User:KiranBOT/AMP|sonraí]]) ([[User talk:Usernamekiran|tuairiscigh earráid]]) v3.1.1s",
    "ha": "cire bin AMP daga URLs ([[:m:User:KiranBOT/AMP|cikakkun bayanai]]) ([[User talk:Usernamekiran|rahoton kuskure]]) v3.1.1s",
    "he": "הסרת מעקב AMP מכתובות URL ([[:m:User:KiranBOT/AMP|פרטים]]) ([[User talk:Usernamekiran|דווח על שגיאה]]) v3.1.1s",
    "hi": "AMP-Tracking को URLs से हटाया ([[:m:User:KiranBOT/AMP|विवरण]]) ([[User talk:Usernamekiran|त्रुटि दर्ज करें]]) v3.1.1s",
    "hr": "uklonjeno je AMP praćenje iz URL-ova ([[:m:User:KiranBOT/AMP|detalji]]) ([[User talk:Usernamekiran|prijavi grešku]]) v3.1.1s",
    "hu": "AMP-követés eltávolítva az URL-ekből ([[:m:User:KiranBOT/AMP|részletek]]) ([[User talk:Usernamekiran|hibabejelentés]]) v3.1.1s",
    "hy": "հեռացվել է AMP հետևումը URL-ներից ([[:m:User:KiranBOT/AMP|մանրամասներf]]) ([[User talk:Usernamekiran|հաղորդել սխալի մասին]]) v3.1.1s",
    "ht": "retire swivi AMP nan URL yo ([[:m:User:KiranBOT/AMP|detay]]) ([[User talk:Usernamekiran|rapòte yon erè]]) v3.1.1s",
    "id": "Pelacakan AMP dihapus dari URL ([[:m:User:KiranBOT/AMP|rincian]]) ([[User talk:Usernamekiran|laporkan kesalahan]]) v3.1.1s",
    "ja": "URLからアプリトラッキングを削除 ([[:m:User:KiranBOT/AMP|詳細]]) ([[User talk:Usernamekiran|エラーを報告]]) v3.1.1s",
    "jv": "mbusak pelacakan AMP saka URL ([[:m:User:KiranBOT/AMP|rincian]]) ([[User talk:Usernamekiran|laporan kesalahan]]) v3.1.1s",
    "ka": "URL-ებიდან AMP თვალთვალი წაიშალა ([[:m:User:KiranBOT/AMP|დეტალები]]) ([[User talk:Usernamekiran|შეცდომის შესახებ შეტყობინება]]) v3.1.1s",
    "ko": "URL에서 AMP 추적을 제거했습니다 ([[:m:User:KiranBOT/AMP|세부]]) ([[User talk:Usernamekiran|오류 보고]]) v3.1.1s",
    "ku": "şopandina AMP ji URLan hate rakirin ([[:m:User:KiranBOT/AMP|hûrgulî]]) ([[User talk:Usernamekiran|çewtiyek rapor bike]]) v3.1.1s",
    "ky": "URL'дерден AMP көз салуу алынып салынды ([[:m:User:KiranBOT/AMP|майда-чүйдөсүнө чейин]]) ([[User talk:Usernamekiran|ката жөнүндө кабарлоо]]) v3.1.1s",
    "la": "vestigationem AMP ex URL remotam ([[:m:User:KiranBOT/AMP|singularia]]) ([[User talk:Usernamekiran|errorem nuntia]]) v3.1.1s",
    "lb": "AMP-Tracking vun URLen ewechgeholl ([[:m:User:KiranBOT/AMP|detailer]]) ([[User talk:Usernamekiran|feeler mellen]]) v3.1.1s",
    "lmo": "eliminà el tracciament AMP di URL ([[:m:User:KiranBOT/AMP|detali]]) ([[User talk:Usernamekiran|segnalà un errur]]) v3.1.1s",
    "lt": "pašalintas AMP stebėjimas iš URL ([[:m:User:KiranBOT/AMP|detalės]]) ([[User talk:Usernamekiran|pranešti apie klaidą]]) v3.1.1s",
    "lv": "noņemta AMP izsekošana no URL ([[:m:User:KiranBOT/AMP|sīkāka informācija]]) ([[User talk:Usernamekiran|ziņot par kļūdu]]) v3.1.1s",
    "mg": "nesorina ny fanaraha-maso AMP tamin'ny URL ([[:m:User:KiranBOT/AMP|tsipiriany]]) ([[User talk:Usernamekiran|mitatitra lesoka]]) v3.1.1s",
    "min": "dihapuih palacakan AMP dari URL ([[:m:User:KiranBOT/AMP|detail]]) ([[User talk:Usernamekiran|malaporkan kasalahan]]) v3.1.1s",
    "ml": "URL-കളിൽ നിന്ന് AMP ട്രാക്കിംഗ് നീക്കം ചെയ്തു  ([[:m:User:KiranBOT/AMP|വിശദാംശങ്ങൾ]]) ([[User talk:Usernamekiran|പിശക് റിപ്പോർട്ട് ചെയ്യുക]]) v3.1.1s",
    "mr": "दुव्यांमधील AMP ट्रॅकिंग काढले ([[:m:User:KiranBOT/AMP|माहिती]]) ([[User talk:Usernamekiran|त्रुटी नोंदवा]]) v3.1.1s",
    "ms": "Penjejakan AMP telah dialih keluar dari URL ([[:m:User:KiranBOT/AMP|butiran]]) ([[User talk:Usernamekiran|laporkan ralat]]) v3.1.1s",
    "my": "AMP ခြေရာခံခြင်းကို URL မှ ဖယ်ရှားခဲ့သည်။ ([[:m:User:KiranBOT/AMP|အသေးစိတ်]]) ([[User talk:Usernamekiran|အမှားအယွင်းတစ်ခုကို သတင်းပို့ပါ။]]) v3.1.1s",
    "nds": "Bot: AMP-Tracking ut de URLs rutmaakt ([[:m:User:KiranBOT/AMP|Details]]) ([[User talk:Usernamekiran|Fehler mellen]]) v3.1.1s",
    "new": "यूआरएलपाखें एएमपि ट्राकिङ्ग लिकयाबिल ([[:m:User:KiranBOT/AMP|विवरण]]) ([[User talk:Usernamekiran|छगू द्वंगु रिपोर्ट]]) v3.1.1s",
    "nl": "AMP-tracking uit URL's verwijderd ([[:m:User:KiranBOT/AMP|details]]) ([[User talk:Usernamekiran|fout melden]]) v3.1.1s",
    "nn": "fjernet AMP-sporing fra URL-er ([[:m:User:KiranBOT/AMP|detaljer]]) ([[User talk:Usernamekiran|rapporter en feil]]) v3.1.1s",
    "no": "fjernet AMP-sporing fra URL-er ([[:m:User:KiranBOT/AMP|detaljer]]) ([[User talk:Usernamekiran|rapporter en feil]]) v3.1.1s",
    "oc": "suprimit lo seguiment AMP de las URL ([[:m:User:KiranBOT/AMP|detalhs]]) ([[User talk:Usernamekiran|senhalar una error]]) v3.1.1s",
    "pa": "URL ਤੋਂ AMP ਟਰੈਕਿੰਗ ਹਟਾਈ ਗਈ ([[:m:User:KiranBOT/AMP|ਵੇਰਵੇ]]) ([[User talk:Usernamekiran|ਗਲਤੀ ਦੀ ਰਿਪੋਰਟ ਕਰੋ]]) v3.1.1s",
    "pms": "gjavât vie il monitoraç AMP dai URL ([[:m:User:KiranBOT/AMP|detais]]) ([[User talk:Usernamekiran|segnalâ un erôr]]) v3.1.1s",
    "ro": "a fost eliminată urmărirea AMP din adresele URL ([[:m:User:KiranBOT/AMP|detalii]]) ([[User talk:Usernamekiran|raportează o eroare]]) v3.1.1s",
    "ru": "удалено отслеживание AMP из URL-адресов ([[:m:User:KiranBOT/AMP|подробности]]) ([[User talk:Usernamekiran|сообщить об ошибке]]) v3.1.1s",
    "si": "URL වලින් AMP ලුහුබැඳීම ඉවත් කරන ලදී ([[:m:User:KiranBOT/AMP|විස්තර]]) ([[User talk:Usernamekiran|දෝෂයක් වාර්තා කරන්න]]) v3.1.1s",
    "simple": default_summary,
    "sk": "odstránené sledovanie AMP z URL adries ([[:m:User:KiranBOT/AMP|detaily]]) ([[User talk:Usernamekiran|nahlásiť chybu]]) v3.1.1s",
    "sl": "odstranjeno sledenje AMP iz URL-jev ([[:m:User:KiranBOT/AMP|podrobnosti]]) ([[User talk:Usernamekiran|prijavi napako]]) v3.1.1s",
    "sq": "gjurmimi i AMP u hoq nga URL-të ([[:m:User:KiranBOT/AMP|detajet]]) ([[User talk:Usernamekiran|raporto një gabim]]) v3.1.1s",
    "sr": "уклоњено AMP праћење из URL-ова ([[:m:User:KiranBOT/AMP|детаљи]]) ([[User talk:Usernamekiran|пријави грешку]]) v3.1.1s",
    "su": "dipiceun tracking AMP tina URL ([[:m:User:KiranBOT/AMP|rinci]]) ([[User talk:Usernamekiran|kasalahan laporan]]) v3.1.1s",
    "sv": "AMP-spårning borttagen från URL:er ([[:m:User:KiranBOT/AMP|detaljer]]) ([[User talk:Usernamekiran|rapportera fel]]) v3.1.1s",
    "sw": "iliondoa ufuatiliaji wa AMP kutoka kwa URL ([[:m:User:KiranBOT/AMP|maelezo]]) ([[User talk:Usernamekiran|ripoti hitilafu]]) v3.1.1s",
    "szl": "usuniynto śledzynie AMP z URL-ōw ([[:m:User:KiranBOT/AMP|detale]]) ([[User talk:Usernamekiran|zgłosić błōnd]]) v3.1.1s",
    "ta": "URL களில் இருந்து AMP கண்காணிப்பை அகற்றியது ([[:m:User:KiranBOT/AMP|விவரங்கள்]]) ([[User talk:Usernamekiran|பிழையைப் புகாரளிக்கவும்]]) v3.1.1s",
    "te": "URL నుండి AMP ట్రాకింగ్ తీసివేయబడింది ([[:m:User:KiranBOT/AMP|వివరాలు]]) ([[User talk:Usernamekiran|లోపాన్ని నివేదించండి]]) v3.1.1s",
    "tg": "пайгирии AMP аз URL хориҷ карда шуд ([[:m:User:KiranBOT/AMP|тафсилот]]) ([[User talk:Usernamekiran|дар бораи хато хабар диҳед]]) v3.1.1s",
    "th": "ลบการติดตาม AMP ออกจาก URL ([[:m:User:KiranBOT/AMP|รายละเอียด]]) ([[User talk:Usernamekiran|รายงานข้อผิดพลาด]]) v3.1.1s",
    "tl": "inalis ang pagsubaybay sa AMP sa mga URL ([[:m:User:KiranBOT/AMP|mga detalye]]) ([[User talk:Usernamekiran|mag-ulat ng error]]) v3.1.1s",
    "tr": "URL'lerden AMP izlemesi kaldırıldı ([[:m:User:KiranBOT/AMP|detaylar]]) ([[User talk:Usernamekiran|hata bildir]]) v3.1.1s",
    "uk": "видалено відстеження AMP з URL-адрес ([[:m:User:KiranBOT/AMP|деталі]]) ([[User talk:Usernamekiran|повідомити про помилку]]) v3.1.1s",
    "ur": "یوآرایل سے اے ایم پی (AMP) ٹریکنگ کو حذف کر دیا گیا ہے: ([[:m:User:KiranBOT/AMP|مزید تفصیلات]]) ([[User talk:Usernamekiran|غلطی سے آگاہ کریں]]) نسخہ 2.2.9s",
    "uz": "URL manzillardan AMP kuzatuvi olib tashlandi ([[:m:User:KiranBOT/AMP|tafsilotlar]]) ([[User talk:Usernamekiran|xato haqida xabar bering]]) v3.1.1s",
    "vec": "cavà el tracciamento AMP dai URL ([[:m:User:KiranBOT/AMP|detaji]]) ([[User talk:Usernamekiran|segnałar un eror]]) v3.1.1s",
}
