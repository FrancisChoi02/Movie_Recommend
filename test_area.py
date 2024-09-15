import os
import asyncio
from service.openai import get_rag_information,call_gpt
from service.movie_service import get_genreId_reverse
from entity.movie import Movie
# movieId = "1"

# raw = get_moive_dao(movieId)
# print(raw[-1])

# result = split_genre_to_list(raw[-1])
# print(result)

# genre_str = "Drama"

# result = get_movie_with_genre_dao(genre_str)
# print(len(result))

# movieId = "4"
# movie = get_movie_with_movieId_dao(movieId)
# print(movie)

# pos_URL = get_movie_posterURL_with_movieId_dao(movieId)
# print(pos_URL)

# with open("D:\\Movie_Recommend\\static\prompt\\tag_extraction.txt",'r', encoding='utf-8') as f:
#     prompt = f.read() 
# query = "Movie played by Shawn Wayans"
# result = asyncio.run(call_gpt(query,prompt))
# print(result)

# query_string = "{'movie_name': 'Hung fan kui (1995) ', 'directors': 'Stanley Tong', 'stars': 'Jackie Chan|Anita Mui|Fran?oise Yip', 'genre': 'Action|Comedy|Crime'}"
# COLLECTION_MIX = os.getenv("COLLECTION_MIX")

# collection_name = COLLECTION_MIX
# matched,retrieved_detail = get_rag_information(query_string,collection_name)
# print(matched)
# print(retrieved_detail)


genre_id = "14"
genre_str = get_genreId_reverse(genre_id)
print(genre_str)
