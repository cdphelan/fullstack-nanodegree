import webbrowser

class Movie():
    def __init__(self, movie_title, rt_consensus, rt_rating, poster_image, trailer_youtube):
        self.title = movie_title
        self.consensus = rt_consensus
        self.rating = rt_rating
        self.poster_image_url = poster_image
        self.trailer_youtube_url = trailer_youtube

    def show_trailer(self):
        webbrowser.open(self.trailer_youtube_url)
