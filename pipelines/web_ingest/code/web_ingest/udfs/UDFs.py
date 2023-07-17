from pyspark.sql import *
from pyspark.sql.functions import *
from pyspark.sql.types import *
from prophecy.lookups import (
    createLookup,
    createRangeLookup,
    lookup,
    lookup_last,
    lookup_match,
    lookup_count,
    lookup_row,
    lookup_row_reverse,
    lookup_nth
)

def registerUDFs(spark: SparkSession):
    spark.udf.register("scrape_text", scrape_text)
    spark.udf.register("parse_subsections", parse_subsections)
    

    try:
        from prophecy.utils import ScalaUtil
        ScalaUtil.initializeUDFs(spark)
    except :
        pass

@udf(returnType = StringType())
def scrape_text(url: str):
    import requests
    from bs4 import BeautifulSoup
    response = requests.get(url)
    soup = BeautifulSoup(response.text, 'html.parser')
    text = soup.get_text(' ')

    return text

def parse_subsectionsGenerator():
    SECTIONS_TO_IGNORE = ["See also", "References", "External links", "Further reading", "Footnotes", "Bibliography",
                          "Sources", "Citations", "Literature", "Footnotes",
                          "Notes and references", "Photo gallery", "Works cited", "Photos",
                          "Gallery", "Notes", "References and sources",
                          "References and notes",]

    def all_subsections_from_section(section, parent_titles: list[str], sections_to_ignore: set[str], ):
        """
    From a Wikipedia section, return a flattened list of all nested subsections.
    Each subsection is a tuple, where:
        - the first element is a list of parent subtitles, starting with the page title
        - the second element is the text of the subsection (but not any children)
    """
        import mwparserfromhell
        headings = [str(h) for h in section.filter_headings()]

        if len(headings) == 0:
            return [["/".join(parent_titles), section.strip_code()]]

        title = headings[0]

        if title.strip("=" + " ") in sections_to_ignore:
            # ^wiki headings are wrapped like "== Heading =="
            return []

        titles = parent_titles + [title.strip("=" + " ")]
        full_text = str(section)
        section_text = full_text.split(title)[1]
        stripped_text = mwparserfromhell.parse(section_text).strip_code().strip()

        if not len(stripped_text):
            return []

        if len(headings) == 1:
            return [["/".join(titles), stripped_text]]
        else:
            first_subtitle = headings[1]
            section_text = section_text.split(first_subtitle)[0]
            results = [["/".join(titles), stripped_text]]

            for subsection in section.get_sections(levels = [len(titles) + 1]):
                subs = all_subsections_from_section(subsection, titles, sections_to_ignore)

                if len(subs):
                    results.extend(subs)

            return results

    def all_subsections_from_page(
            content: str,
            title,
            sections_to_ignore: set[str] = SECTIONS_TO_IGNORE,
    ):
        """From a Wikipedia page title, return a flattened list of all nested subsections.
    Each subsection is a tuple, where:
        - the first element is a list of parent subtitles, starting with the page title
        - the second element is the text of the subsection (but not any children)
    """
        import mwparserfromhell
        text = content
        parsed_text = mwparserfromhell.parse(text)

        for link in parsed_text.filter_wikilinks():
            if link.title.startswith("File:"):
                parsed_text.remove(link)

        results = []

        for subsection in parsed_text.get_sections(levels = [2], include_lead = True):
            subs = all_subsections_from_section(subsection, [title], sections_to_ignore)

            if len(subs):
                results.extend(subs)

        return results

    @udf(returnType = ArrayType(ArrayType(StringType())))
    def func(text: str, title: str):
        return all_subsections_from_page(text, title)

    return func

parse_subsections = parse_subsectionsGenerator()
