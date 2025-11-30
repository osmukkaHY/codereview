# Codereview
* Sovelluksessa käyttäjät pystyvät jakamaan suhteellisen lyhyitä koodinpätkiä (esim 50 riviä, rivipituus max 80 merk.) toisilleen ja
  pyytää muita käyttäjiä arvostelemaan näitä.
  Käyttäjät saavat pisteitä kontribuutioistaan.
* Käyttäjä pystyy luomaan tunnuksen ja kirjautumaan sisään sovellukseen.
* Käyttäjä pystyy lisäämään tililleen koodinpätkiä.
* Käyttäjä pystyy muokkaamaan ja poistamaan näitä koodinpätkiä.
* Käyttäjä pystyy näkemään toisten käyttäjien koodinpätkät ja arvostelut.
* Käyttäjä pystyy kommentoimaan toisten käyttäjien koodinpätkiä ja antamaan niille arvostelun.
* Käyttäjä pystyy hakemaan tietokohteita filtterien (ohjelmointikieli, vastausen määrä, postauksen ikä ym.) perusteella.
* Sovelluksessa voi tarkastella toisten käyttäjien profiileja, joista näkee esimerkiksi kontribuutioiden määrän.

Tietokanta ja session-oliota varten tarvittava "secret" luodaan automaattisesti koodin suorituksen yhteydessä, jos niitä ei vielä ole.

# Ohjelman käyttöönotto (linux)
1. Luo python-virtuaaliympäristö komennolla "python3 -m venv env"
2. Aktivoi virtuaaliympäristö komennolla "source env/bin/activate"
3. Asenna riippuvuudet komennolla "pip install -r requirements.txt"
4. Käynnistä sovellus komennolla "flask run"
5. Mene selaimella osoitteeseen "127.0.0.1:5000"
6. Valmis.
Ohjelma luo automaattisesti tietokannan ja secretin tarvittaessa ohjelman käynnistyksen yhteydessä.

# Ohjelman käyttö
* Sign Up -painikkeesta pääsee rekisteröitymissivulle.
* Rekisteröinnin jälkeen voi kirjautua sisään.
* Log In -linkistä pääsee sisäänkirjautumissivulle.
* New Post -linkistä pääsee postauksenluomissivulle.
  * Tällä sivulla pystyy määrittelemään postaukselle otsikon, kertomaan koodistaan toisessa tekstilaatikossa ja kolmanteen laatikkoon voi laittaa itse koodin.
  * Postauksen voi julkaista "Submit Query"-napista, jonka jälkeen sen näkee etusivulta.
* Halkupalkkiin voi kirjoittaa avainsanan/tekstinpätkän ja hakunappia painamalla ohjelma hakee kaikki postaukset, joissa kyseinen teksti esiintyy postauksen
  koodi-osiossa (Alin laatikko postausta luodessa). Myöhemmin lisään postauksille koodikieli-attribuutin ja sitten postauksia voi rajata kielen perusteella.
* Painamalla postauksen previewissä näkyvää linkkiä pääsee näkemään postauksen koko sisällön.
  * Täältä postauksen tekijä pystyy poistamaan tai muokkaamaan postausta.
    * Tällä hetkellä poistamisnappi poistaa postauksen ilman varoitusta.
    * Edit-nappi toimii tällä hetkellä niin, että se kopioi vanhan postauksen sisällön uuden postauksen luomisformiin ja poistaa vanhan postauksen,
      eli jos menee muokkaamaan postausta ja menee pois ikkunasta, poistuu kyseinen postaus tietokannasta.

  * You can now filter search results by language from the drop down menu next to the search button.
  * You can also view your profile by pressing the button from the navigation section.
  * You can also add comments to posts when viewing a post.
