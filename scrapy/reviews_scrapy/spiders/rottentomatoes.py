import scrapy
from scrapy.http import HtmlResponse
from selenium import webdriver
from selenium.webdriver.edge.service import Service
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time
from datetime import datetime

class RottenTomatoesSpider(scrapy.Spider):
    name = "rottentomatoes"

    movie_titles = [
        "Avatar","Jurassic Park", "Joker 2019", "The Dark Knight", "Avengers Endgame", 
        "Avengers Infinity War", "Captain America The Winter Soldier 2014", "Spider-Man No Way Home", 
        "Guardians of the Galaxy", "Thor The Dark World", "Iron Man", "Forrest Gump", 
        "Pulp Fiction", "Titanic", "Fantastic Beasts and Where to Find Them", "Frozen 2013", 
        "The Lion King", "Tangled", "Coco 2017", "Up", "Back to the Future", "Back to the Future 2", 
        "Back to the Future 3", "Jaws", "Catch Me If You Can", "Saving Private Ryan", "Aquaman 2018", 
        "Saw", "Skyfall", "Terminator", "Harry Potter and the Sorcerers Stone", 
        "Harry Potter and the Chamber of Secrets", "Harry Potter and the Prisoner of Azkaban", 
        "Harry Potter and the Goblet of Fire", "Harry Potter and the Order of the Phoenix", 
        "Harry Potter and the Half Blood Prince", "Harry Potter and the Deathly Hallows Part 1", 
        "Harry Potter and the Deathly Hallows Part 2", "Simpsons Movie", "The Maze Runner", 
        "Fight Club", "Matrix", "Interstellar 2014", "Butterfly Effect", "Ready Player One", 
        "Gladiator", "Django Unchained 2012", "Gangs of New York"
    ]

    def __init__(self, *args, **kwargs):
        super(RottenTomatoesSpider, self).__init__(*args, **kwargs)
        self.driver_path = 'C:/Users/yu/Downloads/msedgedriver.exe'
        self.service = Service(self.driver_path)
        self.driver = webdriver.Edge(service=self.service)
        self.extracted_reviews = set()  # Éviter les doublons de critiques

    def start_requests(self):
        base_url = 'https://www.rottentomatoes.com/m/'
        for title in self.movie_titles:
            formatted_title = title.lower().replace(" ", "_")
            url = f"{base_url}{formatted_title}/reviews"
            yield scrapy.Request(url, callback=self.parse)

    def parse(self, response):
        self.driver.get(response.url)
        time.sleep(3)

        # Gestion de la bannière de cookies
        try:
            cookie_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.ID, "onetrust-accept-btn-handler"))
            )
            cookie_button.click()
        except Exception as e:
            print("Aucune bannière de cookies détectée ou erreur :", e)

        # Clic sur le bouton "Load More" 1x
        try:
            load_more_button = WebDriverWait(self.driver, 10).until(
                EC.element_to_be_clickable((By.CSS_SELECTOR, 'rt-button[data-qa="load-more-btn"]'))
            )
            load_more_button.click()
            print("Clic sur 'Load More' effectué.")
            time.sleep(2)  # Attendre que les critiques soient chargées
        except Exception as e:
            print("Erreur lors du clic sur 'Load More' :", e)

        # Extraction des détails du film
        release_date = self.extract_release_date()
        genres = response.css('ul[data-qa="sidebar-movie-details"] li:nth-child(2)::text').get()
        if genres:
            genres = genres.strip().split(',')  # Liste des genres séparée par des virgules
        first_genre = genres[0].strip() if genres else 'Unknown'  # Premier genre seulement

        # Récupérer le HTML après les modifications
        html = self.driver.page_source
        scrapy_response = HtmlResponse(url=self.driver.current_url, body=html, encoding='utf-8')
        yield from self.parse_reviews(scrapy_response, release_date, first_genre)

    def extract_release_date(self):
        """Extraire la date de sortie avant les changements dynamiques."""
        try:
            details = self.driver.find_elements(By.CSS_SELECTOR, 'ul[data-qa="sidebar-movie-details"] li')
            release_date = 'Unknown'
            for element in details:
                text = element.text
                if "In Theaters:" in text:
                    raw_date = text.replace("In Theaters:", "").strip()
                    try:
                        release_date = datetime.strptime(raw_date, '%b %d, %Y').strftime('%d/%m/%Y')
                    except ValueError:
                        release_date = 'Unknown'
            return release_date
        except Exception as e:
            print("Erreur lors de l'extraction de la date de sortie :", e)
        return 'Unknown'

    def parse_reviews(self, response, release_date, first_genre):
        movie_title = response.css('a.sidebar-title::text').get().strip()

        reviews = response.css('.review-row')
        valid_scores = []

        for review in reviews:
            score = review.css('p.original-score-and-url::text').re_first(r'Original Score:\s*(\S+)')
            if score:
                if '/5' in score:
                    try:
                        valid_scores.append(float(score.split('/5')[0].strip()))
                    except ValueError:
                        pass
                elif '/10' in score:
                    try:
                        valid_scores.append(float(score.split('/10')[0].strip()) / 2)
                    except ValueError:
                        pass

        average_score = sum(valid_scores) / len(valid_scores) if valid_scores else 0

        for review in reviews:
            reviewer_name = review.css('a.display-name::text').get()
            review_text = review.css('p.review-text::text').get()

            score = review.css('p.original-score-and-url::text').re_first(r'Original Score:\s*(\S+)')
            if not score:
                score = str(average_score)
            else:
                if '/5' in score:
                    try:
                        score = str(float(score.split('/5')[0].strip()))
                    except ValueError:
                        score = str(average_score)
                elif '/10' in score:
                    try:
                        score = str(float(score.split('/10')[0].strip()) / 2)
                    except ValueError:
                        score = str(average_score)
                else:
                    score = str(average_score)

            review_date = review.css('p.original-score-and-url span[data-qa="review-date"]::text').get()

            if review_date:
                try:
                    formatted_date = datetime.strptime(review_date.strip(), '%b %d, %Y').strftime('%d/%m/%Y')
                except ValueError:
                    formatted_date = 'Unknown'
            else:
                formatted_date = 'Unknown'

            relative_url = review.css('a::attr(href)').get()
            review_url = response.urljoin(relative_url)
            review_url = review_url.split('.fr')[0] if '.fr' in review_url else review_url.split('.com')[0]

            review_key = (reviewer_name, review_text, score, formatted_date)  # Identifiant unique basé sur les données principales
            if review_key in self.extracted_reviews:
                continue
            self.extracted_reviews.add(review_key)

            yield {
                'ID Utilisateur': reviewer_name.strip() if reviewer_name else 'Unknown',
                'Note': score,
                'Commentaire': review_text.strip() if review_text else 'No text',
                'Date de publication': formatted_date,
                'URL de la critique': review_url,
                'Titre du film': movie_title,
                'Date de sortie': release_date,
                'Genre 1': first_genre,
            }

    def closed(self, reason):
        self.driver.quit()
