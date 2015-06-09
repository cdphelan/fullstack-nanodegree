import media, fresh_tomatoes

#movies in movie library, to be handed to media.py to create Movie object
heathers = media.Movie("Heathers",
						"http://resizing.flixster.com/hx7xMt3339QVmNEUUXzluD"+
						"CJuQ0=/175x270/dkpu1ddg7pbsk.cloudfront.net/movie/1"+
						"1/16/07/11160772_ori.jpg",
						"https://www.youtube.com/watch?v=CTmpKgocyYg")

alone = media.Movie("A Girl Walks Home Alone at Night",
					"http://resizing.flixster.com/tAxlAeMDYXrKXQPAjEjtjNHLng"+
					"k=/180x257/dkpu1ddg7pbsk.cloudfront.net/movie/11/18/10/"+
					"11181094_ori.jpg",
					"https://www.youtube.com/watch?v=_YGmTdo3vuY")

right_one = media.Movie("Let the Right One In",
						"http://resizing.flixster.com/JUjzPACzXeb-BfNzvmAJvC"+
						"mLyjI=/180x267/dkpu1ddg7pbsk.cloudfront.net/movie/1"+
						"0/92/37/10923703_ori.jpg",
						"https://www.youtube.com/watch?v=ICp4g9p_rgo")

snowpiercer = media.Movie("Snowpiercer",
						"http://resizing.flixster.com/miXZmQuYtCCBVmM_YZdeDB"+
						"nihjw=/180x270/dkpu1ddg7pbsk.cloudfront.net/movie/1"+
						"1/18/15/11181583_ori.jpg",
						"https://www.youtube.com/watch?v=nX5PwfEMBM0")

scott = media.Movie("Scott Pilgrim vs. the World",
					"http://resizing.flixster.com/2191fflkDHM2iJuFcYI0Lph4Fi"+
					"g=/180x270/dkpu1ddg7pbsk.cloudfront.net/movie/11/16/89/"+
					"11168901_ori.jpg",
					"https://www.youtube.com/watch?v=8NUBVcit5VM")

groundhog = media.Movie("Groundhog Day",
						"http://resizing.flixster.com/iSlVJ6329xsws4_EbZfp4w"+
						"PIFUM=/180x269/dkpu1ddg7pbsk.cloudfront.net/movie/1"+
						"1/17/62/11176227_ori.jpg",
						"https://www.youtube.com/watch?v=tSVeDx9fk60")

serenity = media.Movie("Serenity",
						"http://resizing.flixster.com/ebhrKSO3JMWbyWHfthfIqu"+
						"9ED64=/180x270/dkpu1ddg7pbsk.cloudfront.net/movie/11"+
						"/17/07/11170768_ori.jpg",
						"https://www.youtube.com/watch?v=ZLv_GTmAbEE")

batman = media.Movie("The Dark Knight",
					"http://resizing.flixster.com/csINXh6bBY_YMax7pD2fFGtGDj"+
					"Q=/180x270/dkpu1ddg7pbsk.cloudfront.net/movie/11/16/51/"+
					"11165160_ori.jpg",
					"https://www.youtube.com/watch?v=EXeTwQWrcwY")

#create list of all movies in movie library
movies=[heathers,alone,right_one,snowpiercer,scott,groundhog,serenity,batman]

#hand list of movies to fresh_tomatoes.py to create website
fresh_tomatoes.open_movies_page(movies)
