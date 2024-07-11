from openness.services.Utils import Utils


class LanguageService:
    def __init__(self):
        self.language_composition = None

    def get_active_languages(self, myproject):
        language_settings = myproject.LanguageSettings
        enum = Utils().get_attributes(["ActiveLanguages"], language_settings)
        return enum[0]
        
    def get_language_by_culture(self, myproject, language_culture):
        for language in myproject.LanguageSettings.Languages:
            culture = Utils().get_attributes(["Culture"], language)
            if str(culture[0]) == language_culture:
                return language
        
        raise Exception("Language not found")

    def add_language(self, myproject, language_culture):
        try:
            if self.language_composition is None:
                self.language_composition = self.get_active_languages(myproject)
            language = self.get_language_by_culture(myproject, language_culture)
            self.language_composition.Add(language)
        except Exception as e:
            raise Exception("Failed to add language to composition: " + str(e))