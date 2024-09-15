import chromadb
import os 
# from dotenv import load_dotenv
# load_dotenv()


# 我现在有如下几个 Collection，我想将每个collection都导出并生成独立的文件，然后再使用一个for循环再初始化每一个collection。请参考如下的代码，生成

# COLLECTION_COUNTRY = os.getenv("COLLECTION_COUNTRY")
# collection_name = COLLECTION_COUNTRY

# COLLECTION_DETAILS =os.getenv("COLLECTION_DETAILS")
# collection_name = COLLECTION_DETAILS

# COLLECTION_SCOPE=os.getenv("COLLECTION_SCOPE")
# collection_name = COLLECTION_SCOPE

# COLLECTION_REQUEST=os.getenv("COLLECTION_REQUEST")
# collection_name = COLLECTION_REQUEST

# COLLECTION_MULTI_SCOPE=os.getenv("COLLECTION_MULTI_SCOPE")
# collection_name = COLLECTION_MULTI_SCOPE
collection_name = "Just_For_Test"

client = chromadb.HttpClient(host='localhost',port='1235')

collection = client.get_or_create_collection(collection_name)

# # 删除collection
# result = client.list_collections()
# print(result)
# client.delete_collection(collection_name)

result = client.list_collections()
print(result)
print("result")