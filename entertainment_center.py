import media, fresh_tomatoes

#movies in movie library, to be handed to media.py to create Movie object
#EXAMPLE:
	#movie = media.Movie(movie_title, 
	#					RT_critics_consensus, 
	#					RT_rating, movie_poster_image, 
	#					trailer_youtube_url)
heathers = media.Movie("Heathers",
						"Dark, cynical, and subversive, Heathers gently applies a chainsaw to the conventions of the high school movie -- changing the game for teen comedies to follow.",
						"95%",
						"http://resizing.flixster.com/hx7xMt3339QVmNEUUXzluDCJuQ0=/175x270/dkpu1ddg7pbsk.cloudfront.net/movie/11/16/07/11160772_ori.jpg",
						"https://www.youtube.com/watch?v=CTmpKgocyYg")

alone = media.Movie("A Girl Walks Home Alone at Night",
					"A Girl Walks Home Alone at Night blends conventional elements into something brilliantly original -- and serves as a striking calling card for writer-director Ana Lily Amirpour.",
					"96%",
					"http://resizing.flixster.com/tAxlAeMDYXrKXQPAjEjtjNHLngk=/180x257/dkpu1ddg7pbsk.cloudfront.net/movie/11/18/10/11181094_ori.jpg",
					"https://www.youtube.com/watch?v=_YGmTdo3vuY")

right_one = media.Movie("Let the Right One In",
						"Let the Right One In reinvigorates the seemingly tired vampire genre by effectively mixing scares with intelligent storytelling.",
						"98%",
						"http://resizing.flixster.com/JUjzPACzXeb-BfNzvmAJvCmLyjI=/180x267/dkpu1ddg7pbsk.cloudfront.net/movie/10/92/37/10923703_ori.jpg",
						"https://www.youtube.com/watch?v=ICp4g9p_rgo")

snowpiercer = media.Movie("Snowpiercer",
						"Snowpiercer offers an audaciously ambitious action spectacular for filmgoers numb to effects-driven blockbusters.",
						"95%",
						"http://resizing.flixster.com/miXZmQuYtCCBVmM_YZdeDBnihjw=/180x270/dkpu1ddg7pbsk.cloudfront.net/movie/11/18/15/11181583_ori.jpg",
						"https://www.youtube.com/watch?v=nX5PwfEMBM0")

scott = media.Movie("Scott Pilgrim vs. the World",
					"Its script may not be as dazzling as its eye-popping visuals, but Scott Pilgrim vs. the World is fast, funny, and inventive.",
					"82%",
					"http://resizing.flixster.com/2191fflkDHM2iJuFcYI0Lph4Fig=/180x270/dkpu1ddg7pbsk.cloudfront.net/movie/11/16/89/11168901_ori.jpg",
					"https://www.youtube.com/watch?v=8NUBVcit5VM")

groundhog = media.Movie("Groundhog Day",
						"Smart, sweet, and inventive, Groundhog Day highlights Murray's dramatic gifts while still leaving plenty of room for laughs.",
						"96%",
						"http://resizing.flixster.com/iSlVJ6329xsws4_EbZfp4wPIFUM=/180x269/dkpu1ddg7pbsk.cloudfront.net/movie/11/17/62/11176227_ori.jpg",
						"https://www.youtube.com/watch?v=tSVeDx9fk60")

serenity = media.Movie("Serenity",
						"Snappy dialogue and goofy characters make this Wild Wild West soap opera in space fun and adventurous.",
						"82%",
						"http://resizing.flixster.com/ebhrKSO3JMWbyWHfthfIqu9ED64=/180x270/dkpu1ddg7pbsk.cloudfront.net/movie/11/17/07/11170768_ori.jpg",
						"https://www.youtube.com/watch?v=ZLv_GTmAbEE")

batman = media.Movie("The Dark Knight",
					"Dark, complex and unforgettable, The Dark Knight succeeds not just as an entertaining comic book film, but as a richly thrilling crime saga.",
					"94%",
					"http://resizing.flixster.com/csINXh6bBY_YMax7pD2fFGtGDjQ=/180x270/dkpu1ddg7pbsk.cloudfront.net/movie/11/16/51/11165160_ori.jpg",
					"https://www.youtube.com/watch?v=EXeTwQWrcwY")

#create list of all movies in movie library
movies = [heathers,alone,right_one,snowpiercer,scott,groundhog,serenity,batman]

#hand list of movies to fresh_tomatoes.py to create website
fresh_tomatoes.open_movies_page(movies)
