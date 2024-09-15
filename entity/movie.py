class Movie:
    def __init__(self, id, name, url, time, genre, release_time, intro, directors, writers, stars):
        self.id = id
        self.name = name
        self.url = url
        self.time = time
        self.genre = genre
        self.release_time = release_time
        self.intro = intro
        self.directors = directors
        self.writers = writers
        self.stars = stars
    
    def to_dict(self):
        return {
            "id": self.id,
            "name": self.name,
            "url": self.url,
            "time": self.time,
            "genre": self.genre,
            "release_time": self.release_time,
            "intro": self.intro,
            "directors": self.directors,
            "writers": self.writers,
            "stars": self.stars
        }