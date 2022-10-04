# Ren'Py_automatic_translations
Translate your Ren'Py projects with an AI

requirements:
1. Python
2. libraries:
  - textblob
  
``` pip install textblob```
  
  - pycontry 
  
```pip inttall pycontry```

When your project is complete then use this script.
* Step 1. Check spelling and syntax.
* Step 2. Generate the translation files with the Ren'Py launcher,
        language names must be lowercase.
* Step 3. Make a copy of this file in the game folder of your project.
* step 4. Open a prompt in the game folder of your project and run this file

        ```$ python auto_translate.py [language]```

    where [language] is the ISO 639-1 code of the language of your project in lowercase.
* Step 5. You will find the traditions in the 'tl_output' folder, check the 
        traditions and make the pertinent changes, replace the translations
        in the 'tl' folder.
* Step 6. Remove this script from your project
