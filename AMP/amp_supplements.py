import pywikibot
from pywikibot import Site

# list of url patterns to skip
skip_url_patterns = [
    rf"^https?://(?:.*\.)?{domain}(/.*)?$" for domain in [
        "bandcamp.com", "suhrkamp.de", "waltercamp.org",
        "econtents.bc.unicamp.br", "middlewoodcamp.org.uk",
        "ilonahaberkamp.com", "larepublica-pe.cdn.ampproject.org",
        "elpopular-pe.cdn.ampproject.org", "amp.dev",
        "archive.today", "ghostarchive.org", "webcitation.org",
        "seedcamp.com", "champ.org.uk", "dwebcamp.org",
        "saejongcamp.org", "nsobegamecamp.com", "camptocamp.org",
        "seecamp.com", "angelscamp.gov", "vzwamp.com",
        "scoutcamp.org", "bamp.fr", "astronomycamp.org",
        "onecamp.com.au", "hey-alex.com", "wardsauto.com",
        "onlamp.com", "unicamp.br", "boamp.fr",
        "yardbarker.com", "rockcamp.com", "rockcamp.com",
        "slayalive.com", "oamp.fr", "ampalestine.org",
        "astrocamp.org", "emmelkamp.de", "tifosamp.com",
        "ronchamp.fr", "honeyrockcamp",
    ]
]

exact_skip_urls = {
    ## exact matches for the URLs to skip (with or without www)
    r"^https?://(?:www\.)?wdwinfo\.com/news-stories/amp-suit-decorated-with-holiday-theming-at-disneys-animal-kingdom/$",
    r"^https?://(?:www\.)?swissinfo\.ch/spa/las--fake-news--amplifican-el-miedo-y-la-confusi%C3%B3n-en-hong-kong/45380788$",
    r"^https?://(?:www\.)?padua-access\.stuttgart\.de/Access\.xhtml\?.*$",

}

# Set of words to check for skipping
skippable_words = {
    "amplio",  
    "ampel",
    "ampersand",
    "ampproject",
    "amp-project",
    "webarchive",
}
"""
# dictionary of supported sites
wiki_sites = {
    "enwiki": pywikibot.Site("en", "wikipedia"),
    "dewiki": pywikibot.Site("de", "wikipedia"),
    "eswiki": pywikibot.Site("es", "wikipedia"),
    "frwiki": pywikibot.Site("fr", "wikipedia"),
    "itwiki": pywikibot.Site("it", "wikipedia"),
    "plwiki": pywikibot.Site("pl", "wikipedia"),
    #"ptwiki": pywikibot.Site("pt", "wikipedia"),
}
"""
## single line combination for dictionary of supported sites
wiki_sites = {f"{code}wiki": Site(code, "wikipedia") for code in ["en", "de", "es", "fr", "it", "pl"]} #, "pt"

# dictionary of edit summaries for each wikipedia language
default_summary = "removed AMP tracking from URLs ([[:en:User:KiranBOT/AMP|details]]) ([[:en:User talk:Usernamekiran|report error]]) v2.2.3s"

edit_summaries = {
    "en": default_summary,
    "de": "Bot: AMP-Tracking aus URLs entfernt ([[:en:User:KiranBOT/AMP|details]]) ([[User talk:Usernamekiran|Fehler melden]]) v2.2.3s",
    "es": "eliminación del seguimiento AMP en URLs ([[:en:User:KiranBOT/AMP|detalles]]) ([[User talk:Usernamekiran|reportar error]]) v2.2.3s",
    "fr": "suppression du suivi AMP dans les URLs ([[:en:User:KiranBOT/AMP|détails]]) ([[User talk:Usernamekiran|signaler une erreur]]) v2.2.3s",
    "it": "rimosso il tracciamento AMP dagli URL ([[:en:User:KiranBOT/AMP|dettagli]]) ([[Discussioni utente:Usernamekiran|segnala errore]]) v2.2.3s",
    "pl": "Usunięto śledzenie AMP z adresów URL ([[:en:User:KiranBOT/AMP|szczegóły]]) ([[User talk:Usernamekiran|zgłoś błąd]]) v2.2.3s",
    "pt": "remoção do rastreamento AMP das URLs ([[:en:User:KiranBOT/AMP|detalhes]]) ([[User talk:Usernamekiran|reportar erro]]) v2.2.3s",
}

