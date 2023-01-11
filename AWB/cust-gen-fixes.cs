/// following is a module listing almost all the general fixes provided by AWB.
/// using this custom module, these fixes can be disabled or enabled as require.

WikiFunctions.Parse.Parsers parsers = new WikiFunctions.Parse.Parsers();
WikiFunctions.Parse.HideText removeText = new WikiFunctions.Parse.HideText(false, true, false);
WikiFunctions.Parse.HideText HiderHideExtLinksImages = new WikiFunctions.Parse.HideText(true, true, true);
 
public string ProcessArticle(string ArticleText, string ArticleTitle, int wikiNamespace, out string Summary, out bool Skip)
{
        Skip = false;
        Summary = "";
 
        Article a = new Article(ArticleTitle, ArticleText);
        string zeroth = WikiRegexes.ZerothSection.Match(a.ArticleText).Value;
        bool CircaLink = WikiRegexes.CircaLinkTemplate.IsMatch(a.ArticleText), Floruit = (!zeroth.Contains(@"[[floruit|fl.]]") && WikiRegexes.UnlinkedFloruit.IsMatch(zeroth));

        a.HideMoreText(HiderHideExtLinksImages);

        // The two slashes below are inserted to disable the insertion of non-breaking spaces HTML markup (sample) 
        // a.AWBChangeArticleText("Fix non-breaking spaces", parsers.FixNonBreakingSpaces(a.ArticleText), true);

        // a.AWBChangeArticleText("Mdashes", parsers.Mdashes(a.ArticleText, ArticleTitle), true);

        // a.AWBChangeArticleText("Fix Date Ordinals/Of", parsers.FixDateOrdinalsAndOf(a.ArticleText, ArticleTitle), true, true);


        a.AWBChangeArticleText("FixBrParagraphs", parsers.FixBrParagraphs(a.ArticleText).Trim(), true);

        if (!Tools.IsRedirect(a.ArticleText))
        {
            a.AWBChangeArticleText("Fix dates 1", parsers.FixDatesB(a.ArticleText, CircaLink, Floruit).Trim(), true);
        }

        a.UnHideMoreText(HiderHideExtLinksImages);

        if (!Tools.IsRedirect(a.ArticleText))
        {
            // FixDates does its own hiding
            a.AWBChangeArticleText("Fix dates 2", parsers.FixDatesA(a.ArticleText).Trim(), true);
        }

        a.HideText(removeText);

        if (Tools.IsRedirect(a.ArticleText))
        {
            a.AWBChangeArticleText("Redirect tagger", WikiFunctions.Parse.Parsers.RedirectTagger(a.ArticleText, ArticleTitle), true);

            a.AWBChangeArticleText("Fix syntax redirects", WikiFunctions.Parse.Parsers.FixSyntaxRedirects(a.ArticleText), true);
        }
        else
        {
            a.AWBChangeArticleText("Template redirects", WikiFunctions.Parse.Parsers.TemplateRedirects(a.ArticleText, WikiRegexes.TemplateRedirects), true);

            // a.AWBChangeArticleText("Fixes for {{Multiple issues}}", parsers.MultipleIssues(a.ArticleText), true);

            // a.AWBChangeArticleText("Fix whitespace in links", WikiFunctions.Parse.Parsers.FixLinkWhitespace(a.ArticleText, ArticleTitle), true);

            a.AWBChangeArticleText("Fix syntax", WikiFunctions.Parse.Parsers.FixSyntax(a.ArticleText), true, true);

            a.AWBChangeArticleText("Rename Template Parameters", WikiFunctions.Parse.Parsers.RenameTemplateParameters(a.ArticleText, WikiRegexes.RenamedTemplateParameters), true);
            
            // a.EmboldenTitles(parsers, false);

            // a.AWBChangeArticleText("Conversions", WikiFunctions.Parse.Parsers.Conversions(a.ArticleText), true);
            // a.AWBChangeArticleText("FixLivingThingsRelatedDates", WikiFunctions.Parse.Parsers.FixLivingThingsRelatedDates(a.ArticleText), true);
            a.AWBChangeArticleText("FixHeadings", WikiFunctions.Parse.Parsers.FixHeadings(a.ArticleText, ArticleTitle), true);

            // a.FixPeopleCategories(parsers, false);

            a.SetDefaultSort(Variables.LangCode, false, false);

            a.AWBChangeArticleText("Fix categories", WikiFunctions.Parse.Parsers.FixCategories(a.ArticleText), true);

            a.AWBChangeArticleText("Fix images", WikiFunctions.Parse.Parsers.FixImages(a.ArticleText), true);

            a.BulletExternalLinks(false);

            // a.CiteTemplateDates(parsers, false);

            // a.AWBChangeArticleText("Fix citation templates", WikiFunctions.Parse.Parsers.FixCitationTemplates(a.ArticleText), true, true);

            a.AWBChangeArticleText("Fix temperatures", WikiFunctions.Parse.Parsers.FixTemperatures(a.ArticleText), true);

            a.AWBChangeArticleText("Fix main article", WikiFunctions.Parse.Parsers.FixMainArticle(a.ArticleText), true);

            if(a.IsMissingReferencesDisplay && !Variables.LangCode.Equals("de"))
                a.AWBChangeArticleText("Fix reference tags", WikiFunctions.Parse.Parsers.FixReferenceListTags(a.ArticleText), true);

            a.AWBChangeArticleText("Fix empty links and templates", WikiFunctions.Parse.Parsers.FixEmptyLinksAndTemplates(a.ArticleText), true);

            a.AWBChangeArticleText("Fix empty references", WikiFunctions.Parse.Parsers.SimplifyReferenceTags(a.ArticleText), true);

            a.AWBChangeArticleText("DuplicateUnnamedReferences", WikiFunctions.Parse.Parsers.DuplicateUnnamedReferences(a.ArticleText), true);

            a.AWBChangeArticleText("DuplicateNamedReferences", WikiFunctions.Parse.Parsers.DuplicateNamedReferences(a.ArticleText), true);

            a.AWBChangeArticleText("SameRefDifferentName", WikiFunctions.Parse.Parsers.SameRefDifferentName(a.ArticleText), true);
            
            a.AWBChangeArticleText("Refs after punctuation", WikiFunctions.Parse.Parsers.RefsAfterPunctuation(a.ArticleText), true);
            
            if(!Variables.IsWikipediaEN)
                a.AWBChangeArticleText("ReorderReferences", WikiFunctions.Parse.Parsers.ReorderReferences(a.ArticleText), true);

            // a.AWBChangeArticleText("FixReferenceTags", WikiFunctions.Parse.Parsers.FixReferenceTags(a.ArticleText), true);

            a.AWBChangeArticleText("Add missing {{reflist}}", WikiFunctions.Parse.Parsers.AddMissingReflist(a.ArticleText), true, true);

            // a.AWBChangeArticleText("PersonData", WikiFunctions.Parse.Parsers.PersonData(a.ArticleText, ArticleTitle), true);

            a.FixLinks(false);

            // a.AWBChangeArticleText("Simplify links", WikiFunctions.Parse.Parsers.SimplifyLinks(a.ArticleText), true);
        }

        a.UnHideText(removeText);

        a.AWBChangeArticleText("Sort meta data", parsers.SortMetaData(a.ArticleText, ArticleTitle), true);

        return a.ArticleText;
}
