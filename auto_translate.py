# The MIT License (MIT)
#
# Copyright 2022 Erik Juárez-Guerrero <https://github.com/Moshibit>
#
# Permission is hereby granted, free of charge, to any person
# obtaining a copy of this software and associated documentation files
# (the "Software"), to deal in the Software without restriction,
# including without limitation the rights to use, copy, modify, merge,
# publish, distribute, sublicense, and/or sell copies of the Software,
# and to permit persons to whom the Software is furnished to do so,
# subject to the following conditions:
#
# The above copyright notice and this permission notice shall be
# included in all copies or substantial portions of the Software.
#
# THE SOFTWARE IS PROVIDED "AS IS", WITHOUT WARRANTY OF ANY KIND,
# EXPRESS OR IMPLIED, INCLUDING BUT NOT LIMITED TO THE WARRANTIES OF
# MERCHANTABILITY, FITNESS FOR A PARTICULAR PURPOSE AND
# NONINFRINGEMENT. IN NO EVENT SHALL THE AUTHORS OR COPYRIGHT HOLDERS BE
# LIABLE FOR ANY CLAIM, DAMAGES OR OTHER LIABILITY, WHETHER IN AN ACTION
# OF CONTRACT, TORT OR OTHERWISE, ARISING FROM, OUT OF OR IN CONNECTION
# WITH THE SOFTWARE OR THE USE OR OTHER DEALINGS IN THE SOFTWARE.


# This file generates automatic translations for renpy projects

# requirements:
# 1. Python
# 2. libraries:
#   - textblob 
#       $ pip install textblob
#   - pycontry 
#       $ pip install pycontry

# When your project is complete then use this script.
# Step 1. Check the spelling of your project
# Step 2. Generate the translation files with the Ren'Py launcher,
#         language names must be lowercase.
# Step 3. Make a copy of this file in the game folder of your project.
# step 4. Open a prompt in the game folder of your project and run this file
#               $ python auto_translate.py [language]
#         where [language] is the ISO 639-1 code of the language of your project in lowercase.
# Step 5. You will find the translations files in the 'tl_output' folder, check the 
#         translations and make the pertinent changes, replace the translations files
#         in the 'tl' folder.
# Step 6. Remove this script from your project

# NOTE: This is a link where you can find the languages and their ISO639-1 codes
# https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes


# *** Imports ***
import os
import re
import pycountry
import argparse
from textblob import TextBlob
from textblob import exceptions

# *** Constantes ***
# directorio de trabajo
WORK_PATH = os.getcwd()

# directorio de traduciones de Ren'Py
TRANSLATE_DIR = 'tl'

# directorio de salida
OUTPUT_DIR = 'tl_output'

# esta expresión regular encuentra lineas de tradución en los archivos de la carpeta './tl'
REGEX_UTIL = r'#\s.*\s".*"'


# *** Funciones ***

def argument_paser():
    """ parseo desde linea de instruciones """
    parser = argparse.ArgumentParser()
    parser.add_argument('source_lang')
    args = parser.parse_args()

    return args

def get_languages_dict():
    """ Diccionario de idiomas 
    { 'idioma' : 'ISO639-1' }
    """
    # primero obtenemos los valores, las claves ISO
    values = [lang.alpha_2 for lang in pycountry.languages if hasattr(lang, 'alpha_2')]

    # lista de idiomas, en inglés
    keys = [ ]
    for lang in values:
        l = pycountry.languages.get(alpha_2=lang).name
        keys.append(l.lower())

    # armamos el diccionario
    langs_dict = { k:v for (k,v) in zip(keys, values) }

    return langs_dict
 

def get_langs_to_translate(lang_dirs, dict):
    """ Regresas una lista carpetas contenidas en './tl' que pueden ser traducidas
    """
    for lang in lang_dirs:
        try:
            l = dict[lang]
        except KeyError:
            print('ERROR:', str(lang), 'language is not supported.')
            lang_dirs.remove(lang)
    return lang_dirs


def translate_file(origin_file, output_file, from_l, to_l):
    """ traducir un archivo a otro idioma
    """

    input_file = open(origin_file, 'rt', encoding='utf-8')
    output_file = open(output_file, 'wt', encoding='utf-8')

    translate_flag = False
    translated_line = ''

    for line in input_file:

        if translate_flag:
            translated_line = '"' + translated_line + '"'
            
            line_ = line.replace('""', translated_line)
            output_file.write(line_)
            translate_flag = False
        elif line.startswith('    old ') or re.search(REGEX_UTIL, line) is not None:
            split_list = line.split('"')
            line_to_translate = split_list[1]

            # * Tradución *
            try:
                o_tb = TextBlob(line_to_translate)
                translated_line = str(o_tb.translate(from_lang=from_l, to=to_l))
            except exceptions.NotTranslated:
                translated_line = line_to_translate
                # print('The string "', line_to_translate, '" no did not change', sep='')
            
            output_file.write(line)
            translate_flag = True
        else:
            output_file.write(line)
        
    input_file.close()
    output_file.close()


def main():
    """ funcion principal """
    ## *** parseo desde linea de instruciones ***
    args = argument_paser()

    # idioma de origen
    source_language = str(args.source_lang)


    ## ** Obtenemos el diccionario de idiomas **
    langs_dict = get_languages_dict()


    ## ** Creacion de las carpetas que usa el script **
    try:
        os.mkdir(os.path.join(WORK_PATH, OUTPUT_DIR))
    except FileExistsError:
        print('Cannot create a file that already exists')


    ## ** Idiomas que se van a traducir **
    # lista de los directorios de idiomas a traducir
    lang_dirs = os.listdir(os.path.join(WORK_PATH, TRANSLATE_DIR))

    # retira los idiomas no soportados
    lang_dirs = get_langs_to_translate(lang_dirs, langs_dict)


    ## ** creación de las subcarpetas en tr_output:
    for dir in lang_dirs:
        try:
            os.mkdir(os.path.join(WORK_PATH, OUTPUT_DIR, dir))
        except FileExistsError:
            print('Cannot create a file that already exists')


    # ** traduccion del archivo common.rpy **
    for lang in lang_dirs:
        # lista de archivos con extención '.rpy'
        file_list = [ ]
        for file_name in os.listdir(os.path.join(WORK_PATH, TRANSLATE_DIR, lang)):
            if file_name.endswith('.rpy'):
                file_list.append(file_name)

        for file_name in file_list:
            input_file = os.path.join(WORK_PATH, TRANSLATE_DIR, lang, file_name)
            output_file = os.path.join(WORK_PATH, OUTPUT_DIR, lang, file_name)
            print('translating', os.path.join(lang, file_name))
            if file_name == 'common.rpy':
                # el archivo 'common.rpy' siempre se traduce del inlgés.
                translate_file(input_file, output_file, 'en', langs_dict[lang])
            else:
                translate_file(input_file, output_file ,source_language, langs_dict[lang])

    print('Done.')


if __name__ == '__main__':
    main()
