# Ren'Py_automatic_translations
Translate your Ren'Py projects with an AI

requirements:
1. Python
2. libraries:
  - textblob
  
``` pip install textblob```
  
  - pycontry 
  
```pip install pycontry```

When your project is complete then use this script.
* Step 1. Check the spelling of your project
* Step 2. Generate the translation files with the Ren'Py launcher,
          language names must be lowercase.
* Step 3. Make a copy of this file in the game folder of your project.
* step 4. Open a prompt in the game folder of your project and run this file
               ```$ python auto_translate.py [language]```
          where [language] is the ISO 639-1 code of the language of your project in lowercase.
* Step 5. You will find the translations files in the 'tl_output' folder, 
          replace the translations files in the 'tl' folder.
* Step 6. Remove this script and the 'tl_output' folder from your project.
* Step 7. Check the translations files and make the pertinent changes.

NOTE: This is a link where you can find the languages and their ISO639-1 codes
https://en.wikipedia.org/wiki/List_of_ISO_639-1_codes
