# 212 VVS AB – premiumwebbplats

Öppna index.html i en modern webbläsare. Bilder, typsnitt, stilar och funktioner är inbäddade; ingen installation behövs. redigerbar.html är samma webbplats med separata assets- och fonts-mappar, som ska ligga bredvid filen. Alla sidor nås via navigationen. ZIP-paketet har även omdirigeringssidor för vyer och tidigare sidnamn.

## Innehåll och design
Stor helskärmshero med en verklig installationsbild från originalets galleri, originalets vita transparenta logotyp och en tydlig kontaktväg. Fem kompletta tjänstevyer, om-sida, sex bildvyer med bildvisare, galleri med kategorier och sökning, tre områdesvyer, kontakt, trestegsförfrågan, FAQ och integritet. Totalt 23 vyer. Mobilmeny, tydliga tangentbordsfokus, reducerad rörelse och fast kontaktfält på mobil. Designed by Ekom länkar till ekom.se.

## Kontakt och förfrågan
Formulären förbereder mejlutkast till info@212.se. Besökaren granskar texten, bifogar eventuella bilder i sitt mejlprogram och skickar själv. Ingen automatisk sändning, bokning eller beställning sker. Alternativet Kopiera förfrågan kopierar den granskade texten; om webbläsaren inte tillåter urklipp går sammanställningen att markera och kopiera manuellt. Telefonnummer och ort är frivilliga. Sidan lagrar ingen formulärdata efter omladdning och använder ingen analys, spårning, reklaminbäddning eller lokal lagring. Integritetstexten behöver uppdateras om en formulärserver eller annan databehandling ansluts.

## Källor och innehåll
Primärkälla är https://www.212.se/ och dess 14 lokala tjänstesidor samt integritetspolicy, hämtade 2026-11-25. Verksamhetsnamnet 212 VVS AB, telefon 076-010 56 58, mejl info@212.se och adress Ljungbylund 116, 361 92 Emmaboda följer originalets kontaktuppgifter. Fem tjänster och områdena Emmaboda, Nybro, Lessebo är källverifierade. Upprepade lokala SEO-sidor har sammanförts till tre användbara områdesvyer med länkar till tjänsterna; äldre namn finns som omdirigeringar.

Sex bilder är hämtade från originalwebbplatsen och har neutrala beskrivningar av synligt innehåll. Inga kundnamn, projektorter, datum, före-/efterkopplingar eller individuella personidentiteter har skapats. Familje-/gruppfotot med barn och en trägrind har valts bort från arbetsgalleriet. Originalets drönarvideo över Öland används inte som eget projektfoto. Logotypen har kvar sin originalform och transparens; bara tomma alfamarginaler har beskurits. Inga genererade bilder, falska recensioner, certifieringar, garantier, jourlöften, priser, grundår eller besparingssiffror har lagts till.

Bildadresser, alttexter, dimensioner, sammanhang och SHA256 finns i qa/assets.json. Företagsuppgifter och HTML-källornas URL/hashmanifest finns i qa/facts.json; research/SOURCES.md sammanfattar bedömningarna. Originalfiler ligger i det fullständiga projektets research/originals. Den fristående filen och ZIP-paketet innehåller de bilder som faktiskt används.

## Redigera och kontrollera
Källfiler finns i qa/template.html, qa/site.css, qa/site.js, qa/content.json och qa/media.json. Bygg med python3 qa/build.py, kontrollera med python3 qa/check.py. Python3 med BeautifulSoup samt Node krävs för att bygga och kontrollera, men behövs inte för att öppna webbplatsen.

Manrope används som lokalt typsnitt under SIL Open Font License, med licenstext i fonts/Manrope-LICENSE.txt och källadress/hash i qa/fonts.json. Navigeringen använder hashvyer för att fungera som fristående fil; titlar och beskrivningar byts vid navigering. Lösningen är inte en serverrenderad flersideswebbplats för sökmotorindexering.

Statisk kontroll omfattar alla vyer, interna länkar, JavaScript-syntax, lokala resurser, inbäddade filer, kontaktuppgifter, Ekom-länk och exakt ZIP-innehåll/CRC. Förfrågan granskas utan att något skickas. Webbplatsen ersätter inte den publicerade originalwebbplatsen.
