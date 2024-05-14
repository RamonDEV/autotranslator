import re
import json
from googletrans import Translator
from deep_translator import (GoogleTranslator,
                             ChatGptTranslator,
                             MicrosoftTranslator,
                             PonsTranslator,
                             LingueeTranslator,
                             MyMemoryTranslator,
                             YandexTranslator,
                             PapagoTranslator,
                             DeeplTranslator,
                             QcriTranslator,
                             single_detection,
                             batch_detection)

with open('config.json', 'r') as json_file:
    config_data = json.load(json_file)

translatorconfig = config_data.get('translator', None)
apikeyconfig = config_data.get('apikey', None)
languagesource = config_data.get('languagesource', None)
languageto = config_data.get('languageto', None)
removenumber = config_data.get('removenumbers', None)
deletestringsconfig = config_data.get('deletestrings', [])
translatevariables = config_data.get('variabletotranslate', [])
removestring = config_data.get('removenumbers', None)
removestringto = config_data.get('removestringto', None)

if translatorconfig == "GoogleTranslator":
    def translate_text(text):
        if text is None:
            return ""
        
        if deletestringsconfig:
            for string_substituir in deletestringsconfig:
                if string_substituir in text:
                    text = text.replace(string_substituir, '')

        if removenumber:
            text = re.sub(r'\d+', '', text)

        if removestring:
            if f'{removestring}' in text:
                text = text.replace(f'{removestring}', removestringto)
        
        if GoogleTranslator(source=languagesource, target=languageto).translate(text):
            translated = GoogleTranslator(source=languagesource, target=languageto).translate(text)
            if translated is not None:
                print("Traduzido de:", text ,"Para",translated)
                return translated
            else:
                return text
elif translatorconfig == "DeeplTranslator":
    def translate_text(text):
        if text is None:
            return ""
        
        if deletestringsconfig:
            for string_substituir in deletestringsconfig:
                if string_substituir in text:
                    text = text.replace(string_substituir, '')

        if removenumber:
            text = re.sub(r'\d+', '', text)

        if removestring:
            if f'{removestring}' in text:
                text = text.replace(f'{removestring}', removestringto)

        translated = DeeplTranslator(api_key=apikeyconfig, source=languagesource, target=languageto, use_free_api=True).translate(text)
        if translated is not None:
            print("Traduzido de:", text ,"Para",translated)
            return translated
        else:
            return text
elif translatorconfig == "Translator":
    def translate_text(text):
        if text is None:
            return ""
        
        if deletestringsconfig:
            for string_substituir in deletestringsconfig:
                if string_substituir in text:
                    text = text.replace(string_substituir, '')

        if removenumber:
            text = re.sub(r'\d+', '', text)

        if removestring:
            if f'{removestring}' in text:
                text = text.replace(f'{removestring}', removestringto)
        
        translator = Translator()
        translated = translator.translate(text, dest=languageto).text
        if translated is not None:
            print("Traduzido de:", text ,"Para",translated)
            return translated
        else:
            return text

def preserve_case(original, translated):
    if original.islower():
        return translated.lower()
    elif original.isupper():
        return translated.upper()
    elif original.istitle():
        return translated.title()
    else:
        return translated

with open('config_to_translate.lua', 'r', encoding='utf-8') as file:
    config_lines = file.readlines()


translated_lines = []
for line in config_lines:
    translated_line = line
    for variavel in translatevariables:
            if f"['{variavel}']" in translated_line:
                if '(' in translated_line:
                    translated_line = re.sub(rf"(\['{variavel}'\]\s*=\s*')([^']*)\(([^)]*)\)(.*?)'", lambda match: f"{match.group(1)}{preserve_case(match.group(2), translate_text(match.group(2)))}({preserve_case(match.group(3), match.group(3))}){match.group(4)}'", translated_line)
                else:
                    translated_line = re.sub(rf"(\['{variavel}'\]\s*=\s*')([^']*)'", lambda match: f"{match.group(1)}{preserve_case(match.group(2), translate_text(match.group(2)))}'", translated_line)
            elif f"{variavel} =" in translated_line:
                if '(' in translated_line:
                    translated_line = re.sub(rf"({variavel}\s*=\s*')([^']*)\(([^)]*)\)(.*?)'", lambda match: f"{match.group(1)}{preserve_case(match.group(2), translate_text(match.group(2)))}({preserve_case(match.group(3), match.group(3))}){match.group(4)}'", translated_line)
                else:
                    translated_line = re.sub(rf"({variavel}\s*=\s*')([^']*)'", lambda match: f"{match.group(1)}{preserve_case(match.group(2), translate_text(match.group(2)))}'", translated_line)
    translated_lines.append(translated_line)

with open('translated_config_to_translate.lua', 'w', encoding='utf-8') as file:
    file.writelines(translated_lines)

print("Tradução concluída. Arquivo 'translated_config_to_translate.lua' criado com sucesso.")
