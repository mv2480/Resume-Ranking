import os
from nltk.corpus import stopwords
import re
from io import StringIO
from pdfminer.pdfinterp import PDFResourceManager, PDFPageInterpreter
from pdfminer.converter import TextConverter
from pdfminer.layout import LAParams
from pdfminer.pdfpage import PDFPage


class ResumeRanking:## class for ranking resumes


    def convertPdf2Text(self, path, pages=None):## function to convert pdf to text
        if not pages:
            pagenums = set()
        else:
            pagenums = set(pages)

        output = StringIO()
        manager = PDFResourceManager()
        converter = TextConverter(manager, output, laparams=LAParams())
        interpreter = PDFPageInterpreter(manager, converter)

        infile = open(path, 'rb')
        for page in PDFPage.get_pages(infile, pagenums):
            interpreter.process_page(page)
        infile.close()
        converter.close()
        text = output.getvalue()
        output.close
        return text

    def tokenizeAndCleantext(self,text):## function to clean and tokenize text
        resumeTxtNoStopword = []
        sw = set(stopwords.words('english'))
        text = text.split()
        useful_words = [w for w in text if w not in sw]
        resumeTxtNoStopword.append(" ".join(useful_words))
        text = resumeTxtNoStopword
        pattern = re.compile(r'[A-Za-z]+[\w^\']*|[\w^\']*[A-Za-z]+[\w^\']*')
        return pattern.findall(text[0].lower())

    def getAvergeCategoryScore(self,resume,progWords = None,csWords = None,engWords = None,finWords = None,manWords = None,artWords = None):## function to generate score for given resume
        if (progWords == None):
            programming = ["assembly", "bash", " c ", "c++", "c#", "coffeescript", "emacs lisp",
                           "go!", "groovy", "haskell", "java", "javascript", "matlab", "max MSP", "objective c",
                           "perl", "php", "html", "xml", "css", "processing", "python", "ruby", "sml", "swift",
                           "latex" "unity", "unix", "visual basic", "wolfram language", "xquery", "sql", "node.js",
                           "scala", "kdb", "jquery", "mongodb"]
        else:
            programming = progWords
        programmingTotal = 0

        for i in range(len(programming)):
            if programming[i].lower() in resume != -1:
                programmingTotal += 1

        progScore = min(programmingTotal / 10.0, 1) * 5.0

        if (csWords == None):
            csKeyWords = ["computer", "software", "engineering", "computer science", "prototype", "structured design",
                          "code development", "communication skills", "problem solving", "software design", "systems",
                          "web", "client",
                          "testing", "SDLC", "development process", "database management systems", "web applications",
                          "code","user support", "programming", "developing", "software", "server administration",
                          "machine learning",
                          "alogorithms", "team", "programming language", "database", "artificial intelligence",
                          "administrator"]
        else:
            csKeyWords = csWords

        csWordScore = []
        for i in range(len(csKeyWords)):
            csWordScore.append(0)
            if csKeyWords[i].lower() in resume != -1:
                csWordScore[i] += 1

        csScore = min((float)(sum(csWordScore) + 10) / (len(csKeyWords)), 1.0) * 25.0

        if finWords == None:
            financeKeyWords = ["financial reporting", "excel", "finance", "trend analysis",
                               "financial statement", "result analysis", "strategic planning", "develop trends",
                               "DCF", "presentation skills", "team player", "financial analysis", "forecasting",
                               "policy development", "business policies", "powerpoint", "microsoft word", "analytical",
                               "accounting", "team player", "team", "ability", "accounting", "accountant",
                               "balance sheet",
                               "liquidy", "money", "stocks"]
        else:
            financeKeyWords = finWords

        finWordScore = []
        for i in range(len(financeKeyWords)):
            finWordScore.append(0)
            if financeKeyWords[i].lower() in resume != -1:
                finWordScore[i] += 1

        finScore = min((float)(sum(finWordScore) + 10) / len(financeKeyWords), 1.0) * 25.0

        if (engWords == None):
            engineeringKeyWords = ["chemical", "civil", "engineering", "mechanical", "CAD", "design",
                                   "mechanics", "analysis", "systems", "technical", "autodesk", "inventor", "skills",
                                   "realization",
                                   "technology", "functionality", "hardware", "design process", "process control",
                                   "protyping", "team",
                                   "project conceptualization", "design verification", "project management",
                                   "structural design",
                                   "build", "modeling", "buildings", "tests", "application"]
        else:
            engineeringKeyWords = engWords

        engWordScore = []
        for i in range(len(engineeringKeyWords)):
            engWordScore.append(0)
            if engineeringKeyWords[i].lower() in resume != -1:
                engWordScore[i] += 1

        engScore = min((float)(sum(engWordScore) + 10) / len(engineeringKeyWords), 1.0) * 25.0

        if manWords == None:
            managementKeyWords = ["data analysis", "automation", "planning", "ability to plan",
                                  "customer", "interaction", "consumer", "implement", "analytical", "network",
                                  "skill analysis", "hiring", "firing", "business development", "contract negotiation",
                                  "budget", "leadership", "operational development", "evaluations", "management",
                                  "business", "project planning", "production schedule", "responsibility", "budgeting",
                                  "optimization", "decision making", "organization", "business"]
        else:
            managementKeyWords = manWords

        manWordScore = []
        for i in range(len(managementKeyWords)):
            manWordScore.append(0)
            if managementKeyWords[i].lower() in resume != -1:
                manWordScore[i] += 1

        manScore = min((float)(sum(manWordScore) + 10) / len(managementKeyWords), 1.0) * 25.0

        if artWords == None:
            artsKeyWords = ["performance", "exhibit", "music", "art", "writing", "expressive",
                            "editing", "editorial", "social work", "design", "artist", "musician", "collaborative",
                            "group", "program", "exhibition", "media", "blog", "journalism", "creative", "innovative",
                            "workshop", "master class", "teaching", "lectures", "practice", "studio", "newspaper",
                            "english"]
        else:
            artsKeyWords = artWords

        artsWordScore = []
        for i in range(len(artsKeyWords)):
            artsWordScore.append(0)
            if artsKeyWords[i].lower() in resume != -1:
                artsWordScore[i] += 1

        artsScore = min((float)(sum(artsWordScore) + 10) / len(artsKeyWords), 1.0) * 25.0

        average_score = (progScore + csScore + engScore + finScore + manScore + artsScore)

        return average_score


def main():
    resumeDir = 'data/clean_resume/'

    resume_ranking = ResumeRanking()
    resume_ranks = []
    for filename in os.listdir(resumeDir):
        text = resume_ranking.convertPdf2Text(resumeDir+filename)
        resume_txt = resume_ranking.tokenizeAndCleantext(text)
        score = resume_ranking.getAvergeCategoryScore(resume_txt)
        resume_ranks.append([filename,score])

    resume_ranks.sort(key=lambda x: -x[1])
    print(resume_ranks)




if __name__ == "__main__":
    main()






